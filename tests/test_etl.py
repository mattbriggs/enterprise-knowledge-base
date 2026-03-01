import json
from pathlib import Path

from oks.etl import (
    build_chunk_corpus,
    build_graph_projection,
    chunk_markdown_by_heading,
    extract_chunks_from_file,
    run_cli,
    split_front_matter,
)


CONTENT_DIR = Path(__file__).resolve().parent.parent / "content"


def test_markdown_files_exist():
    files = list(CONTENT_DIR.glob("*.md"))
    assert files, "No Markdown files found in content/"


def test_split_front_matter_parses_metadata():
    test_md = """---
title: Test Chapter
slug: test-chapter
---

## Heading One

Content under heading one.
"""
    meta, body = split_front_matter(test_md)
    assert meta["title"] == "Test Chapter"
    assert "## Heading One" in body


def test_chunk_extraction_creates_chunks():
    sample = "Intro paragraph.\n\n## Heading A\n\nText for A.\n\n## Heading B\n\nMore text."
    chunks = chunk_markdown_by_heading(sample)
    assert len(chunks) == 3
    assert chunks[0]["heading"] == "Intro"
    assert chunks[1]["heading"] == "Heading A"
    assert "Text for A" in chunks[1]["content"]


def test_extract_chunks_from_file_normalizes_metadata(tmp_path: Path):
    file_path = tmp_path / "sample.md"
    file_path.write_text(
        """---
title: Sample Chapter
slug: sample-chapter
author: Test Author
tags:
  - etl
  - markdown
---

## First Section

Body text.
""",
        encoding="utf-8",
    )

    chunks = extract_chunks_from_file(file_path)
    assert len(chunks) == 1
    assert chunks[0]["source_file"] == "sample.md"
    assert chunks[0]["document_slug"] == "sample-chapter"
    assert chunks[0]["metadata"]["author"] == "Test Author"


def test_etl_extracts_repo_content():
    total_chunks = build_chunk_corpus(CONTENT_DIR)
    assert total_chunks, "ETL did not extract any chunks"
    assert len({chunk["id"] for chunk in total_chunks}) == len(total_chunks)
    for chunk in total_chunks:
        assert chunk["heading"]
        assert chunk["content"]
        assert isinstance(chunk["metadata"], dict)


def test_graph_projection_contains_relationships(tmp_path: Path):
    file_path = tmp_path / "graphable.md"
    file_path.write_text(
        """---
title: Graphable Chapter
slug: graphable
author: Final State Press
tags: etl, graph
---

## Section One

Body text.
""",
        encoding="utf-8",
    )

    chunks = extract_chunks_from_file(file_path)
    graph = build_graph_projection(chunks)
    assert graph["chapters"][0]["slug"] == "graphable"
    assert graph["topics"][0]["name"] == "etl"
    assert graph["authors"][0]["name"] == "Final State Press"
    assert graph["relationships"]["validated_by"][0]["schema"] == "MarkdownChunk"


def test_cli_writes_chunk_and_graph_outputs(tmp_path: Path):
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    (content_dir / "cli.md").write_text(
        """---
title: CLI Chapter
slug: cli-chapter
---

## Section One

Body text.
""",
        encoding="utf-8",
    )

    chunk_output = tmp_path / "build" / "chunks.json"
    graph_output = tmp_path / "build" / "graph.json"

    exit_code = run_cli(
        [
            str(content_dir),
            "--output",
            str(chunk_output),
            "--graph-output",
            str(graph_output),
        ]
    )

    assert exit_code == 0
    assert json.loads(chunk_output.read_text(encoding="utf-8"))[0]["document_slug"] == "cli-chapter"
    assert json.loads(graph_output.read_text(encoding="utf-8"))["chapters"][0]["slug"] == "cli-chapter"


def test_content_files_do_not_contain_placeholder_todos():
    for file_path in CONTENT_DIR.glob("*.md"):
        text = file_path.read_text(encoding="utf-8")
        assert "_TODO: Add content._" not in text, f"Placeholder content remains in {file_path.name}"
