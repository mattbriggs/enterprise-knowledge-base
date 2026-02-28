---
title: "Authoring & ETL"
slug: 04_authoring_etl
---

# 4. Authoring & ETL

Chapter 4 anchors the manuscript in the first implemented boundary that is both real and central to the larger design. It explains how author-facing Markdown becomes machine-friendly records, which rules govern that transformation, and where the implementation draws hard boundaries.

The ETL layer in `src/oks/etl.py` is intentionally narrow. It does not implement schema CRUD, semantic enrichment, or database persistence. It does implement the boundary those later capabilities depend on: parse, normalize, identify, and emit deterministic records.

## 4.1 The Authoring Contract

The current authoring contract is small enough to reason about precisely:

- Each source document is a Markdown file.
- Optional YAML front matter stores document metadata such as `title` and `slug`.
- The Markdown body is chunked at level-two headings, meaning headings that begin with `## ` at the start of a line.
- Each emitted chunk inherits the document metadata and the source file identity.

This contract is intentionally conservative. It does not pretend that arbitrary Markdown is already a robust data model. Instead, it uses a constrained document shape that can be validated and transformed predictably.

## 4.2 What The Pipeline Does

The ETL slice implements five practical operations:

1. detect and parse YAML front matter
2. split the document body into chunkable sections
3. assign a deterministic identifier to each section
4. emit normalized chunk records
5. optionally emit a graph-oriented projection derived from those records

The first four operations are the core ETL path. The graph projection is a downstream convenience layer.

## 4.3 Parsing Rules

The parsing behavior is defined by the implementation rather than by editorial convention, so it is worth stating it exactly.

### 4.3.1 Front Matter Detection

The function `split_front_matter()` treats a document as having front matter only if the file begins with a leading `---` block. In implementation terms, the parser matches the document against a regular expression anchored to the start of the file:

```python
^---\n(.*?)\n---\n?(.*)$
```

That detail matters because it creates several current rules:

- front matter must begin on the first line of the file
- the closing delimiter must also be `---`
- any blank lines or content before the opening delimiter prevent front matter detection
- content without matching front matter is still valid and is treated as body-only Markdown

### 4.3.2 Front Matter Shape

Once detected, front matter is parsed with `yaml.safe_load()`. The parsed result must be a mapping. Scalar values or top-level lists are rejected.

That means the following is valid:

```yaml
---
title: Knowledge Handbook
slug: knowledge-handbook
author: Final State Press
tags:
  - etl
  - graph
---
```

And the following is invalid because the top-level YAML value is not a mapping:

```yaml
---
- bad
- front
- matter
---
```

### 4.3.3 Body Chunking

The body is chunked by the regular expression `(?=^##\s)` in multiline mode. This creates a strict rule: only level-two headings begin a new chunk. Lower or higher heading levels remain inside the current chunk unless they themselves match `## `.

The current consequences are:

- `## Section` starts a new chunk
- `### Subsection` does not start a new chunk
- prose before the first `##` becomes an `Intro` chunk
- an empty body yields no chunk records

These are not generic Markdown semantics. They are the repository's current normalization rules.

## 4.4 Worked Example

Consider the following source document:

```md
---
title: Knowledge Handbook
slug: knowledge-handbook
author: Final State Press
tags:
  - etl
  - graph
---

This preface explains the scope of the document.

## Normalization Boundary

The normalization boundary converts authored Markdown into stable records.

### Internal Note

This subsection remains inside the current chunk because only level-two headings split the body.

## Failure Modes

Malformed front matter should fail before publication.
```

The current implementation emits three chunks:

1. an `Intro` chunk for the preface
2. a `Normalization Boundary` chunk
3. a `Failure Modes` chunk

The first two chunk identifiers are:

- `knowledge-handbook-001-intro`
- `knowledge-handbook-002-normalization-boundary`

The identifier format is deterministic:

```text
{slugified source stem}-{three-digit order}-{slugified heading}
```

That behavior comes directly from `build_chunk_id()` and the `slugify()` helper in `src/oks/etl.py`.

## 4.5 Normalized Record Shape

Each emitted chunk has the same record contract.

| Field | Meaning |
| --- | --- |
| `id` | Deterministic chunk identifier |
| `heading` | Chunk heading, or `Intro` for pre-heading content |
| `content` | The raw Markdown content for the chunk |
| `order` | One-based chunk order within the source document |
| `source_file` | File name of the originating document |
| `source_path` | Relative path used at extraction time |
| `document_title` | Title from front matter, or a filename-derived fallback |
| `document_slug` | Slug from front matter, or a slugified filename fallback |
| `metadata` | The parsed front matter mapping |

A real record from the repository currently looks like this:

```json
{
  "id": "01-introduction-001-intro",
  "heading": "Intro",
  "content": "# 1. Introduction",
  "order": 1,
  "source_file": "01_introduction.md",
  "source_path": "content/01_introduction.md",
  "document_title": "Introduction",
  "document_slug": "01_introduction",
  "metadata": {
    "title": "Introduction",
    "slug": "01_introduction"
  }
}
```

Two details are easy to miss:

- the first chunk in many files is `Intro` because the chapter title line appears before the first `##`
- the `metadata` field remains unflattened, which preserves source information for later consumers

## 4.6 Corpus Traversal Rules

The CLI accepts either a single Markdown file or a directory. Directory traversal is intentionally shallow: `collect_markdown_files()` currently uses `glob("*.md")`, not recursive discovery.

This means:

- `python -m oks.etl content --output build/chunks.json` processes top-level Markdown files in `content/`
- nested notebook or asset directories are ignored by the ETL corpus build
- passing a non-Markdown file raises a `ValueError`
- passing a missing path raises `FileNotFoundError`

For a first implementation, these constraints are useful because they make corpus behavior obvious.

## 4.7 Command-Line Workflow

Run the ETL pipeline over the book content:

```bash
python -m oks.etl content --output build/chunks.json
```

To emit a graph-oriented projection at the same time:

```bash
python -m oks.etl content \
  --output build/chunks.json \
  --graph-output build/graph.json
```

The CLI writes JSON with sorted keys and stable indentation. That is a small implementation detail, but it matters operationally because it makes generated artifacts easier to diff and inspect.

## 4.8 Failure Modes And Edge Cases

The implementation is simple enough that its edge cases should be stated explicitly.

- If front matter parses to a non-mapping type, extraction fails immediately.
- If the document has no body after front matter, no chunk records are emitted.
- If the document contains no level-two headings, the entire body becomes a single `Intro` chunk.
- If the document contains level-three or deeper headings, they remain inside the current chunk.
- If `title` or `slug` is missing from front matter, the implementation derives a fallback from the file stem.

These are not merely quirks. They define the current record contract.

## 4.9 Why This Boundary Matters

The normalized chunk record is the first representation in the repository that is genuinely suitable for automation. It is stable enough to be:

- tested in isolation
- projected into a graph
- inspected as JSON
- used as input to publication or indexing
- extended later with stricter schema validation

This boundary matters more than its size suggests. In the repository, it is the point where the manuscript stops describing a target system and starts describing one that exists.

## 4.10 Current Scope And Deliberate Omissions

The current implementation does not yet provide:

- Schema CRUD
- Author UI
- API endpoints
- Embedding generation
- Database persistence

Those capabilities remain part of the broader roadmap. The discipline of the current slice is that it only claims what it can execute and test.
