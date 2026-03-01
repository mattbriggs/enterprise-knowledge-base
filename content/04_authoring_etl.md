---
title: "Authoring & ETL"
slug: 04_authoring_etl
---

# 4. Authoring & ETL

Chapter 4 anchors the manuscript in the first implemented boundary that is both real and central to the larger system design. It explains how author-facing Markdown becomes machine-friendly records, which rules govern that transformation, and where the implementation draws hard boundaries.

The technical point is straightforward. Markdown is a usable authoring surface, but it is not by itself a stable machine contract. The ETL layer in `src/oks/etl.py` exists to turn authored documents into deterministic records that later systems can trust.

## 4.1 The Authoring Boundary

The current authoring contract is intentionally small:[^c4-commonmark][^c4-yaml]

- each source document is a Markdown file
- an optional YAML front matter block may appear at the top of the file
- level-two headings define chunk boundaries
- each chunk inherits document-level metadata and provenance

This contract is narrower than the full CommonMark syntax and narrower than a production content model. That is deliberate. A first implementation benefits more from explicit, stable behavior than from flexibility.

Two distinctions matter.

First, Markdown is the author-facing syntax, not the machine-facing storage contract. Second, front matter is a local repository convention layered on top of Markdown rather than a feature of CommonMark itself.

## 4.2 What The ETL Slice Does

The ETL slice implements five practical operations:

1. detect and parse YAML front matter
2. separate metadata from the Markdown body
3. split the body into chunks at level-two headings
4. assign deterministic identifiers to those chunks
5. emit normalized JSON records and, optionally, a graph-oriented projection

The first four steps define the core machine boundary. The graph projection is a consumer of that boundary.

## 4.3 Parsing Model

The parsing behavior is defined by code rather than by editorial intention, so the rules should be stated exactly.

### 4.3.1 Front Matter Detection

`split_front_matter()` treats a document as having front matter only if the file begins with a `---` block at byte zero. The implementation uses a regular expression anchored to the start of the document:

```python
^---\n(.*?)\n---\n?(.*)$
```

That produces several concrete rules:

- front matter must start on the first line
- the closing delimiter must also be `---`
- blank lines before the opening delimiter suppress front matter detection
- documents without front matter remain valid and are treated as body-only Markdown

This is not a universal front matter standard. It is the repository's current parsing contract.

### 4.3.2 Front Matter Shape

Once front matter is detected, `parse_front_matter()` calls `yaml.safe_load()` and requires the parsed value to be a mapping.

That means this shape is valid:

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

This shape is invalid because the top-level value is a list:

```yaml
---
- invalid
- metadata
---
```

The choice to require a mapping is a small but important contract. Metadata must behave like keyed fields, not like an arbitrary YAML document.

### 4.3.3 Body Chunking

`chunk_markdown_by_heading()` splits the body with the expression `(?=^##\s)` in multiline mode. In practical terms, only level-two ATX headings start a new chunk.

That produces the following behavior:

- `## Section` starts a new chunk
- `### Subsection` stays inside the current chunk
- prose before the first `##` becomes an `Intro` chunk
- an empty body yields no chunks

Again, these are repository-local normalization rules. They are not a claim about how all Markdown should be processed.

## 4.4 Deterministic Identity

The repository's first durable guarantee is not schema richness. It is deterministic identity.

`build_chunk_id()` constructs identifiers in this format:

```text
{slugified source stem}-{three-digit order}-{slugified heading}
```

The `slugify()` helper lowercases the text, replaces non-alphanumeric runs with `-`, trims leading and trailing separators, and falls back to `item` if nothing remains. That yields predictable identifiers such as:

- `01-introduction-001-intro`
- `knowledge-handbook-002-normalization-boundary`

This matters for four reasons:

- graph loading depends on stable keys
- future retrieval layers need durable joins
- corpus-level duplicate detection becomes possible
- rebuilds remain explainable

## 4.5 Record Contract

Each emitted chunk record has the same shape.

| Field | Purpose |
| --- | --- |
| `id` | deterministic chunk identifier |
| `heading` | local section heading, or `Intro` for pre-heading content |
| `content` | raw Markdown for the chunk |
| `order` | one-based order within the source document |
| `source_file` | original filename |
| `source_path` | extraction-time path |
| `document_title` | title from metadata or fallback from filename |
| `document_slug` | slug from metadata or filename-derived fallback |
| `metadata` | parsed front matter mapping |

This structure is intentionally flat except for `metadata`. The flat fields support direct downstream use. The nested metadata preserves source detail without pretending that every front matter key has already been normalized into a schema.

## 4.6 Worked Example

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

The first two identifiers are:

- `knowledge-handbook-001-intro`
- `knowledge-handbook-002-normalization-boundary`

Those identifiers come directly from the source stem, chunk order, and heading text. No external state is required to reproduce them.

## 4.7 Corpus Traversal

The CLI accepts either a single Markdown file or a directory. Directory traversal is intentionally shallow. `collect_markdown_files()` uses `glob("*.md")`, not recursive discovery.

This means:

- `python -m oks.etl content --output build/chunks.json` processes the top-level Markdown files in `content/`
- nested notebook or asset directories are ignored
- a non-Markdown input file raises `ValueError`
- a missing path raises `FileNotFoundError`

These choices keep the first implementation easy to reason about. They also keep the book honest about what the repository does not yet support.

## 4.8 Failure Cases

The ETL slice is simple enough that its failure behavior should be explicit.

### 4.8.1 Non-Mapping Front Matter

If YAML parses successfully but does not produce a mapping, extraction fails immediately with `ValueError`.

### 4.8.2 Empty Body

If a document contains valid front matter but no body, extraction succeeds but emits no chunk records.

### 4.8.3 No Level-Two Headings

If a document contains prose but no `##` headings, the whole body becomes a single `Intro` chunk.

### 4.8.4 Missing Title Or Slug

If front matter omits `title` or `slug`, the implementation derives fallbacks from the filename.

These are not minor quirks. They define the current contract that tests and downstream consumers rely on.

## 4.9 Why This Boundary Matters

The normalized chunk record is the first representation in the repository that is stable enough to support automation. It can be:

- tested in isolation
- written to deterministic JSON
- projected into a graph
- used as the basis for future indexing
- compared across rebuilds

That is why the ETL layer matters more than its code size suggests. It is the point where the manuscript stops describing a target system and starts describing one that exists.

## 4.10 What A Stronger ETL Layer Would Add

The next-stage ETL layer would likely add:[^c4-jsonschema]

- explicit schema validation over metadata and record fields
- recursive or configurable corpus discovery
- richer content typing beyond one generic chunk schema
- more formal error classes and diagnostics
- loaders that consume normalized records without reparsing raw documents

Those are reasonable next steps. They should be built on top of the existing deterministic boundary rather than in place of it.

## 4.11 Reading Notes

- **CommonMark Specification:** useful for distinguishing general Markdown syntax from the repository's local chunking rules.
- **YAML 1.2.2 Specification:** useful for understanding why the front matter contract requires mapping-shaped metadata.
- **JSON Schema:** useful for the next step beyond the repository's current structural validation.

[^c4-commonmark]: CommonMark, *CommonMark Spec*: https://spec.commonmark.org/
[^c4-yaml]: YAML Language Development Team, *YAML Ain't Markup Language (YAML) version 1.2.2*: https://yaml.org/spec/1.2.2/
[^c4-jsonschema]: JSON Schema, *What is JSON Schema?*: https://json-schema.org/overview/what-is-jsonschema
