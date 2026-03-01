---
title: "Appendix"
slug: 98_appendix
---

# 9. Appendix

This appendix supports the main text with compact reference material. It does not carry architectural argument on its own. Terms appear only where they help the reader move through the technical chapters with less friction.

## A.1 Core Terms

- **Source document:** An author-facing Markdown file, optionally with YAML front matter.
- **Front matter:** The YAML metadata block at the top of a source document.
- **Normalized record:** A machine-friendly chunk emitted by the ETL layer, with stable identity and preserved provenance.
- **Chunk:** A section of a source document produced by the repository's current `##`-based chunking rule.
- **Graph projection:** A graph-ready representation derived from normalized records, intended for downstream relationship-oriented workflows.
- **Source of truth:** The representation that is authoritative for a class of edits. In the current repository, authored Markdown is the human-facing source of truth.
- **Derived artifact:** Any output regenerated from source or normalized records, such as graph JSON, site output, EPUB, or PDF.
- **Publication artifact:** A reader-facing output surface such as the MkDocs site, an EPUB, or a PDF.
- **Design target:** A capability discussed as part of the target platform but not yet implemented in the repository.
- **Implemented behavior:** A behavior that can be inspected in the repository code or validated by tests.

## A.2 Repository Artifact Map

| Path | Role |
| --- | --- |
| `content/*.md` | primary manuscript and source content corpus |
| `content/notebooks/` | notebook content published through MkDocs |
| `src/oks/etl.py` | current ETL implementation slice |
| `tests/test_etl.py` | executable checks around the ETL boundary |
| `graphs/schema.cypher` | example Neo4j schema and seed script |
| `mkdocs.yml` | documentation site configuration and navigation |
| `scripts/build.sh` | local repeatable build workflow |
| `.github/workflows/build-docs.yml` | CI publication and validation workflow |
| `build/chunks.json` | normalized chunk corpus generated locally |
| `build/graph.json` | graph-oriented projection generated locally |

## A.3 Command Reference

The following commands are the main operational entry points for the current repository.

### Build The HTML Site

```bash
mkdocs build --strict
```

### Run The Tests

```bash
pytest
```

### Generate Normalized Chunk Output

```bash
python -m oks.etl content --output build/chunks.json
```

### Generate Chunk And Graph Outputs Together

```bash
python -m oks.etl content \
  --output build/chunks.json \
  --graph-output build/graph.json
```

### Run The Local Build Script

```bash
./scripts/build.sh
```

## A.4 Abbreviations

- **API:** Application Programming Interface.
- **CI:** Continuous Integration.
- **CRUD:** Create, Read, Update, Delete.
- **ETL:** Extract, Transform, Load.
- **HTML:** Hypertext Markup Language.
- **JSON:** JavaScript Object Notation.
- **JSON-LD:** JSON for Linked Data.
- **KG:** Knowledge Graph.
- **KPI:** Key Performance Indicator.
- **MkDocs:** Static site generator used for the HTML publication surface in this repository.
- **Neo4j:** Graph database used as the reference target for the current graph projection chapter.
- **OKS:** Open Knowledge Systems.
- **PDF:** Portable Document Format.
- **RBAC:** Role-Based Access Control.
- **SLA:** Service Level Agreement.
- **UI:** User Interface.
- **YAML:** Human-readable serialization format used for front matter in the current source-document contract.

## A.5 Reading Conventions

The manuscript uses a few repeated distinctions that are worth keeping visible:

- **Target architecture** refers to the broader platform the book is designing toward.
- **Current repository** refers to the implementation and build behavior that can be inspected now.
- **Manual chapters** explain system boundaries, mechanisms, and tradeoffs.
- **Design criteria** state standards the system should satisfy.

Whenever those distinctions blur, the chapter in question should usually be revised rather than explained away.
