---
title: "Publishing & Output"
slug: 08_publication
---

# 8. Publishing & Output

Publication is where the content model becomes visible to readers and reviewers. It is also where weak modeling decisions become expensive. If navigation is inconsistent, artifacts are not reproducible, derived content cannot be regenerated from source, or machine-readable output is an afterthought, publication exposes those weaknesses immediately.

Even in its current form, publication is already a meaningful engineering boundary. The repository publishes a browsable documentation site, can produce EPUB and PDF artifacts, and treats build correctness as part of the manuscript contract.

## 8.1 Publication In The Current Repository

The current publication layer has three output classes:

- HTML documentation built with MkDocs
- EPUB generated with Pandoc
- PDF generated either from HTML via WeasyPrint or directly via Pandoc

The HTML site is the primary artifact because it is the fastest review surface and the one most tightly integrated with the repository's content workflow.

## 8.2 Source-To-Artifact Pipeline

The publication path in the repository is intentionally simple:

1. content is authored in `content/*.md`
2. MkDocs renders the book into a static HTML site
3. optional export tools produce EPUB and PDF outputs
4. tests run alongside publication checks so the manuscript and implementation slice fail together when contracts drift

This is more than a convenience workflow. It reflects the book's larger position: publication should depend on governed content and explicit build rules, not on ad hoc manual export steps.

## 8.3 The HTML Publication Path

The HTML site is configured through `mkdocs.yml`. Several details matter:

- `docs_dir: content` means the manuscript itself is the source corpus for the site
- navigation order is explicitly declared rather than inferred
- `mkdocs-jupyter` publishes notebook content as part of the book
- `mkdocs build --strict` is the expected build mode, which treats broken navigation and related drift as failures

That last point is especially important. Strict mode turns publication from a best-effort rendering step into a quality gate.

## 8.4 The Export Artifact Path

The repository also supports book-style exports.

### 8.4.1 EPUB

EPUB output is built from the Markdown corpus with Pandoc. The current commands use:

- the `content/*.md` source set
- explicit title metadata
- a table of contents
- chapter-level splitting for EPUB generation

EPUB matters because it forces the manuscript to remain structurally coherent outside the HTML site.

### 8.4.2 PDF

PDF output currently has two possible paths:

- render the HTML site into PDF with WeasyPrint
- generate PDF directly from Markdown through Pandoc and a LaTeX engine

Those paths have different tradeoffs.

- The HTML-to-PDF path preserves more of the site styling model.
- The Pandoc-to-PDF path is more independent of the web output but depends on LaTeX availability and formatting behavior.

The repository supports both because publication is still being stabilized.

## 8.5 Build Automation And Release Discipline

The publication layer is governed by two operational entry points:

- `scripts/build.sh` for local repeatable builds
- `.github/workflows/build-docs.yml` for CI validation and artifact generation

The local build script currently performs the following sequence:

1. clean old outputs
2. build the HTML site in strict mode
3. build EPUB if Pandoc is available
4. build PDF if WeasyPrint is available
5. run tests

The CI workflow performs a similar sequence on GitHub Actions, including dependency installation, strict MkDocs build, tests, and artifact upload.

This matters for two reasons. First, the manuscript is already part of an engineering release process rather than a detached prose document. Second, it creates a review standard: a chapter is not ready merely because it reads well; it must also survive the publication pipeline.

## 8.6 Worked Example: Publication Surfaces

A single manuscript chapter currently exists simultaneously in several forms.

For example, a chapter authored as:

- `content/04_authoring_etl.md`

can appear as:

- a navigable page in the MkDocs site
- a section in the EPUB output
- a section in the generated PDF
- source content for ETL-derived artifacts elsewhere in the repository

A chapter is not written for one output surface only. A well-formed chapter must:

- render predictably as HTML
- remain readable in export form
- preserve heading structure for navigation
- maintain stable links in the docs site

Publication therefore places a structural demand on the prose itself.

## 8.7 Publication And The ETL Boundary

The publication layer and the ETL layer are intentionally separate.

- The ETL layer normalizes content for machine-facing use.
- The publication layer renders content for reader-facing use.

That separation is important. Publication should not become the only way the system knows how to interpret content, and ETL should not be forced to adopt the assumptions of a specific static-site renderer.

This also explains why the repository currently does not generate the HTML site from `build/chunks.json`. The normalized chunk corpus exists to support machine-oriented workflows. The manuscript still renders directly from the author-facing source corpus.

## 8.8 Machine-Readable Publication

The target platform described elsewhere in the book aims to produce stronger machine-readable publication outputs, including structured metadata such as JSON-LD. The repository does not yet implement that layer.

Keep that distinction explicit:

- current repository publication is primarily human-facing
- target platform publication should become both human-facing and machine-readable

Machine-readable publication is not just a serialization problem. It depends on earlier architectural work:

- stable identifiers
- clearer content typing
- explicit schema mapping
- controlled metadata vocabularies

Without those, JSON-LD or other structured publication formats become decorative rather than useful.

## 8.9 Publication Failure Modes

Several publication failures are already visible in a repository of this size:

- navigation drift between the manuscript and `mkdocs.yml`
- placeholder content reaching published output
- export paths depending on environment-specific tooling
- artifact generation succeeding while the implementation slice has regressed

The repository mitigates these risks in simple ways:

- strict MkDocs builds
- tests that reject placeholder `_TODO` text
- explicit build automation
- CI artifact generation

These are modest controls, but they are real controls.

## 8.10 Release Criteria For The Manuscript

At the level of the current repository, a chapter should be treated as publication-ready only when:

- it fits cleanly into the MkDocs navigation structure
- it renders without build drift in strict mode
- it contains no placeholder scaffolding
- its examples match the implementation or are clearly marked as design targets
- its presence does not break EPUB or PDF export paths

This editorial standard ties writing quality to build integrity.

## 8.11 Current Limits

The publication layer does not yet provide:

- explicit JSON-LD or schema.org metadata emission
- content-type-specific publication templates beyond the MkDocs theme structure
- incremental artifact rebuild logic
- release metadata attached to normalized records
- a publication path derived from the chunk corpus itself

Those are valid future directions, but they should be built on the current discipline rather than added speculatively.

## 8.12 Why Publication Belongs In The Technical Spine

Publication is not the end of the system. It is a test of the system.

If the content model is weak, publication exposes that weakness. If the architecture has no clear source-of-truth policy, publication makes the ambiguity visible. If the build surface is not reproducible, publication is where the failure becomes operationally expensive.

Publication belongs in the technical spine of this book rather than in a short tooling appendix. It is one of the places where architecture becomes observable.
