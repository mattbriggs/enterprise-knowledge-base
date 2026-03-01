---
title: "Publishing & Output"
slug: 08_publication
---

# 8. Publishing & Output

Publication is where the content model becomes visible to readers and reviewers. It is also where weak modeling decisions become operationally expensive. If navigation drifts, if artifacts cannot be rebuilt, if machine-readable output is an afterthought, or if build rules are informal, publication exposes those weaknesses quickly.

That is why publication belongs in the technical spine of the book. It is not merely a formatting step. It is the boundary where contracts from the earlier chapters become observable artifacts.

## 8.1 Publication Surfaces In The Repository

The repository currently supports three output classes:

- HTML documentation built with MkDocs
- EPUB generated with Pandoc
- PDF generated either from HTML via WeasyPrint or from Markdown via Pandoc

The HTML site is the primary artifact because it is the fastest review surface and the one most tightly integrated with the manuscript's day-to-day workflow.

## 8.2 The HTML Publication Path

The HTML site is configured through `mkdocs.yml`.[^c8-mkdocs] Several details matter:

- `docs_dir: content` means the manuscript itself is the source corpus for the site
- navigation order is declared explicitly rather than inferred from filenames
- `mkdocs-jupyter` publishes notebook content as part of the book
- `mkdocs build --strict` is the intended build mode

Strict mode is especially important. It turns publication from a best-effort rendering step into a quality gate. Broken navigation, broken links between chapters, and related drift become build failures rather than editorial surprises.

## 8.3 Export Artifact Paths

The repository also supports book-style export artifacts.

### 8.3.1 EPUB

Pandoc builds EPUB from the Markdown corpus.[^c8-pandoc] That path matters because it forces the manuscript to remain structurally coherent outside the HTML site. A chapter that works only inside one static-site renderer is weaker than it appears.

### 8.3.2 PDF

The repository supports two PDF paths:[^c8-weasy]

- HTML to PDF through WeasyPrint
- Markdown to PDF through Pandoc and a LaTeX engine

These paths have different tradeoffs.

- the WeasyPrint path preserves more of the HTML styling model
- the Pandoc path is more independent of the site renderer but depends on LaTeX availability and template behavior

Keeping both paths visible is useful while publication is still being stabilized.

## 8.4 Build Automation And Release Discipline

Publication is governed by two operational entry points:

- `scripts/build.sh` for local repeatable builds
- `.github/workflows/build-docs.yml` for CI validation and artifact generation

The local build script currently performs this sequence:

1. remove prior outputs
2. build the HTML site in strict mode
3. build EPUB if Pandoc is available
4. build PDF if WeasyPrint is available
5. run tests

The CI workflow performs a similar sequence in GitHub Actions, including dependency installation, strict build enforcement, tests, and artifact upload.

This matters for two reasons. First, the manuscript is already part of an engineering release process rather than a detached prose document. Second, a chapter is not ready merely because it reads well. It must also survive the publication pipeline.

## 8.5 Publication And The Earlier Content Contracts

Publication depends on decisions made earlier in the book.

- Chapter 4 determines whether source content is structured enough to be transformed predictably
- Chapter 5 determines whether relationship-oriented metadata can support richer machine-facing outputs
- Chapter 6 determines whether identifiers and chunk structure survive into retrieval and delivery surfaces
- Chapter 7 determines whether the system can reject invalid content before it reaches readers

Publication is therefore a test of the whole architecture, not an independent subsystem.

## 8.6 Machine-Readable Publication

The current repository is primarily human-facing at publication time. The target platform described elsewhere in the book should also support stronger machine-readable publication.

That later layer would likely include:

- explicit stable identifiers in published pages
- governed metadata vocabularies
- JSON-LD embedded into HTML pages
- schema mappings suitable for external consumers or search engines

JSON-LD is useful here because it lets a page expose structured graph-like metadata without abandoning ordinary HTML. A vocabulary such as `schema.org` provides a practical web-facing naming system for that metadata.[^c8-jsonld][^c8-schemaorg]

The repository does not yet implement this layer. The architecture should still reserve a place for it.

## 8.7 Worked Example: One Chapter, Several Artifacts

A single manuscript chapter such as `content/04_authoring_etl.md` can appear as:

- a navigable HTML page in the docs site
- an EPUB section
- a PDF section
- source material for ETL-derived records elsewhere in the repository

That is why publication design cannot be reduced to theming. A well-formed chapter must:

- preserve heading hierarchy
- render predictably across output surfaces
- remain compatible with strict navigation rules
- avoid examples or claims that drift from the implementation

Publication places structural demands on the prose itself.

## 8.8 Publication Failure Modes

Even a repository of this size exposes several publication risks:

- navigation drift between content files and `mkdocs.yml`
- placeholder content reaching output artifacts
- export commands that depend on undocumented local tooling
- build success while the implementation slice has regressed

The repository mitigates these in modest but real ways:

- strict MkDocs builds
- test checks that reject placeholder text
- explicit build scripts and CI workflow steps
- publication and test execution in the same release path

These are not complete release controls, but they are genuine controls.

## 8.9 Release Criteria For A Chapter

At the level of the current repository, a chapter should be treated as publication-ready only when:

- it fits cleanly into the declared navigation structure
- it renders under `mkdocs build --strict`
- it contains no placeholder scaffolding
- its examples match the implementation or are marked as design targets
- it does not break EPUB or PDF export paths

This standard ties editorial quality to build integrity. That is the correct standard for a technical manual.

## 8.10 Current Limits

The publication layer does not yet provide:

- explicit JSON-LD or `schema.org` emission
- content-type-specific publication templates beyond the current MkDocs structure
- incremental rebuild logic for large corpora
- a publication path driven directly from normalized chunk records
- release metadata attached to machine-facing artifacts

These are sensible next-stage goals. They should be added only after the current build and manuscript boundary remain stable.

## 8.11 Why Publication Belongs In The Technical Spine

Publication is not the end of the system. It is where the rest of the system becomes observable.

If the content model is weak, publication exposes it. If source-of-truth policy is unclear, publication makes the ambiguity visible. If the build is not reproducible, publication is where the cost becomes real.

That is why publication belongs in a full chapter rather than in a short tooling appendix. It is one of the places where architecture stops being conceptual and starts being public.

## 8.12 Reading Notes

- **MkDocs Configuration Guide:** useful for understanding the site build as a declared configuration contract.
- **Pandoc User's Guide:** useful for EPUB and PDF export behavior and command-line options.
- **WeasyPrint Documentation:** useful for the HTML-to-PDF path and its styling assumptions.
- **JSON-LD 1.1:** useful for machine-readable publication.
- **schema.org:** useful for choosing practical web-facing metadata vocabularies.

[^c8-mkdocs]: MkDocs, *Configuration*: https://www.mkdocs.org/user-guide/configuration/
[^c8-pandoc]: Pandoc, *Pandoc User's Guide*: https://pandoc.org/MANUAL.html
[^c8-weasy]: WeasyPrint, *WeasyPrint documentation*: https://doc.courtbouillon.org/weasyprint/stable/
[^c8-jsonld]: W3C, *JSON-LD 1.1*: https://www.w3.org/TR/json-ld11/
[^c8-schemaorg]: Schema.org home page: https://schema.org/
