# Editorial Plan

## Purpose

This document turns the current manuscript audit into an executable revision brief. The goal is to move *Open Knowledge Systems* from a mixed SRS/specification draft into a high-standard technical manual with textbook discipline, stronger flow, and deeper technical substantiation.

The editorial target is:

- precise, cumulative prose
- explicit distinction between target architecture and current implementation
- chapter-level arguments instead of requirement inventories
- stronger sourcing from standards, official documentation, and primary technical material
- concrete technical artifacts in every substantive chapter

## Editorial Position

The book should be framed as:

- a technical manual for designing and implementing enterprise knowledge systems
- grounded in a narrow but real reference implementation in this repository
- supplemented by design criteria and requirements, rather than dominated by them

The book should not read primarily as:

- a formal SRS
- a product brochure
- a speculative roadmap

## Revised Table Of Contents

This is the target table of contents for the next major manuscript pass. It is a narrative structure, not yet a one-to-one file layout commitment.

1. Introduction  
   Why knowledge systems are hard, who this book is for, what the reader will build or understand, and how the book is organized.

2. System Model And Design Principles  
   Problem framing, system boundaries, content as structured knowledge, target architecture, and non-goals.

3. Content Model And Authoring Contract  
   Schema concepts, document shape, front matter, controlled vocabularies, ontology boundaries, authoring rules, and failure modes.

4. ETL And Content Normalization  
   Parsing, chunking, normalization, idempotency, record design, and the reference implementation in `src/oks/etl.py`.

5. Storage, Graph Projection, And Retrieval Boundaries  
   Document form, graph form, identifiers, synchronization boundaries, retrieval modes, and graph-ready representations.

6. Validation, Quality Gates, And Operational Safety  
   Structural validation, rule validation, authoring safeguards, test design, telemetry boundaries, and what must fail fast.

7. Publication, Delivery, And Machine-Readable Output  
   Static-site generation, JSON-LD, artifact production, deployment surfaces, and publication workflow.

8. Search, Query, And Knowledge Access  
   Keyword retrieval, semantic retrieval, metadata filtering, graph queries, and interface design.

9. Security, Reliability, And Scalability Design Criteria  
   Identity, authorization, observability, performance assumptions, and capacity planning as design constraints.

10. Future Directions And Implementation Roadmap  
    What the repository implements now, what the target platform still lacks, and how to evolve without losing rigor.

Appendix A. Glossary And Terminology  
Appendix B. Condensed Requirement Matrix  
Appendix C. Reference Architecture Diagrams  
Appendix D. Research Notes And Sources

## Chapter-By-Chapter Rewrite Brief

### `content/index.md`

Status: Rewrite completely.

Role in book:

- establish the book's promise
- define the intended reader
- orient the reader to the distinction between current repository and target platform

Required additions:

- a clear one-paragraph thesis
- audience and prerequisites
- what is implemented now
- a short reading path through the book

Avoid:

- generic welcome copy
- marketing language

### `content/01_introduction.md`

Status: Rewrite completely.

Role in book:

- replace SRS framing with manual framing
- define scope, boundaries, and reader expectations

Required additions:

- explicit reader contract
- design problem statement
- distinction between target architecture and reference implementation
- chapter-by-chapter map
- conventions used in the book

Avoid:

- exhaustive glossary-style definition dumps in the main flow
- standards boilerplate for its own sake

### `content/02_overall_description.md`

Status: Heavy rewrite and compression.

Role in book:

- become the conceptual center of the architecture
- explain the system as a set of cooperating boundaries

Required additions:

- architecture described as responsibilities and interfaces, not just module lists
- clearer separation of logical model versus deployable system
- a short list of design principles
- explicit non-goals

Required cuts:

- repetitive restatement of content, graph, API, and monitoring claims
- speculative deployment detail that is not yet justified

### `content/03_requirements.md`

Status: Demote and restructure.

Role in book:

- become a condensed design criteria chapter or appendix

Required changes:

- compress requirement prose into grouped tables
- separate mandatory design criteria from speculative future capabilities
- tie each criterion to a validation method

Avoid:

- line-by-line narrative requirement sprawl in the main text

### `content/04_authoring_etl.md`

Status: Expand substantially.

Role in book:

- become the first concrete technical chapter

Required additions:

- worked example of a Markdown source file
- front matter parsing rules
- chunk extraction behavior
- identifier construction
- expected normalized output examples
- failure cases and edge cases

### `content/05_graph_modeling_neo4j.md`

Status: Expand substantially.

Role in book:

- explain the graph projection as a design choice

Required additions:

- node labels and property definitions
- relationship semantics
- sample Cypher queries
- discussion of why a property graph is being used here
- limits of the current graph model

### `content/06_storage_retrieval.md`

Status: Expand substantially.

Role in book:

- define storage contracts and retrieval boundaries

Required additions:

- document form versus graph form
- source-of-truth discussion
- synchronization model
- retrieval paths and indexing implications
- future vector-search boundary without hand-waving

### `content/07_validation.md`

Status: Expand substantially.

Role in book:

- explain validation as layered quality control

Required additions:

- syntax validation
- schema validation
- business-rule validation
- corpus-level quality checks
- test strategy tied to failure modes

### `content/08_publication.md`

Status: Expand substantially.

Role in book:

- explain how technical content becomes publishable output

Required additions:

- publication pipeline
- HTML, EPUB, and PDF roles
- JSON-LD and machine-readable publication
- build reproducibility and release criteria

### `content/98_appendix.md`

Status: Rebuild after main chapters stabilize.

Role in book:

- support the text with compact definitions

Required changes:

- remove material that belongs in the main chapters
- shorten definitions
- keep only terms that materially help the reader

### `content/99_future_work.md`

Status: Keep, then tighten later.

Role in book:

- define disciplined next steps

Required additions:

- implementation milestones
- editorial milestones
- dependency on completed technical foundations

## Research Standard For Rewrite

Each major chapter revision should be supported by stronger sources than the current draft. Preferred source classes:

- standards and RFCs
- official product or framework documentation
- academic papers for retrieval, knowledge representation, and evaluation methods
- engineering references with concrete operational guidance

Avoid relying on:

- vendor marketing pages as primary authority
- unsourced performance targets
- broad claims about AI, search, or knowledge graphs without mechanism

## Revision Sequence

1. Rewrite `index.md` and `01_introduction.md`.
2. Rewrite `02_overall_description.md` into a cleaner architecture chapter.
3. Convert `03_requirements.md` into condensed design criteria and move the long-form inventory to appendix form.
4. Expand `04` through `08` into the technical spine of the book.
5. Rebuild the appendix only after the main chapters have stabilized.
6. Perform a final global prose pass for consistency, diction, and transitions.

## Quality Bar

The manuscript is ready for a serious review pass only when:

- each chapter has a single governing argument
- every major claim is either evidenced, cited, or marked as a design target
- the prose no longer sounds like a generated specification ledger
- the current repository and the target platform are clearly separated
- the reader can move through the book without genre confusion
