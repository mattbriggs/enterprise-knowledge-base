---
title: "Design Criteria"
slug: 03_requirements
---

# 3. Design Criteria

The manuscript no longer needs a long-form requirement ledger in its main narrative. What it does need is a clear set of design criteria: standards the system should satisfy, reasons those standards matter, and an evidence model for deciding whether a given capability is real, partial, or still aspirational.[^c3-jsonschema][^c3-asvs][^c3-otel]

The criteria below preserve rigor without turning the book into a traceability catalog. Each criterion describes a system property, its architectural purpose, and the sort of evidence that would support it.

## 3.1 How To Read These Criteria

The criteria fall into three categories.

- **implemented criteria** describe behavior the repository can already demonstrate
- **near-term criteria** follow directly from the current implementation path
- **target-platform criteria** describe what a fuller OKS deployment should eventually satisfy

Keeping those categories visible prevents the manuscript from overstating what the repository actually does.

## 3.2 Contract And Governance Criteria

### DC-01 Source Documents Must Conform To An Explicit Authoring Contract

The system must define what counts as a valid source document. In practice that means explicit rules for front matter, body structure, and identifier behavior. Without an authoring contract, every later stage becomes less reliable.

The current repository demonstrates only a narrow version of this criterion: Markdown plus optional YAML front matter and heading-based chunking. A fuller platform would likely extend that contract with explicit schema validation over metadata and content types.

### DC-02 Validation Must Occur Before Derived Output Is Trusted

Parsing, metadata checks, and structural validation must happen before publication, graph loading, or retrieval indexing. Invalid input should fail early rather than contaminate multiple derived stores.

This criterion is partly a correctness concern and partly a cost concern. The later a structural failure is discovered, the more expensive it becomes to explain and repair.

### DC-03 Content Rules Must Be Distinct From Rendering Rules

The system should distinguish content validity from presentation choices. A document can be structurally valid even if a template changes. That separation reduces coupling between authoring, normalization, and publication.

### DC-04 Identity Must Survive Across Derived Forms

Normalized records, graph projections, and publication artifacts must preserve stable identifiers. Without stable identity, provenance, synchronization, deduplication, and query joins all become fragile.

## 3.3 Transformation Criteria

### DC-05 Normalization Must Produce A Deterministic Intermediate Form

The system should transform source documents into a machine-friendly representation that can be regenerated predictably. Deterministic outputs are the basis for trustworthy testing, rebuilds, and downstream consumers.

### DC-06 The Core Transformation Boundary Must Be Testable In Isolation

Normalization logic should be verifiable without a live graph database, search cluster, or publication service. Early stages should stay lightweight enough to run in local development and continuous integration.

This is one of the strongest criteria already satisfied by the repository.

### DC-07 Derived Representations Must Remain Downstream Consumers

Graphs, indexes, and publication artifacts should be derived from normalized records rather than maintained as independently edited peers. This preserves a clean source-of-truth policy.

### DC-08 The Pipeline Must Support Rebuilds From Governed Inputs

A clean rebuild from source documents should regenerate normalized records and downstream artifacts. Rebuildability is necessary for recovery, audit, and long-lived maintainability.

## 3.4 Storage, Retrieval, And Publication Criteria

### DC-09 Storage Must Preserve Both Authored Meaning And Retrieval Utility

The system should support an authored representation that remains legible to humans and a derived representation that supports automation and retrieval. One storage form should not be forced to do every job badly.

### DC-10 Graph Projection Must Encode Concrete Query Value

Graph structures should exist because they support real traversals: provenance, membership, taxonomy alignment, or relationship-aware lookup. The graph should not become a vague substitute for content modeling.

### DC-11 Retrieval Must Be Designed As A Consequence Of Content Modeling

Lexical search, graph traversal, filtering, and later semantic retrieval all depend on the shape of the content that feeds them. Retrieval quality begins in the content contract, not in the ranking layer alone.

### DC-12 Publication Must Produce Both Reader-Facing And Machine-Readable Outputs

At minimum, publication should generate coherent human-facing artifacts. A fuller platform should also support machine-readable publication through governed metadata, structured identifiers, and explicit vocabulary mappings such as JSON-LD.[^c3-jsonld]

## 3.5 Validation, Operations, And Safety Criteria

### DC-13 Validation Must Be Layered

The system should distinguish syntax validation, schema validation, business-rule validation, corpus-level checks, and operational validation. These layers answer different questions and should not be collapsed into a single pass.

### DC-14 Operational Evidence Must Be Designed In Early

Tests, logs, metrics, traces, and build outputs should make it possible to explain what the system did and why. In the current repository, tests and build behavior are the first form of that evidence. In a fuller platform, OpenTelemetry-style instrumentation would extend it.

### DC-15 Security And Access Control Must Be Architectural Constraints

Security cannot be bolted on after interfaces and data flow are already fixed. Even where the repository does not yet implement production controls, the architecture should preserve a path to verification standards such as OWASP ASVS without redesigning the whole system.

### DC-16 Performance Claims Must Be Paired With A Verification Method

Latency, throughput, and scale claims are only useful when paired with workload assumptions and a measurement plan. Unsupported performance promises should remain explicit design targets rather than implied facts.

## 3.6 Criteria Already Demonstrated By The Repository

The repository already demonstrates a limited but important subset of the full criteria:

- an explicit authoring contract for the current Markdown corpus
- deterministic normalization into chunk records
- stable identifiers for derived records
- a graph-oriented derived projection
- isolated tests around the transformation boundary
- publication and build behavior driven from version-controlled source

These are not the final platform. They are the part of the platform that can already be executed, tested, and explained.

## 3.7 Criteria Matrix

The matrix below is a compact planning and review aid. It is denser than the surrounding prose by design.

| ID | Criterion | Why It Matters | Typical Evidence | Current State | External Anchor |
| --- | --- | --- | --- | --- | --- |
| DC-01 | explicit authoring contract | prevents ambiguous input | fixture-based parsing tests and source examples | Partial | CommonMark, YAML |
| DC-02 | validation before derived trust | stops bad input from spreading | parser failures, validation tests, build gates | Partial | JSON Schema |
| DC-03 | content rules separate from rendering rules | reduces coupling | template-independent examples and docs review | Planned | publication architecture |
| DC-04 | stable identity across forms | enables provenance and synchronization | deterministic ID tests across rebuilds | Implemented in ETL slice | repository ID contract |
| DC-05 | deterministic intermediate form | creates a trustworthy hinge layer | repeatable chunk and graph outputs | Implemented in ETL slice | repository ETL behavior |
| DC-06 | isolated transformation tests | keeps the core verifiable | unit tests without external services | Implemented in ETL slice | repository test suite |
| DC-07 | derived forms stay downstream | preserves source-of-truth discipline | loader design review and storage boundaries | Partial | graph and publication design |
| DC-08 | rebuilds from governed inputs | supports recovery and audit | clean rebuild of chunk and graph artifacts | Partial | build discipline |
| DC-09 | storage serves both authorship and retrieval | avoids one-store compromises | storage contract documentation | Partial | storage architecture |
| DC-10 | graph projection encodes real query value | keeps graph modeling precise | Cypher examples and loader rules | Partial | Neo4j data modeling |
| DC-11 | retrieval follows content modeling | improves ranking and explainability | retrieval design tied to chunk and metadata contracts | Planned | information retrieval practice |
| DC-12 | publication supports reader and machine outputs | broadens delivery surfaces responsibly | strict docs build and structured metadata plan | Partial | JSON-LD |
| DC-13 | validation is layered | prevents one-pass overreach | separate schema, corpus, and loader checks | Partial | JSON Schema |
| DC-14 | operational evidence exists | supports debugging and operations | tests, logs, metrics, traces | Planned | OpenTelemetry |
| DC-15 | security is architectural | reduces redesign risk | interface and control review | Planned | OWASP ASVS |
| DC-16 | performance claims are measurable | keeps scaling claims honest | workload model plus benchmark method | Planned | performance engineering practice |

## 3.8 How These Criteria Guide The Rewrite

These criteria are not a detached governance appendix. They are the rule set the rest of the book should satisfy.

- Chapter 4 explains the current authoring and normalization contract.
- Chapter 5 shows how a graph projection can remain derived rather than authoritative.
- Chapter 6 shows why retrieval begins in chunk and metadata design.
- Chapter 7 shows how the validation layers should be separated.
- Chapter 8 shows how publication turns the earlier decisions into observable artifacts.

If a later chapter makes a claim that these criteria would reject, the chapter should be revised rather than the criterion weakened.

## 3.9 Reading Notes

- **JSON Schema:** helpful for explicit content contracts and schema validation.
- **OWASP ASVS:** useful for turning security from an aspiration into a verification target.
- **OpenTelemetry Specification:** useful for operational evidence and observability design.
- **JSON-LD 1.1:** useful for machine-readable publication criteria.

[^c3-jsonschema]: JSON Schema, *What is JSON Schema?*: https://json-schema.org/overview/what-is-jsonschema
[^c3-asvs]: OWASP Foundation, *Application Security Verification Standard*: https://owasp.org/www-project-application-security-verification-standard/
[^c3-otel]: OpenTelemetry, *OpenTelemetry Specification*: https://opentelemetry.io/docs/specs/otel/
[^c3-jsonld]: W3C, *JSON-LD 1.1*: https://www.w3.org/TR/json-ld11/
