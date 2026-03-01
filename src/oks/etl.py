"""Minimal Markdown ETL pipeline for the repository's content corpus."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml


FRONT_MATTER_PATTERN = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.DOTALL)
SECTION_PATTERN = re.compile(r"(?=^##\s)", re.MULTILINE)
NON_ALNUM_PATTERN = re.compile(r"[^a-z0-9]+")


@dataclass(frozen=True)
class ChunkRecord:
    """Normalized chunk record emitted by the ETL slice."""

    id: str
    heading: str
    content: str
    order: int
    source_file: str
    source_path: str
    document_title: str
    document_slug: str
    metadata: dict[str, Any]


def parse_front_matter(front_matter: str) -> dict[str, Any]:
    """Parse YAML front matter into a normalized dictionary."""

    parsed = yaml.safe_load(front_matter) if front_matter.strip() else {}
    if parsed is None:
        return {}
    if not isinstance(parsed, dict):
        raise ValueError("YAML front matter must parse to a mapping")
    return parsed


def split_front_matter(markdown_text: str) -> tuple[dict[str, Any], str]:
    """Split Markdown text into front matter metadata and body."""

    match = FRONT_MATTER_PATTERN.match(markdown_text)
    if not match:
        return {}, markdown_text
    metadata = parse_front_matter(match.group(1))
    body = match.group(2)
    return metadata, body


def slugify(value: str) -> str:
    """Create a stable slug for ids and graph projection keys."""

    normalized = NON_ALNUM_PATTERN.sub("-", value.strip().lower()).strip("-")
    return normalized or "item"


def chunk_markdown_by_heading(body: str) -> list[dict[str, Any]]:
    """Split Markdown body into level-two sections."""

    stripped_body = body.strip()
    if not stripped_body:
        return []

    sections = SECTION_PATTERN.split(stripped_body)
    chunks: list[dict[str, Any]] = []
    for section in sections:
        trimmed = section.strip()
        if not trimmed:
            continue
        heading_match = re.match(r"^##\s+(.*)", trimmed)
        title = heading_match.group(1).strip() if heading_match else "Intro"
        chunks.append(
            {
                "heading": title,
                "content": trimmed,
            }
        )
    return chunks


def build_chunk_id(source_stem: str, order: int, heading: str) -> str:
    """Build a deterministic chunk identifier."""

    return f"{slugify(source_stem)}-{order:03d}-{slugify(heading)}"


def extract_chunks_from_file(file_path: Path) -> list[dict[str, Any]]:
    """Extract normalized chunks from a Markdown file."""

    raw_markdown = file_path.read_text(encoding="utf-8")
    metadata, body = split_front_matter(raw_markdown)
    source_stem = file_path.stem
    document_slug = str(metadata.get("slug", slugify(source_stem)))
    document_title = str(metadata.get("title", source_stem.replace("_", " ").title()))

    records: list[dict[str, Any]] = []
    for order, chunk in enumerate(chunk_markdown_by_heading(body), start=1):
        record = ChunkRecord(
            id=build_chunk_id(source_stem, order, chunk["heading"]),
            heading=chunk["heading"],
            content=chunk["content"],
            order=order,
            source_file=file_path.name,
            source_path=str(file_path),
            document_title=document_title,
            document_slug=document_slug,
            metadata=metadata,
        )
        records.append(asdict(record))
    return records


def collect_markdown_files(path: Path) -> list[Path]:
    """Collect Markdown files from a file or directory input."""

    if path.is_file():
        if path.suffix != ".md":
            raise ValueError(f"Expected a Markdown file, got: {path}")
        return [path]
    if path.is_dir():
        return sorted(file_path for file_path in path.glob("*.md") if file_path.is_file())
    raise FileNotFoundError(f"Input path does not exist: {path}")


def build_chunk_corpus(path: Path) -> list[dict[str, Any]]:
    """Build a normalized chunk corpus from a file or directory."""

    corpus: list[dict[str, Any]] = []
    for file_path in collect_markdown_files(path):
        corpus.extend(extract_chunks_from_file(file_path))
    return corpus


def normalize_topics(metadata: dict[str, Any]) -> list[str]:
    """Normalize optional topic/tag metadata into a stable string list."""

    tags = metadata.get("tags") or metadata.get("topics") or []
    if isinstance(tags, str):
        raw_topics = [topic.strip() for topic in tags.split(",")]
    elif isinstance(tags, list):
        raw_topics = [str(topic).strip() for topic in tags]
    else:
        raw_topics = []
    return sorted({topic for topic in raw_topics if topic})


def build_graph_projection(chunks: list[dict[str, Any]]) -> dict[str, Any]:
    """Build a graph-friendly projection of chunk records."""

    chapters: dict[str, dict[str, Any]] = {}
    topics: dict[str, dict[str, str]] = {}
    authors: dict[str, dict[str, str]] = {}
    schemas: dict[str, dict[str, str]] = {
        "MarkdownChunk": {"name": "MarkdownChunk", "version": "1.0"}
    }
    contains: list[dict[str, Any]] = []
    tagged_with: list[dict[str, str]] = []
    wrote: list[dict[str, str]] = []
    validated_by: list[dict[str, str]] = []

    for chunk in chunks:
        chapter_slug = chunk["document_slug"]
        chapter = chapters.setdefault(
            chapter_slug,
            {
                "slug": chapter_slug,
                "title": chunk["document_title"],
                "source_file": chunk["source_file"],
            },
        )
        chapter["title"] = chunk["document_title"]

        contains.append(
            {
                "chapter_slug": chapter_slug,
                "chunk_id": chunk["id"],
                "order": chunk["order"],
            }
        )
        validated_by.append(
            {
                "chunk_id": chunk["id"],
                "schema": "MarkdownChunk",
            }
        )

        metadata = chunk["metadata"]
        for topic in normalize_topics(metadata):
            topics.setdefault(topic, {"name": topic})
            tagged_with.append(
                {
                    "chunk_id": chunk["id"],
                    "topic": topic,
                }
            )

        author = metadata.get("author")
        if author:
            author_name = str(author).strip()
            if author_name:
                authors.setdefault(author_name, {"name": author_name})
                wrote.append(
                    {
                        "author": author_name,
                        "chunk_id": chunk["id"],
                    }
                )

    return {
        "chapters": sorted(chapters.values(), key=lambda item: item["slug"]),
        "chunks": chunks,
        "topics": sorted(topics.values(), key=lambda item: item["name"]),
        "authors": sorted(authors.values(), key=lambda item: item["name"]),
        "schemas": sorted(schemas.values(), key=lambda item: item["name"]),
        "relationships": {
            "contains": contains,
            "tagged_with": tagged_with,
            "wrote": wrote,
            "validated_by": validated_by,
        },
    }


def write_json(path: Path, payload: Any) -> None:
    """Write JSON output, creating parent directories if needed."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_argument_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""

    parser = argparse.ArgumentParser(description="Build normalized ETL outputs from Markdown.")
    parser.add_argument("input", type=Path, help="Markdown file or directory to process")
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Path to write normalized chunk JSON",
    )
    parser.add_argument(
        "--graph-output",
        type=Path,
        help="Optional path to write graph projection JSON",
    )
    return parser


def run_cli(argv: list[str] | None = None) -> int:
    """Run the ETL CLI."""

    parser = build_argument_parser()
    args = parser.parse_args(argv)

    chunks = build_chunk_corpus(args.input)
    write_json(args.output, chunks)
    if args.graph_output:
        write_json(args.graph_output, build_graph_projection(chunks))
    return 0


def main() -> None:
    """Console entry point."""

    raise SystemExit(run_cli())


if __name__ == "__main__":
    main()
