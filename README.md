# Open Knowledge Systems

*A technical manual and reference implementation slice for structured, machine-readable knowledge systems.*

![Build](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.10+-blue)

---

## Overview

This repository has two related layers:

- A technical manual describing the target Open Knowledge Systems architecture.
- A narrow reference implementation for schema-aware Markdown ETL.

The implementation is intentionally narrower than the target platform described in the book. The runnable code currently covers content parsing, front matter extraction, heading-based chunking, normalized JSON output, and a graph-friendly projection for Neo4j-oriented workflows.

The project uses:

- **Markdown** for content
- **Python** for data processing
- **Neo4j** for knowledge graphs
- **MkDocs** for publishing
- **Jupyter Notebooks** for demonstrations

The manual and code together focus on:

- Create schema-driven modular content
- Store and retrieve content programmatically
- Model knowledge in Neo4j
- Validate your system's consistency
- Publish as HTML, EPUB, and PDF

---

## Project Structure

```
.
├── content/                # Manuscript chapters in Markdown
├── content/notebooks/      # Notebook pages published with MkDocs
├── books/                  # Generated EPUB and PDF artifacts
├── graphs/                 # Neo4j schema and example Cypher
├── scripts/                # Build automation
├── src/oks/                # Reference implementation package
├── tests/                  # Unit and content sanity tests
├── mkdocs.yml              # Site configuration
├── pyproject.toml          # Package metadata and test config
├── requirements.txt        # Docs/build dependencies
├── LICENSE                 # MIT License
└── README.md               # Project overview
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/finalstatepress/open-knowledge-systems.git
cd open-knowledge-systems
```

### 2. Create a virtual environment

```bash
python3 -m venv ENV
source ENV/bin/activate
```

### 3. Install dependencies

```bash
ENV/bin/python -m pip install -r requirements.txt
ENV/bin/python -m pip install -e .
```

---

## Common Commands

### Serve the site locally

```bash
ENV/bin/python -m mkdocs serve
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) to review the manuscript locally.

### Build the HTML site

```bash
ENV/bin/python -m mkdocs build --strict
```

Output: `/site/`

### Run tests

```bash
ENV/bin/python -m pytest
```

### Run the ETL slice

Normalize the Markdown corpus into chunk records:

```bash
ENV/bin/python -m oks.etl content --output build/chunks.json
```

Generate both chunk and graph-oriented projections:

```bash
ENV/bin/python -m oks.etl content \
  --output build/chunks.json \
  --graph-output build/graph.json
```

### Build all publication artifacts

```bash
scripts/build.sh
```

Outputs:

- `/site/` for the HTML site
- `/books/open-knowledge-systems.epub` for the ebook
- `/books/open-knowledge-systems.pdf` for the PDF built from the Markdown chapters with Pandoc

---

## Export an EPUB

Use `pandoc` to convert the Markdown source into EPUB.

### Install Pandoc

macOS:

```bash
brew install pandoc
```

Ubuntu:

```bash
sudo apt install pandoc
```

### Convert to EPUB

```bash
pandoc content/*.md -o books/open-knowledge-systems.epub --metadata title="Open Knowledge Systems"
```

To include additional metadata:

```bash
pandoc content/*.md -o books/open-knowledge-systems.epub \
  --metadata title="Open Knowledge Systems" \
  --metadata author="Final State Press" \
  --epub-cover-image=assets/cover.png
```

---

## Export a PDF

PDF output depends on your system's LaTeX or HTML rendering setup. Two options:

### Option 1: via Pandoc + LaTeX (default book build)

```bash
pandoc content/*.md -o books/open-knowledge-systems.pdf \
  --metadata title="Open Knowledge Systems" \
  --metadata author="Final State Press" \
  --toc --pdf-engine=xelatex
```

If LaTeX is not installed:

macOS:

```bash
brew install --cask mactex-no-gui
```

Ubuntu:

```bash
sudo apt install texlive texlive-xetex texlive-fonts-recommended
```

### Option 2: via `weasyprint` (HTML snapshot, not the full multi-page book)

```bash
ENV/bin/python -m pip install weasyprint

# macOS native libraries
brew install glib pango libffi

# build the HTML site first, then convert it
ENV/bin/python -m mkdocs build --strict
scripts/weasyprint.sh site/index.html books/open-knowledge-systems.pdf
```

`scripts/weasyprint.sh` configures Homebrew library lookup on macOS and a writable font cache directory.

---

## Maintenance Notes

- Add new chapters in `content/NN_topic.md` and update `mkdocs.yml` navigation.
- Use `scripts/build.sh` for repeatable builds.
- Treat `/books/` as generated release output; keep only `books/.gitkeep` under version control.
- Keep prose claims aligned with the implementation boundary.
- Run `black`, `flake8`, or `pytest` before releasing.
- Use GitHub Issues and PRs for contributions.

---

## Create a Release

Recommended flow:

1. Activate the environment and run `scripts/build.sh`.
2. Confirm the release artifacts exist at `books/open-knowledge-systems.epub` and `books/open-knowledge-systems.pdf`.
3. Run `ENV/bin/python -m pytest` if you have not already done so in this release cycle.
4. Commit and push the source changes you want in the release.
5. Create and push a tag, for example:

```bash
git tag -a v0.1.0 -m "Open Knowledge Systems v0.1.0"
git push origin v0.1.0
```

6. In GitHub, open `Releases` for the repository and create a new release from that tag.
7. Upload `books/open-knowledge-systems.epub` and `books/open-knowledge-systems.pdf` as release assets.

If you use the GitHub CLI, you can create the release from the terminal after building:

```bash
gh release create v0.1.0 \
  books/open-knowledge-systems.epub \
  books/open-knowledge-systems.pdf \
  --title "Open Knowledge Systems v0.1.0" \
  --notes "Release notes go here."
```

---

## Contributing

We welcome issues, suggestions, and pull requests!

1. Fork the repo
2. Create a branch
3. Make your changes and run the relevant checks
4. Open a PR

Please follow [semantic commit messages](https://www.conventionalcommits.org/) and write tests for new functionality.

---

## License

This project is licensed under the MIT License. See [LICENSE](./LICENSE) for full terms.

© 2026 Final State Press.
