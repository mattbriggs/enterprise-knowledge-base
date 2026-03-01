---
title: "Graph Modeling (Neo4j)"
slug: 05_graph_modeling_neo4j
---

# 5. Graph Modeling (Neo4j)

Chapter 5 shows how normalized records are projected into a small property graph model. The goal is not to build a complete enterprise ontology. The goal is to demonstrate a disciplined graph boundary: one that is derived from stable content records, designed around actual queries, and constrained enough to remain inspectable.

That distinction matters because graph work is easy to overstate. A graph does not become useful merely because it contains nodes and edges. It becomes useful when identity is stable, relationships answer real questions, and the graph does not compete with the content model that produced it.

## 5.1 Why Use A Property Graph Here

The repository uses a property-graph projection because the present query class is concrete and local:

- which chunks belong to which source document
- which topics are associated with which chunks
- which author metadata is attached to which content
- which schema contract a chunk was validated against

For those questions, a property graph is a practical fit. Nodes represent entities, relationships represent traversable links, and properties preserve the small amount of attached metadata needed for loading and query behavior.

The important boundary is this: the graph is derived. Authoring does not begin in Neo4j. The graph exists because the normalized records are already structured enough to support a second representation.

## 5.2 Why The Model Is Not Ontology-First

The present graph model is not an ontology stack, and it should not pretend to be one. It does not attempt open-world reasoning, description-logic inference, or a formal concept hierarchy beyond what the current metadata can justify.

That restraint is useful. In early-stage knowledge systems, an ontology-first approach often produces broad concept models that are weakly connected to actual content operations. The repository takes the opposite stance:

- start with content records that exist
- project only the entities and relationships those records justify
- expand the graph when concrete query needs require it

This is consistent with a query-first modeling approach. Graph shape should follow the questions the system intends to answer.[^c5-modeling]

## 5.3 Current Node Model

`build_graph_projection()` emits five logical node types:

- `Chapter`
- `ContentChunk`
- `Schema`
- `Topic`
- `Author`

Each node type represents a different concern:

- `Chapter` captures the source-document boundary
- `ContentChunk` represents the normalized unit of content
- `Schema` names the contract under which the record was produced
- `Topic` expresses lightweight topical classification from metadata
- `Author` preserves optional authorship metadata

This is still a content projection, not a domain ontology. The model is intentionally small because its job is to stay legible while proving that the normalized corpus supports graph-oriented work.

## 5.4 Current Relationship Model

The present relationship set is also deliberately small:

- `(:Chapter)-[:CONTAINS]->(:ContentChunk)`
- `(:ContentChunk)-[:TAGGED_WITH]->(:Topic)`
- `(:Author)-[:WROTE]->(:ContentChunk)`
- `(:ContentChunk)-[:VALIDATED_BY]->(:Schema)`

These relationships are sufficient to demonstrate:

- provenance from source document to chunk
- grouping of chunks under source boundaries
- metadata-driven topic traversal
- attachment of chunk records to the schema contract that produced them

This is a good early graph rule: add relationships because they support known traversals, not because they sound semantically rich.

## 5.5 Identity And Constraints

Graph usefulness depends on identity discipline. The repository already includes uniqueness constraints in `graphs/schema.cypher`:

```cypher
CREATE CONSTRAINT chapter_id IF NOT EXISTS
FOR (c:Chapter) REQUIRE c.slug IS UNIQUE;

CREATE CONSTRAINT chunk_id IF NOT EXISTS
FOR (cc:ContentChunk) REQUIRE cc.id IS UNIQUE;
```

The same pattern is used for `Author`, `Topic`, and `Schema`.

These constraints matter for two reasons.[^c5-constraints]

First, they protect identity at the database level rather than leaving uniqueness to application convention. Second, they support efficient keyed lookup, which is what a loader will need once the graph moves beyond seed data.

## 5.6 `MERGE` And Idempotent Loading

Neo4j's `MERGE` clause is the right basis for repeatable loading, but it is not enough by itself.[^c5-merge] True idempotence depends on the combination of:

- stable application-side identifiers
- database-side uniqueness constraints
- `MERGE` keyed on those constrained properties

That is why a production-oriented load pattern should look like this:

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
```

Topics, authors, and schema nodes follow the same pattern. The current `graphs/schema.cypher` file still uses `CREATE` for sample data because it is a seed file, not a true loader.

## 5.7 Mapping From Chunk Records To Graph Entities

The graph projection is built from normalized chunk records, not from raw Markdown. That means the mapping rules are explicit and reproducible.

Given a chunk record such as:

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

the projection yields:

- one `Chapter` node keyed by `document_slug`
- one `ContentChunk` node keyed by `id`
- one `Schema` node, currently `MarkdownChunk`
- one `Author` node keyed by author name when present
- one `Topic` node for each normalized topic or tag

The relationships emitted by `build_graph_projection()` then connect those nodes. No graph-side inference is required to reconstruct the basic model.

## 5.8 Query Patterns The Current Model Supports

The present graph is small, but it already supports useful query patterns.

### 5.8.1 Chunks In Document Order

```cypher
MATCH (c:Chapter)-[:CONTAINS]->(cc:ContentChunk)
RETURN c.title AS chapter, cc.heading AS heading, cc.id AS chunk_id
ORDER BY c.slug, cc.order
```

This reproduces the normalized corpus in graph form.

### 5.8.2 Topics In Use

```cypher
MATCH (cc:ContentChunk)-[:TAGGED_WITH]->(t:Topic)
RETURN DISTINCT t.name AS topic
ORDER BY topic
```

This is a simple but useful integrity query. It shows whether metadata normalization is behaving as expected.

### 5.8.3 Author-To-Topic Traversal

```cypher
MATCH (a:Author)-[:WROTE]->(cc:ContentChunk)-[:TAGGED_WITH]->(t:Topic)
RETURN a.name AS author, cc.heading AS heading, collect(t.name) AS topics
ORDER BY author, heading
```

This query demonstrates the main reason the graph exists at all: relationship composition is easier to express here than by reconstructing joins manually over flat JSON.

## 5.9 Current Limits

The current graph model is useful because it is bounded.

Its limits are explicit:

- `Chapter` represents a source-document boundary, not a semantic chapter hierarchy
- `Topic` nodes come only from front matter metadata, not from NLP extraction
- `Schema` is a single coarse contract node, not a full schema registry
- there is no ontology alignment, synonym management, or citation graph
- the repository does not yet ship a true Neo4j loader

These are acceptable limits for a first graph boundary. A small graph that answers real questions is more valuable than a large graph whose semantics no one can defend.

## 5.10 What A Stronger Graph Layer Would Add

The next stage of graph work should add:

- a repeatable loader that consumes normalized records directly
- integration tests against a disposable Neo4j instance
- richer schema typing for chunks and future content classes
- more explicit taxonomy or ontology links only where real query needs require them
- loader diagnostics that explain constraint failures and merge outcomes

The order matters. The graph should become more powerful because the normalized substrate becomes richer, not because the graph is asked to compensate for a weak content model.

## 5.11 Reading Notes

- **Neo4j Modeling Designs:** useful for query-first graph design and deciding when a graph actually helps.
- **Neo4j Constraints Manual:** useful for understanding why identity belongs in the database contract, not just in loader code.
- **Neo4j `MERGE` Documentation:** useful for idempotent load behavior and its limits.

[^c5-modeling]: Neo4j, *Modeling designs - Getting Started*: https://neo4j.com/docs/getting-started/data-modeling/modeling-designs/
[^c5-constraints]: Neo4j, *Create, show, and drop constraints - Cypher Manual*: https://neo4j.com/docs/cypher-manual/current/constraints/managing-constraints/
[^c5-merge]: Neo4j, *MERGE - Cypher Manual*: https://neo4j.com/docs/cypher-manual/current/clauses/merge/
