// Delete all existing data (only run in dev/test)
MATCH (n) DETACH DELETE n;

// Define node labels with key properties
CREATE CONSTRAINT chapter_id IF NOT EXISTS
FOR (c:Chapter) REQUIRE c.slug IS UNIQUE;

CREATE CONSTRAINT chunk_id IF NOT EXISTS
FOR (cc:ContentChunk) REQUIRE cc.id IS UNIQUE;

CREATE CONSTRAINT author_id IF NOT EXISTS
FOR (a:Author) REQUIRE a.name IS UNIQUE;

CREATE CONSTRAINT topic_id IF NOT EXISTS
FOR (t:Topic) REQUIRE t.name IS UNIQUE;

CREATE CONSTRAINT schema_id IF NOT EXISTS
FOR (s:Schema) REQUIRE s.name IS UNIQUE;

// Sample nodes
CREATE (c1:Chapter {
  title: "Authoring & ETL",
  slug: "02-authoring-etl",
  order: 2
});

CREATE (cc1:ContentChunk {
  id: "chunk-0201",
  heading: "ETL Pipeline",
  content: "Extract, transform, and load structured content from Markdown into a knowledge base.",
  order: 1
});

CREATE (cc2:ContentChunk {
  id: "chunk-0202",
  heading: "Markdown Conventions",
  content: "Use front matter metadata and semantic headings.",
  order: 2
});

CREATE (a1:Author {
  name: "Final State Press"
});

CREATE (t1:Topic { name: "ETL" });
CREATE (t2:Topic { name: "Markdown" });
CREATE (s1:Schema { name: "ContentChunk", version: "1.0" });

// Relationships
CREATE (c1)-[:CONTAINS]->(cc1);
CREATE (c1)-[:CONTAINS]->(cc2);

CREATE (a1)-[:WROTE]->(cc1);
CREATE (a1)-[:WROTE]->(cc2);

CREATE (cc1)-[:TAGGED_WITH]->(t1);
CREATE (cc2)-[:TAGGED_WITH]->(t2);

CREATE (cc1)-[:VALIDATED_BY]->(s1);
CREATE (cc2)-[:VALIDATED_BY]->(s1);