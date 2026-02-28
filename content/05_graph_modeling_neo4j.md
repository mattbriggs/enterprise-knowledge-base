---
title: "Graph Modeling (Neo4j)"
slug: 05_graph_modeling_neo4j
---

# 5. Graph Modeling (Neo4j)

Chapter 5 shows how normalized records are projected into a small property graph model. The goal is not to build a complete enterprise ontology. It is to show how a disciplined ETL boundary can produce graph-ready entities and relationships without turning the graph into an ambiguous second source of truth.

The current implementation is intentionally narrow. It uses a small number of labels and relationship types so that the graph layer remains inspectable, queryable, and subordinate to the content normalization boundary described in Chapter 4.

## 5.1 Why A Property Graph Here

The graph layer exists for a specific class of questions:

- which chunks belong to which source document
- which topics are associated with which chunks
- which author metadata is attached to which content
- which schema contract a chunk was validated against

A property graph fits because it models entities as nodes, typed connections as relationships, and descriptive metadata as properties on either. For this repository, that is enough to support relationship-aware traversal and query design without introducing a more complex ontology stack.

The architectural point is simple: the graph is **derived**. It is not where authoring begins.

## 5.2 The Current Node Model

The graph projection emitted by `build_graph_projection()` currently produces five logical node types:

- `Chapter`
- `ContentChunk`
- `Schema`
- `Topic`
- `Author`

Each one corresponds to a different modeling concern:

- `Chapter` identifies the source document boundary
- `ContentChunk` represents the normalized unit of content
- `Schema` names the contract under which the chunk was produced
- `Topic` represents optional front matter tags or topics
- `Author` captures author metadata when present

This is not yet a domain ontology. It is a projection over a content corpus.

## 5.3 Relationship Model

The current relationship set is small and explicit:

- `(:Chapter)-[:CONTAINS]->(:ContentChunk)`
- `(:ContentChunk)-[:TAGGED_WITH]->(:Topic)`
- `(:Author)-[:WROTE]->(:ContentChunk)`
- `(:ContentChunk)-[:VALIDATED_BY]->(:Schema)`

These relationships are sufficient for the current repository because they encode provenance, grouping, and lightweight categorization. They also reflect a useful rule of thumb for graph modeling: start with the relationships you know you need to query, not with an abstract taxonomy of everything that might someday matter.

## 5.4 Constraints And Identity

The seed Cypher file in `graphs/schema.cypher` already creates uniqueness constraints for the current labels:

```cypher
CREATE CONSTRAINT chapter_id IF NOT EXISTS
FOR (c:Chapter) REQUIRE c.slug IS UNIQUE;

CREATE CONSTRAINT chunk_id IF NOT EXISTS
FOR (cc:ContentChunk) REQUIRE cc.id IS UNIQUE;
```

The same pattern is used for `Author`, `Topic`, and `Schema`.

This is an important design choice. Neo4j uniqueness constraints are not decorative; they protect identity and support indexed lookup on key properties. They matter even more when loaders evolve from toy examples into repeatable ingestion jobs.

A related point follows from Neo4j's `MERGE` semantics: `MERGE` is the correct clause for idempotent graph loading, but `MERGE` alone is not enough to guarantee uniqueness under concurrent writes. The uniqueness guarantee comes from the combination of `MERGE` and property uniqueness constraints.

## 5.5 Mapping From Normalized Records To Graph Entities

The graph projection is built from the chunk corpus, not from raw Markdown. That means the mapping rules are explicit.

Given a normalized chunk record such as:

```json
{
  "id": "knowledge-handbook-002-normalization-boundary",
  "heading": "Normalization Boundary",
  "order": 2,
  "source_file": "knowledge_handbook.md",
  "document_title": "Knowledge Handbook",
  "document_slug": "knowledge-handbook",
  "metadata": {
    "author": "Final State Press",
    "tags": ["etl", "graph"]
  }
}
```

the graph projection yields:

- one `Chapter` node keyed by `document_slug`
- one `ContentChunk` node keyed by `id`
- one `Schema` node, currently `MarkdownChunk`
- one `Author` node keyed by author name
- one `Topic` node for each normalized tag

The relationship records emitted by the projection then bind these nodes together. A real projection excerpt from the repository looks like:

```json
{
  "chapters": [
    {
      "slug": "01_introduction",
      "title": "Introduction",
      "source_file": "01_introduction.md"
    }
  ],
  "schemas": [
    {
      "name": "MarkdownChunk",
      "version": "1.0"
    }
  ],
  "relationships": {
    "contains": [
      {
        "chapter_slug": "01_introduction",
        "chunk_id": "01-introduction-001-intro",
        "order": 1
      }
    ]
  }
}
```

The structure is deliberately straightforward. It is designed to make the loader logic obvious.

## 5.6 A Production-Style Load Pattern

The repository's `graphs/schema.cypher` file currently uses `CREATE` statements to seed demo data. That is acceptable for a pedagogical seed file, but it is not the right pattern for repeatable loading.

A more robust loader would use `MERGE` keyed by the constrained identity properties:

```cypher
MERGE (c:Chapter {slug: $document_slug})
  ON CREATE SET
    c.title = $document_title,
    c.source_file = $source_file

MERGE (cc:ContentChunk {id: $id})
  SET
    cc.heading = $heading,
    cc.content = $content,
    cc.order = $order,
    cc.source_file = $source_file

MERGE (c)-[:CONTAINS {order: $order}]->(cc)

MERGE (s:Schema {name: 'MarkdownChunk'})
  ON CREATE SET s.version = '1.0'

MERGE (cc)-[:VALIDATED_BY]->(s)
```

Topics and authors follow the same pattern:

```cypher
MERGE (t:Topic {name: $topic})
MERGE (cc)-[:TAGGED_WITH]->(t)

MERGE (a:Author {name: $author})
MERGE (a)-[:WROTE]->(cc)
```

This pattern gives the loader four desirable properties:

- repeated runs are idempotent
- node identity is explicit
- relationships are created from normalized records rather than inferred ad hoc
- the graph remains rebuildable from source

## 5.7 Query Patterns

The current graph is small, but it already supports useful query patterns.

### 5.7.1 List Chunks In Chapter Order

```cypher
MATCH (c:Chapter)-[:CONTAINS]->(cc:ContentChunk)
RETURN c.title AS chapter, cc.heading AS heading, cc.id AS chunk_id
ORDER BY c.slug, cc.order
```

This query is the graph equivalent of traversing the normalized corpus by document and section order.

### 5.7.2 List Topics In Use

```cypher
MATCH (cc:ContentChunk)-[:TAGGED_WITH]->(t:Topic)
RETURN DISTINCT t.name AS topic
ORDER BY topic
```

This is useful for verifying that topic normalization behaves as expected.

### 5.7.3 Find Author-Tagged Chunks

```cypher
MATCH (a:Author)-[:WROTE]->(cc:ContentChunk)-[:TAGGED_WITH]->(t:Topic)
RETURN a.name AS author, cc.heading AS heading, collect(t.name) AS topics
ORDER BY author, heading
```

Even in a small graph, this shows why the graph layer is useful: it composes multiple relationships without forcing the caller to reconstruct joins manually.

## 5.8 Modeling Choices And Current Limits

The graph model is useful precisely because it is constrained.

The current limitations are:

- `Chapter` is a source-document boundary, not a semantic chapter hierarchy
- `Topic` nodes come only from front matter tags or topics, not from NLP extraction
- `Schema` is currently a single coarse node, `MarkdownChunk`
- there is no explicit ontology, synonym model, or cross-document citation graph
- the current demo Cypher file uses pedagogical seed data rather than a true loader

These are acceptable limits for a first projection. A graph model becomes more valuable when it grows from concrete query needs, not when it starts as a speculative taxonomy.

## 5.9 Why This Graph Layer Matters

The graph layer matters because it proves that the ETL boundary is rich enough to support a second representation without losing discipline. That is the real lesson of the chapter.

The graph is not an alternative to content modeling. It is evidence that the content model is structured enough to support relationship-aware systems downstream.
