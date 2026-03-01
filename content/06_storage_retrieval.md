---
title: "Storage & Retrieval"
slug: 06_storage_retrieval
---

# 6. Storage & Retrieval

Chapter 6 explains how the repository stores governed content, what it treats as authoritative, and which retrieval layers follow from that choice. The main point is simple: storage is not a single database decision. It is a set of contracts over different representations of the same content.

That distinction matters because retrieval quality begins long before ranking or interface design. It begins with what the system stores, what it considers authoritative, and how much structure survives the trip from source document to machine-facing record.

## 6.1 Storage As Multiple Contracts

The repository already works with four practical content forms:

- the authored Markdown source document
- the normalized chunk record
- the graph-oriented projection
- the published artifact

These forms are not interchangeable.

### 6.1.1 Source Document

The source document is optimized for authorship, readability, and version control. It is the correct place for human edits.

### 6.1.2 Normalized Record

The normalized record is optimized for deterministic machine use. It is the first representation that can be indexed, projected, validated, or joined consistently.

### 6.1.3 Graph Projection

The graph projection is optimized for relationship-aware traversal. It preserves entities and relationships, not the full authored surface.

### 6.1.4 Publication Artifact

The publication artifact is optimized for readers and delivery surfaces. It preserves narrative presentation while depending on earlier structure and build discipline.

## 6.2 Source-Of-Truth Policy

The system already implies a source-of-truth policy even without a production database stack.

- the authored Markdown file is authoritative for human-authored content
- the normalized chunk record is authoritative for machine-facing downstream consumers
- the graph projection and published artifacts are derived outputs

This policy prevents a familiar failure mode in knowledge systems: allowing multiple derived stores to drift into pseudo-authoritative status. Once that happens, the system loses a clean answer to the question, "Where does this fact get corrected?"

The operating rule is therefore simple:

1. correct content at the source document layer
2. regenerate normalized records
3. rebuild derived forms from those records

At this stage, that rebuild discipline is more valuable than a more elaborate storage stack.

## 6.3 Current Storage Surfaces In The Repository

The repository currently stores or emits the following practical artifacts:

- `content/*.md` as the source corpus
- `build/chunks.json` as the normalized chunk corpus
- `build/graph.json` as the graph-oriented projection
- `site/` plus export artifacts as publication outputs

Only the first of these is hand-authored. The others should be treated as deterministic rebuild products.

## 6.4 The Normalized Chunk Corpus As Retrieval Substrate

The chunk corpus is the repository's clearest storage contract for later retrieval work.

| Field | Retrieval Use |
| --- | --- |
| `id` | stable join key across derived systems |
| `heading` | local semantic label for ranking or display |
| `content` | text body for indexing and rendering |
| `order` | document sequence |
| `source_file` | provenance for rebuild and debugging |
| `source_path` | extraction-time location |
| `document_title` | document-level label |
| `document_slug` | grouping key for document membership |
| `metadata` | preserved source metadata for filtering and projection |

This shape supports several later retrieval operations:

- regroup chunks by source document
- filter by metadata
- feed lexical indexes
- feed graph projection
- preserve provenance in results

The record is intentionally flat except for `metadata`. That compromise keeps the main fields easy to query while preserving unflattened source detail for later schema-aware handling.

## 6.5 Retrieval Layers And Their Boundaries

The book uses the word "retrieval" for several different behaviors. They should be separated.

### 6.5.1 Author-Facing Retrieval

Authors retrieve content by opening and editing the original Markdown files. That remains the correct path for source edits.

### 6.5.2 Lexical Retrieval

Lexical retrieval works over tokenized text and term statistics, usually through an inverted index.[^c6-index] In a fuller platform, the normalized chunk corpus would be the correct input to such an index.

This matters because lexical retrieval is sensitive to chunk shape. BM25-style ranking, for example, rewards matching terms while normalizing for document length.[^c6-bm25] If chunks become too long, term specificity weakens. If chunks become too short, context and ranking stability degrade. Chunk design is therefore not just an ETL question. It is a ranking question.

### 6.5.3 Relationship-Oriented Retrieval

Graph retrieval answers questions that are primarily about relationships:

- which document contains this chunk
- which author or topic is associated with this chunk
- which schema contract produced it

That retrieval mode depends on the graph projection, not on the raw source document.

### 6.5.4 Semantic Retrieval

Semantic or vector retrieval is not yet implemented in the repository. In a fuller system it would likely operate over normalized chunks or later content types with explicit identifiers and provenance. It should remain a downstream consumer of governed records, not a parallel parsing path. For web-facing delivery, that same discipline also supports structured outputs such as JSON-LD.[^c6-jsonld]

## 6.6 Worked Example: One Source, Several Retrieval Paths

Suppose the source corpus contains a document with:

```md
---
title: Knowledge Handbook
slug: knowledge-handbook
author: Final State Press
tags:
  - etl
  - graph
---

## Normalization Boundary

The normalization boundary converts authored Markdown into stable records.

## Failure Modes

Malformed front matter should fail before publication.
```

From that one source, the system can support several retrieval behaviors.

- author-facing retrieval opens `knowledge_handbook.md`
- machine-facing retrieval returns chunk `knowledge-handbook-001-normalization-boundary`
- graph retrieval answers which chapter contains that chunk and which topics attach to it
- a future lexical index could rank that chunk for queries about normalization or failure handling

The same content supports those behaviors only because the intermediate representation is stable.

## 6.7 Why Retrieval Begins In Content Modeling

Retrieval is often described as an interface or ranking problem. In practice it begins earlier.

The content model determines:

- what units are indexed
- what metadata can be filtered
- what identifiers can be returned in results
- which relationships can be traversed
- how publication artifacts link back to source and machine representations

This is why weak content contracts produce weak retrieval layers. No ranking function can recover structure that the content model never captured.

## 6.8 Current Limits

The repository does not yet implement:

- an inverted index
- BM25 or field-weighted ranking
- semantic vector retrieval
- API-based retrieval surfaces
- incremental graph synchronization
- hybrid ranking across lexical and semantic signals

Those omissions are important, but they are not a failure of explanation. They define the present boundary of evidence.

## 6.9 What A Stronger Retrieval Architecture Would Add

A fuller platform would likely introduce at least three explicit retrieval stores:

- a document-oriented store for governed content records
- a graph store for relationship traversal
- a lexical or hybrid index for search-oriented access

It might later add a vector index as well. The ordering still matters:

- source content remains editable at the document layer
- normalization remains the first durable machine boundary
- graph and retrieval stores remain derived consumers
- returned results should preserve stable chunk or document identifiers

The lesson is not "avoid multiple stores." It is "add multiple stores only when each has a clear contract and regeneration path."

## 6.10 Why This Chapter Matters

Storage and retrieval sit in the technical spine of the book because they make earlier choices visible. If chunks are badly shaped, retrieval suffers. If identity is weak, results cannot be joined back to provenance. If source-of-truth policy is unclear, every store starts competing with every other store.

That is why retrieval belongs in a chapter on content contracts rather than in a chapter on search tooling alone.

## 6.11 Reading Notes

- **Introduction to Information Retrieval, index construction:** useful for understanding why lexical retrieval begins with representation choices.
- **Introduction to Information Retrieval, BM25:** useful for seeing why chunk length and term distribution affect ranking quality.
- **JSON-LD 1.1:** useful for connecting retrieval-oriented structure to machine-readable publication surfaces.

[^c6-index]: Manning, Raghavan, and Schutze, *Introduction to Information Retrieval*, "Index construction": https://nlp.stanford.edu/IR-book/html/htmledition/index-construction-1.html
[^c6-bm25]: Manning, Raghavan, and Schutze, *Introduction to Information Retrieval*, "Okapi BM25: a non-binary model": https://nlp.stanford.edu/IR-book/html/htmledition/okapi-bm25-a-non-binary-model-1.html
[^c6-jsonld]: W3C, *JSON-LD 1.1*: https://www.w3.org/TR/json-ld11/
