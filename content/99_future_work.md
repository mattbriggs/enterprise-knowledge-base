---
title: "Roadmap"
slug: 99_future_work
---

# 10. Roadmap

Chapter 10 defines how the repository should evolve without losing the discipline established in the earlier chapters. A roadmap is useful only if it preserves architectural order. In this project, that means future work should extend the current machine boundary outward from the ETL core rather than leap toward the most ambitious platform surfaces.

The central rule is simple: add capabilities in the order that makes their behavior explainable, testable, and rebuildable from source. The repository should resist the temptation to claim completeness through breadth. It should earn completeness through sequence.

## 10.1 Roadmap Principles

The roadmap is governed by five principles.

### 10.1.1 Expand From The Stable Boundary

New capabilities should consume the normalized record boundary rather than bypass it. If a future loader, retrieval layer, or publication feature reparses source content independently, it weakens the architecture instead of extending it.

### 10.1.2 Prefer Rebuildable Systems Over Convenient Ones

Any new subsystem should be regenerable from source or from explicitly governed intermediates. Rebuildability is more valuable at this stage than operational cleverness.

### 10.1.3 Add Verification With Every New Capability

A roadmap item is incomplete if it introduces a new surface area without a matching test, validation path, or inspection mechanism.

### 10.1.4 Preserve The Distinction Between Target Architecture And Current Repository

Future work can move the repository toward the target platform, but the manuscript should continue to distinguish what is implemented now from what remains architectural intent.

### 10.1.5 Sequence Matters More Than Volume

Adding many features quickly is less valuable than adding a few in the right order. The correct order is the one that protects identity, determinism, and source-of-truth discipline.

## 10.2 Phase One: Harden The Current Core

The first phase should make the current ETL-centered repository harder to misuse and easier to extend.

### Objectives

- define explicit schema contracts for the currently supported content shape
- keep the chunk record contract stable
- make generated artifacts easier to inspect and compare
- increase confidence that corpus rebuilds remain deterministic

### Candidate Work

- add explicit schema definitions for supported content types
- introduce fixture-based golden tests for emitted chunk and graph JSON
- add package API documentation for `src/oks`
- document failure semantics more systematically in code and prose

### Exit Criteria

Phase one is complete when a contributor can explain the source contract, run the ETL boundary, inspect the outputs, and understand why the tests pass or fail without relying on undocumented assumptions.

## 10.3 Phase Two: Add Derived Loaders

Once the ETL boundary is stable, the next useful extension is to add consumers of that boundary rather than broader product surfaces.

### Objectives

- turn the graph projection into a repeatable loading path
- ensure derived storage remains subordinate to normalized records
- validate the correctness of the projection against a real database target

### Candidate Work

- introduce a Neo4j loader that consumes `build/graph.json` or the in-memory projection directly
- replace purely pedagogical seed data with idempotent `MERGE`-based load logic
- add integration tests against a disposable Neo4j instance
- document graph load invariants and failure cases

### Exit Criteria

Phase two is complete when the graph can be rebuilt from normalized records repeatably and verified through tests or inspection queries.

## 10.4 Phase Three: Strengthen Validation And Retrieval

After derived loaders exist, the next priority is to make the system more selective and more queryable without breaking the current architecture.

### Objectives

- move from structural validation alone toward richer schema and rule validation
- define retrieval layers that consume governed content rather than bypass it
- make performance and quality claims measurable

### Candidate Work

- add schema-level validation beyond front matter structure
- introduce business-rule checks for content quality and identity management
- add lexical retrieval experiments over normalized chunks
- define workload models and benchmark methodology before making stronger performance claims

### Exit Criteria

Phase three is complete when validation and retrieval behavior can be described as concrete mechanisms rather than as future-facing aspirations.

## 10.5 Phase Four: Add Delivery Surfaces Carefully

Only after the core and its derived consumers are stable should the repository expand toward broader platform surfaces such as APIs or richer publication metadata.

### Objectives

- expose governed content through machine-facing interfaces
- enrich publication outputs without undermining the authoring model
- introduce operational controls that match the new surface area

### Candidate Work

- add an API layer over normalized and derived content stores
- add machine-readable publication metadata such as JSON-LD
- introduce explicit health, metrics, and audit surfaces
- evaluate search and semantic retrieval boundaries for later integration

### Exit Criteria

Phase four is complete when delivery surfaces are derived from governed content contracts and are supported by observability and validation rather than by optimistic assumptions.

## 10.6 Editorial Roadmap

The manuscript itself has a parallel roadmap.

### Immediate Editorial Priorities

- complete the rewrite of all core chapters to a uniform manual standard
- remove language that reads like a legacy specification draft or product brochure
- keep examples tied to repository code or clearly marked as design targets

### Medium-Term Editorial Priorities

- add stronger primary-source research to support security, retrieval, graph, and publication chapters
- introduce more worked examples and comparison tables
- add appendix material only where it supports the main text rather than duplicating it

### Final Editorial Priorities

- maintain a consistent line-level style as new chapters and examples are added
- unify terminology, voice, and evidence standards
- ensure every chapter contributes to a single cumulative argument

## 10.7 Work That Should Not Be Prioritized Yet

The following items may be attractive, but they should not come first:

- elaborate deployment assets before the local pipeline is fully stable
- vector-search infrastructure before lexical and graph boundaries are explicit
- large ontology ambitions before the graph projection contract is hardened
- broad API claims before the data contracts are mature
- performance promises without workload models and verification paths

These are not forbidden. They are simply downstream work.

## 10.8 What Success Looks Like

The repository is moving in the right direction when each new capability satisfies four tests:

- it is derived from a clear content contract
- it can be rebuilt or replayed deterministically
- it adds its own validation or inspection path
- it narrows the gap between the manuscript and the implementation without inflating claims

That is the standard the roadmap should enforce. A disciplined roadmap is part of the architecture, not just a note about future ambitions.
