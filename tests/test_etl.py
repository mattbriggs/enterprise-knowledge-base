import pytest
from pathlib import Path
from typing import List, Dict
import re
import yaml

# Assume ETL utilities live in a local module or inline for test purposes

CONTENT_DIR = Path(__file__).resolve().parent.parent / "content"

def split_front_matter(md_text: str):
    match = re.match(r'^---\n(.*?)\n---\n(.*)', md_text, re.DOTALL)
    if match:
        meta = yaml.safe_load(match.group(1))
        body = match.group(2)
    else:
        meta = {}
        body = md_text
    return meta, body

def chunk_markdown_by_heading(body: str) -> List[Dict]:
    pattern = re.compile(r'(?=^##\s)', re.MULTILINE)
    sections = pattern.split(body)
    chunks = []
    for section in sections:
        heading_match = re.match(r'^##\s+(.*)', section.strip())
        title = heading_match.group(1) if heading_match else "Intro"
        chunks.append({
            "heading": title.strip(),
            "content": section.strip()
        })
    return chunks

def extract_chunks_from_file(file_path: Path) -> List[Dict]:
    with open(file_path, "r", encoding="utf-8") as f:
        raw_md = f.read()
    meta, body = split_front_matter(raw_md)
    chunks = chunk_markdown_by_heading(body)
    for chunk in chunks:
        chunk["source_file"] = file_path.name
        chunk["metadata"] = meta
    return chunks

# --------------------------
# ✅ Pytest Test Cases
# --------------------------

def test_markdown_files_exist():
    files = list(CONTENT_DIR.glob("*.md"))
    assert len(files) > 0, "No Markdown files found in content/"

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
    sample = "## Heading A\n\nText for A.\n\n## Heading B\n\nMore text."
    chunks = chunk_markdown_by_heading(sample)
    assert len(chunks) == 2
    assert chunks[0]["heading"] == "Heading A"
    assert "Text for A" in chunks[0]["content"]

def test_etl_extracts_all_chunks():
    files = list(CONTENT_DIR.glob("*.md"))
    total_chunks = []
    for file in files:
        chunks = extract_chunks_from_file(file)
        total_chunks.extend(chunks)
    assert len(total_chunks) > 0, "ETL did not extract any chunks"
    for chunk in total_chunks:
        assert "heading" in chunk
        assert "content" in chunk
        assert "metadata" in chunk