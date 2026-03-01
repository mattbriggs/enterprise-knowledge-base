---
title: "Validation"
slug: 07_validation
---

# 7. Validation

Validation determines whether the rest of the architecture can be trusted. In a knowledge system, invalid structure does not merely produce a bad page. It contaminates normalized records, graph projections, retrieval behavior, and publication output. That is why validation should be treated as a layered assurance model rather than as a single boolean check.

The repository implements only the first part of that model, but it implements that part concretely enough to study. The sections below explain the current validation boundary, the tests that enforce it, and the additional layers a fuller platform will need.

## 7.1 Validation As Layers

The word "validation" covers several different tasks. They should be kept separate.

### 7.1.1 Syntax Validation

Syntax validation asks whether the input can be parsed at all. In the current repository this includes front matter detection and YAML parsing.

### 7.1.2 Structural Validation

Structural validation asks whether the parsed document conforms to the current transformation contract. In the repository this includes rules such as:

- front matter must parse to a mapping
- chunk records must contain required fields
- emitted identifiers must remain unique across the corpus

### 7.1.3 Schema Validation

Schema validation asks whether the content satisfies an explicit field-level contract: required properties, allowed types, enumerations, nested structure, or format constraints. The repository does not yet implement this layer formally, but JSON Schema is a natural fit for where this layer should eventually sit.[^c7-jsonschema]

### 7.1.4 Business-Rule Validation

Business-rule validation asks whether content satisfies rules beyond structure. Examples include taxonomy membership, allowed workflow state, or uniqueness across a domain concept rather than just across chunk IDs.

### 7.1.5 Corpus-Level Validation

Corpus-level validation asks whether the collection remains coherent as a whole. Examples include placeholder detection, navigation drift, duplicate identities, or missing build artifacts.

### 7.1.6 Operational Validation

Operational validation asks whether the system emits enough evidence to explain its own behavior. In a mature system this includes logs, metrics, traces, health signals, and release artifacts.

These layers solve different problems. They should fail differently and be inspected differently.

## 7.2 What The Repository Validates Today

The repository validates the ETL boundary rather than the full target platform. The test suite in `tests/test_etl.py` verifies:

- Markdown content files are discoverable
- YAML front matter parsing behaves predictably
- heading-based chunk extraction works as expected
- extracted chunk records contain required fields
- emitted chunk identifiers are unique across the corpus
- graph projection emits expected relationship structures
- the CLI writes the expected JSON artifacts
- placeholder `_TODO` text no longer remains in content chapters

This is a narrow validation boundary, but it is an important one. It protects the first stable machine contract in the repository.

## 7.3 Syntax And Structural Validation In Practice

The current implementation is simple enough that its validation rules can be described directly.

### 7.3.1 Front Matter Must Be Parseable

`yaml.safe_load()` must be able to parse the front matter block. Malformed YAML fails immediately.

### 7.3.2 Front Matter Must Produce A Mapping

Even when YAML parses successfully, the result must be a mapping. A list or scalar does not satisfy the metadata contract.

### 7.3.3 Chunk Records Must Be Complete

Each emitted chunk must include the fields needed for provenance, ordering, grouping, and downstream projection.

### 7.3.4 Chunk Identity Must Be Unique Across The Corpus

The test suite checks the current corpus for duplicate IDs. That is a small but critical invariant because graph loading and retrieval both depend on it.

## 7.4 Worked Failure Cases

The repository's failure cases are useful because they expose the shape of the contract.

### 7.4.1 Non-Mapping Front Matter

Input:

```md
---
- invalid
- front
- matter
---

## Section

Text.
```

Outcome:

- front matter is detected
- YAML parsing succeeds
- structural validation fails because the parsed value is not a mapping

This is correct behavior because metadata must remain key-addressable.

### 7.4.2 Empty Body After Front Matter

Input:

```md
---
title: Empty Example
slug: empty-example
---
```

Outcome:

- front matter parsing succeeds
- no chunk records are emitted

This shows the difference between valid metadata and useful content.

### 7.4.3 No Level-Two Headings

Input:

```md
This document has prose but no section headings.
```

Outcome:

- the document still produces a single chunk
- that chunk is labeled `Intro`

This is a design choice. The repository prefers transformability over rejecting all unsectioned prose.

## 7.5 Where Schema Validation Should Sit

The repository currently stops at structural validation, but a fuller system should introduce schema validation between parsing and downstream derivation.

That layer should answer questions such as:

- which metadata fields are required for a content type
- which fields have constrained types or enumerations
- which nested structures are allowed
- which identifiers or slugs must follow a format

JSON Schema is a natural fit for this layer because it can describe object shape, required keys, nested structures, and constrained value forms in a machine-readable way. It does not replace business rules, but it provides a cleaner contract than ad hoc field checks.

## 7.6 Validation And Security

Production validation is broader than content shape. A fuller OKS platform would also need to validate:

- interface inputs exposed through authoring or API surfaces
- permission-sensitive operations
- publication metadata and output integrity
- audit and review trails for privileged actions

This is where a verification framework such as OWASP ASVS becomes useful.[^c7-asvs] The repository does not yet implement those controls, but the architecture should preserve a path to them.

## 7.7 Validation And Operational Evidence

Validation is not complete when the system rejects bad input. It is complete when the system can explain what happened.

At the repository level, tests and build behavior are the first form of that evidence. In a fuller system, operational evidence would also include:

- logs that show parsing and loader failures
- metrics for content throughput and build status
- traces for long-running ingestion or publication paths
- release artifacts that prove what content was published

OpenTelemetry is a useful reference point for this later layer because it treats telemetry as a structured system contract rather than as scattered logging.[^c7-otel]

## 7.8 Future Validation Architecture

A stronger validation architecture should proceed in stages:

1. reject malformed input at parse time
2. enforce schema constraints before normalization is trusted
3. apply business-rule validation over domain-specific semantics
4. validate graph, retrieval, and publication artifacts against normalized source
5. verify operational evidence and release integrity

This sequence matters. It keeps the expensive validation layers dependent on a stable core rather than using them to compensate for weak early contracts.

## 7.9 Why This Chapter Matters

The repository's current validation layer is narrow, but it already does something essential: it defines the minimum conditions under which the rest of the system can be trusted.

Without that layer, the ETL chapter would describe a transformation but could not defend it. With that layer, the manuscript can make a stronger claim: the first machine boundary in the system is not only implemented, but checked.

## 7.10 Reading Notes

- **JSON Schema:** useful for the boundary between structural validation and formal content contracts.
- **OWASP ASVS:** useful for the security side of validation once the system exposes operational surfaces.
- **OpenTelemetry Specification:** useful for understanding why operational evidence is part of validation rather than a separate concern.

[^c7-jsonschema]: JSON Schema, *What is JSON Schema?*: https://json-schema.org/overview/what-is-jsonschema
[^c7-asvs]: OWASP Foundation, *Application Security Verification Standard*: https://owasp.org/www-project-application-security-verification-standard/
[^c7-otel]: OpenTelemetry, *OpenTelemetry Specification*: https://opentelemetry.io/docs/specs/otel/
