---
title: "System Model and Design Principles"
slug: 02_overall_description
---

# 2. System Model And Design Principles

Open Knowledge Systems is best understood as a governed content pipeline, not as a single application surface. The central design problem is not how to publish one more documentation site. It is how to move from human-authored documents to content that can be validated, transformed, queried, and published without losing provenance or structural discipline.

That framing matters because the platform described in this book is larger than the repository that accompanies it. The repository implements only a narrow Markdown ETL slice. The larger system model must therefore do two things at once: describe the full architectural shape of an enterprise knowledge system and keep the current implementation boundary visible.

## 2.1 Problem Frame

Most organizations already have content. What they lack is a dependable way to turn that content into a system that remains structurally consistent as it moves across authoring, automation, storage, search, graph projection, and publication.

Three failures recur:

- content is authored for readers only and becomes expensive to reuse programmatically
- metadata is attached late, inconsistently, or outside the main authoring path
- retrieval and graph features are added after publication rather than designed into the content model itself

OKS is a response to those failures. It treats a document not only as text, but as an input to validation, a source for normalized records, a candidate for graph projection, and a unit of publication.

## 2.2 Governing Contracts

The system model depends on several contracts. These contracts are not all implemented today, but they define the architecture the rest of the book assumes.

### 2.2.1 Authoring Contract

The authoring contract defines what a valid source document looks like. In the current repository that contract is intentionally small: CommonMark-style Markdown plus optional YAML front matter at the top of the file.[^c2-commonmark][^c2-yaml]

Two distinctions are important:

- Markdown provides a human-legible syntax for authored text, headings, lists, and code blocks.
- YAML front matter provides structured metadata, but it is a repository convention rather than part of the CommonMark specification itself.

That distinction prevents a common modeling mistake: confusing general Markdown syntax with the local machine contract used by a particular ETL pipeline.

### 2.2.2 Validation Contract

The validation contract defines how source content becomes trustworthy enough to feed downstream systems. In a fuller platform that contract should include explicit schemas, likely expressed in a machine-readable vocabulary such as JSON Schema, plus rule layers that cover business constraints and corpus-level checks.[^c2-jsonschema]

The repository does not implement all of that yet. It does implement the first step: parsing, structural checks, and tests over the normalization boundary.

### 2.2.3 Operational Contract

Production systems also require an operational contract. At minimum that includes:

- telemetry that explains what the system did
- security controls that preserve safe publication and safe interface behavior
- release rules that determine when content is publishable

OpenTelemetry is a useful reference point for the telemetry side of that contract. OWASP ASVS is a useful reference point for the security side.[^c2-otel][^c2-asvs] The book does not claim that the repository already satisfies those standards. It uses them to define the level of rigor a fuller system should preserve.

## 2.3 Architectural Boundary

The book describes the system boundary at two levels.

### 2.3.1 Target Platform Boundary

The target platform includes:

- schema-governed authoring and ingestion
- parsing, normalization, and layered validation
- durable storage for source and derived forms
- graph projection and graph-oriented querying
- retrieval surfaces for both humans and machines
- publication pipelines for static and machine-readable outputs
- observability, security, and operational control

### 2.3.2 Current Repository Boundary

The repository currently implements only the normalization core:

- Markdown source documents with optional YAML front matter
- heading-based chunk extraction
- deterministic chunk identifiers
- normalized JSON output
- a graph-oriented projection suitable for downstream loading
- tests that defend the transformation boundary

That narrower implementation is the evidence-bearing center of the current system. The rest of the architecture should be read as design intent unless the repository demonstrates otherwise.

## 2.4 Governing Representations

The system revolves around four representations of the same content.

### 2.4.1 Source Document

The source document is the author-facing representation. It is optimized for readability, version control, and low-friction editing. In the repository it is a Markdown file that may include front matter for metadata.

### 2.4.2 Normalized Record

The normalized record is the first machine-governed representation. It separates metadata from body content, imposes deterministic chunk boundaries, and assigns stable identifiers. This is the architectural hinge of the whole system. Every later capability depends on it.

### 2.4.3 Graph Projection

The graph projection is a relationship-oriented representation derived from normalized records. It is useful for graph traversal, relationship-aware retrieval, and downstream graph loading. It is not the authoritative representation for content editing.

### 2.4.4 Publication Artifact

The publication artifact is the human-facing or machine-consumable output produced from governed content. In this repository that includes the MkDocs site and export artifacts such as EPUB and PDF. In a fuller platform it could also include JSON-LD-enriched pages, APIs, or syndication feeds.

## 2.5 Transformation Order

The system depends on a strict order of operations:

1. a source document is authored or ingested
2. the input is parsed and checked against the current authoring contract
3. the document is normalized into stable intermediate records
4. derived forms are generated for graph, retrieval, or publication use
5. artifacts are published or loaded into downstream stores
6. tests, logs, and operational evidence explain what happened

This sequence is more than a workflow. It is a dependency model. Later layers should consume earlier layers rather than reinterpret the source independently. If the graph loader, search indexer, and publisher all parse raw documents differently, the system no longer has one content contract. It has several competing ones.

## 2.6 Responsibility Boundaries

The target platform can be described as a set of cooperating responsibilities.

### 2.6.1 Authoring And Ingestion

This responsibility accepts source material and enforces the authoring contract. In the repository, the input surface is version-controlled Markdown. In a fuller platform, this layer could also include managed forms, import jobs, and API-based ingestion.

### 2.6.2 Normalization And Validation

This responsibility converts authored content into a stable machine contract. It includes parsing, metadata extraction, chunking, deterministic identifiers, and structural checks. It should remain explainable and testable in isolation.

### 2.6.3 Storage And Projection

This responsibility preserves the distinction between source-of-truth content and derived representations. Document-form storage, graph projection, and later retrieval indexes each exist for different reasons and should not be conflated.

### 2.6.4 Retrieval And Publication

This responsibility exposes governed content to readers and systems. Retrieval includes lexical, graph, or later semantic query paths. Publication includes HTML output, export artifacts, and machine-readable metadata.

### 2.6.5 Operations And Control

This responsibility makes the system defensible in production. It includes telemetry, auditability, release discipline, security boundaries, and capacity assumptions. Even where the repository implements only a small portion of this layer, the architecture should preserve a path to it.

## 2.7 Design Principles

The following principles govern the rest of the manuscript.

### 2.7.1 Normalize Before You Enrich

Graph projection, indexing, semantic tagging, and publication metadata should all depend on a stable intermediate representation. Without that boundary, every downstream consumer invents its own interpretation of the source.

### 2.7.2 Keep The Source Of Truth Explicit

The authored document, the normalized record, and the graph projection are not interchangeable. The system should always be able to answer the question, "Where is this fact corrected?"

### 2.7.3 Prefer Deterministic Early Stages

Parsing, chunking, identity assignment, and first-pass validation should be reproducible. A change in output should be traceable to a change in source or rule set.

### 2.7.4 Model For Queries You Intend To Support

The graph should be designed for concrete traversals. The retrieval layer should be designed for concrete query classes. Abstract ontology work or search claims that are not tied to actual query behavior usually weaken the system rather than strengthen it.

### 2.7.5 Treat Publication As A Technical Boundary

Publication is not just rendering. It is where navigation, identifiers, metadata, and release discipline become visible. Weak system boundaries surface quickly in the publication layer.

### 2.7.6 Keep Claims Proportional To Evidence

Implemented behavior, design targets, and technical rationale are not the same thing. The manuscript should mark those categories clearly, and the platform should be discussed with the same discipline.

## 2.8 Cross-Cutting Constraints

Several constraints shape the architecture even when they are only partially implemented in the repository.

### 2.8.1 Identity

Identifiers must survive normalization, projection, publication, and retrieval. Stable identity is what allows rebuilds, provenance tracking, and graph loading to remain coherent.

### 2.8.2 Observability

The system should emit enough evidence to explain parsing failures, build failures, validation failures, and publication state. Test results are part of that evidence. In a production environment, logs, metrics, and traces would extend it.

### 2.8.3 Security

A fuller platform would need to validate user input, protect administrative actions, preserve audit history, and expose interfaces that meet a production verification standard. That work sits mostly outside the current repository, but the architecture should not make it harder later.

### 2.8.4 Rebuildability

Derived artifacts should be regenerable from governed sources or governed intermediates. Rebuildability is the system's defense against drift between stores.

## 2.9 Non-Goals

Several goals are intentionally outside the current implementation boundary:

- a full authoring UI
- a production API surface
- live identity integration
- vector-search infrastructure
- ontology management beyond the present graph projection
- deployment assets for a production runtime

These are legitimate design targets. They are not part of the repository's present evidence.

## 2.10 What This Model Changes For The Rest Of The Book

The rest of the manuscript should now be read through this model.

- Chapter 3 states the design criteria that follow from these boundaries.
- Chapter 4 explains the implemented authoring and normalization contract.
- Chapters 5 and 6 describe how derived graph and retrieval forms depend on normalized records.
- Chapters 7 and 8 explain how validation and publication make the architecture observable.

If a later chapter blurs the line between source and derived forms, or between implemented behavior and target architecture, the correct fix is to revise the chapter rather than to widen the claim.

## 2.11 Reading Notes

- **CommonMark Specification:** useful for separating general Markdown behavior from repository-local parsing rules.
- **YAML 1.2.2 Specification:** useful for understanding why front matter is treated as structured mapping data.
- **JSON Schema:** useful for the next validation layer after parsing and structural checks.
- **OpenTelemetry Specification:** useful for thinking about observability as a system contract.
- **OWASP ASVS:** useful for defining what production-grade verification means once the platform exposes broader interfaces.

[^c2-commonmark]: CommonMark, *CommonMark Spec*: https://spec.commonmark.org/
[^c2-yaml]: YAML Language Development Team, *YAML Ain't Markup Language (YAML) version 1.2.2*: https://yaml.org/spec/1.2.2/
[^c2-jsonschema]: JSON Schema, *What is JSON Schema?*: https://json-schema.org/overview/what-is-jsonschema
[^c2-otel]: OpenTelemetry, *OpenTelemetry Specification*: https://opentelemetry.io/docs/specs/otel/
[^c2-asvs]: OWASP Foundation, *Application Security Verification Standard*: https://owasp.org/www-project-application-security-verification-standard/
