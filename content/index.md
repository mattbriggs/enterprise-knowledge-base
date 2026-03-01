# Open Knowledge Systems

*A technical manual for designing structured, machine-readable knowledge systems, grounded in a working Markdown ETL reference implementation.*

Open Knowledge Systems addresses a practical engineering problem: how to turn loosely managed documents into content that can be structured, validated, transformed, published, and queried as knowledge. The manual treats that problem as both architectural and implementation work. It is written to help technical readers design the larger system without losing the mechanics that make such systems reliable.

The repository has two layers:

- a design-level manuscript that describes the target platform
- a narrower reference implementation that normalizes Markdown into stable chunk and graph-oriented records

The book is written for architects, staff engineers, technical leads, and advanced practitioners who need a disciplined model for content pipelines, graph projection, retrieval boundaries, and publication workflows. It assumes familiarity with software architecture, data modeling, and modern developer tooling, but it does not assume that the reader has already built a knowledge system end to end.

## What This Book Covers

- how to define a content model that can survive validation, transformation, and publication
- how to normalize author-facing Markdown into machine-friendly records
- how to project content into graph-aware structures without collapsing the source-of-truth boundary
- how to think about retrieval, publication, validation, and operational constraints as one coherent system

## What This Repository Implements Today

The current codebase does not yet implement the full platform described in the architecture chapters. What it does implement is a stable first slice:

- YAML front matter parsing
- heading-based Markdown chunk extraction
- normalized chunk records
- graph-oriented projection for downstream Neo4j-style loading
- corpus-level tests around that transformation boundary

That distinction remains explicit throughout the manuscript. The target architecture is discussed as a design goal. The repository is described only where behavior is implemented and inspectable.

## How To Read The Book

For architecture, start with the Introduction and System Model chapter, then move through Storage, Validation, and Publication. For implementation, start with Authoring and ETL, then continue through Graph Modeling, Storage, and Validation. If you are using the repository as a reference, treat the code as the executable center of gravity and the surrounding chapters as design context.

## Reading Standard

The manuscript is written toward a technical-manual standard. The emphasis is on precision, mechanisms, boundaries, and tradeoffs rather than on broad product claims. When the text discusses capabilities that are not yet implemented in this repository, it should do so as architecture, not as fact.
