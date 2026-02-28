---
title: "Validation"
slug: 07_validation
---

# 7. Validation

Validation is the part of the system that determines whether the rest of the architecture can be trusted. In a knowledge system, invalid structure does not merely produce a bad page. It contaminates derived records, graph projections, search indexes, and operational expectations. That is why validation should be treated as a layered system concern rather than as a single boolean check.

The repository implements only the first layer of that model, but it implements that layer concretely enough to study. This chapter explains the current validation boundary, the tests that enforce it, and the additional layers a fuller platform will need.

## 7.1 Validation As Layers

The manuscript uses the word "validation" in several different senses. They should be separated.

### 7.1.1 Syntax Validation

Syntax validation asks whether the source document can be parsed at all. In the current repository this includes front matter detection and YAML parsing behavior.

### 7.1.2 Structural Validation

Structural validation asks whether the parsed document conforms to the repository's transformation contract. In the current implementation this includes rules such as "front matter must parse to a mapping" and "chunk records must contain required fields."

### 7.1.3 Business-Rule Validation

Business-rule validation asks whether the content satisfies domain rules beyond structure. Examples include uniqueness rules, allowed taxonomy membership, or schema-specific authoring constraints. The repository does not yet implement this layer.

### 7.1.4 Corpus-Level Validation

Corpus-level validation asks whether the content set remains coherent as a collection. Examples include placeholder detection, duplicate identifiers, broken publication navigation, or missing build artifacts. The repository implements only a small portion of this layer.

These distinctions matter because each layer fails for different reasons and should be tested differently.

## 7.2 What The Current Implementation Validates

The repository validates the ETL boundary rather than the full target platform. The test suite in `tests/test_etl.py` verifies:

- Markdown content files are discoverable
- YAML front matter parsing behaves predictably
- heading-based chunk extraction works as expected
- extracted chunk records contain the required fields
- emitted chunk identifiers are unique across the corpus
- graph projection emits expected relationship structures
- the CLI writes the expected JSON artifacts
- placeholder `_TODO` text no longer remains in content chapters

This is a narrow validation boundary, but it is a useful one. It protects the first stable machine contract in the repository.

## 7.3 Syntax Validation In Practice

The first validation layer is syntax.

### 7.3.1 Front Matter Parsing

Front matter is parsed with `yaml.safe_load()`. The parser will accept ordinary YAML mappings and reject malformed YAML. More importantly for the repository's current contract, it will also reject top-level YAML values that are not mappings.

For example, this should parse successfully:

```yaml
---
title: Knowledge Handbook
slug: knowledge-handbook
---
```

This should fail structural validation after parsing because the top-level YAML value is a list:

```yaml
---
- title
- slug
---
```

And malformed YAML such as:

```yaml
---
title: Example
slug example
---
```

should fail even earlier at the parser boundary.

### 7.3.2 Markdown Body Shape

The repository does not validate Markdown against the full CommonMark surface. Instead, it validates only the subset of structure needed by the ETL boundary. The most important current rule is that level-two headings create chunk boundaries.

That means the system does not currently ask, "Is this Markdown beautiful?" It asks, "Can this Markdown be transformed into a stable section model?"

## 7.4 Structural Validation In Practice

Once parsing succeeds, the next question is whether the transformation contract can be satisfied.

### 7.4.1 Required Record Fields

Every emitted chunk must include the standard record fields:

- `id`
- `heading`
- `content`
- `order`
- `source_file`
- `source_path`
- `document_title`
- `document_slug`
- `metadata`

Later consumers should not need to guess whether a chunk has enough information to be grouped, projected, or published.

### 7.4.2 Identity Validation

The current test suite checks that emitted chunk identifiers are unique across the current corpus. That is a small but important validation rule. Duplicate chunk IDs would break graph projection, future indexing, and any downstream attempt to use the chunk as a stable reference.

### 7.4.3 Corpus Placeholder Validation

The repository also performs a simple but meaningful corpus-level check: it fails if placeholder `_TODO` text remains in content files. This is not schema validation in the classic sense, but it is still a quality gate. It prevents unfinished editorial scaffolding from being mistaken for publishable content.

## 7.5 Worked Failure Cases

The current system is simple enough that its failure cases can be described directly.

### 7.5.1 Non-Mapping Front Matter

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

Current outcome:

- the file is detected as having front matter
- YAML parsing succeeds
- structural validation fails because the parsed value is not a mapping

Why this is correct:

- the ETL layer expects front matter to behave like metadata, not like an arbitrary YAML document

### 7.5.2 No Level-Two Headings

Input:

```md
This document has prose but no section headings.
```

Current outcome:

- the document still produces a single chunk
- that chunk is labeled `Intro`

Why this is correct:

- the repository chooses to preserve transformability rather than reject all unsectioned prose

### 7.5.3 Empty Body After Front Matter

Input:

```md
---
title: Empty Example
slug: empty-example
---
```

Current outcome:

- front matter parsing succeeds
- no chunk records are emitted

Why this matters:

- it reveals that "valid metadata" is not the same thing as "useful content"
- later platform layers may choose to reject this case more aggressively

## 7.6 The Current Test Boundary

The current test boundary is intentionally close to the ETL code. That is a strength, not a weakness, for this stage of the repository.

The tests are useful because they are:

- fast
- deterministic
- independent of external services
- focused on the repository's real implementation

This means the build can tell the maintainer something concrete: whether the Markdown-to-record contract still holds.

## 7.7 What Is Not Yet Validated

The repository does not yet validate several important layers that the target platform will require:

- schema-specific field contracts beyond simple front matter presence
- business rules such as uniqueness across semantic entities
- ontology integrity
- authoring-time form validation
- graph-load consistency against a live Neo4j instance
- search relevance or index freshness
- telemetry completeness and auditability
- performance targets under realistic workload

These are not omissions in theory. They are future validation layers that should be added only after the current normalization boundary remains stable.

## 7.8 Future Validation Architecture

A fuller OKS platform should validate content in stages rather than in one monolithic check.

### 7.8.1 Ingestion-Time Validation

Reject malformed or structurally incompatible input before it reaches durable storage.

### 7.8.2 Schema Validation

Validate required fields, field types, enumerations, and structural constraints against an explicit schema model.

### 7.8.3 Business-Rule Validation

Validate content against domain-specific rules such as uniqueness, workflow status, ontology membership, or publication readiness.

### 7.8.4 Derived-Artifact Validation

Verify that graph projections, publication outputs, and later retrieval indexes remain consistent with the normalized source.

### 7.8.5 Operational Validation

Verify that logs, metrics, health checks, and build outputs provide enough evidence to explain system behavior.

Validation should eventually become part of the platform architecture rather than remain only a test-suite concern.

## 7.9 Why This Chapter Matters

The repository's current validation layer is narrow, but it already does something important: it defines the minimum conditions under which the rest of the system can be trusted.

Without that layer, the ETL chapter would describe a transformation but could not defend it. With that layer, the repository can make a stronger claim: the first machine boundary in the system is not only implemented, but checked.
