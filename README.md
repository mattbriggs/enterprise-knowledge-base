# Open Knowledge Systems

*A technical manual and reference implementation slice for structured, machine-readable knowledge systems.*

![Build](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.10+-blue)

---

## Overview

This repository currently has two related layers:

- A technical manual describing the target Open Knowledge Systems architecture.
- A narrow reference implementation for schema-aware Markdown ETL.

The implementation is intentionally narrower than the target platform described in the book. Today the runnable code covers content parsing, front matter extraction, heading-based chunking, normalized JSON output, and a graph-friendly projection for Neo4j-oriented workflows.

The project explores how to design, build, validate, and publish knowledge systems using tools like:

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

### 2. Set up a Python environment

```bash
python3 -m venv ENV
source ENV/bin/activate  # On Windows: ENV\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

---

## Building the Book

### 1. Serve HTML locally (live preview)

```bash
mkdocs serve
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) to review the manuscript locally.

###  2. Build HTML static site

```bash
mkdocs build --strict
```

Output is saved in the `/site/` folder.

---

## Export an EPUB

Use `pandoc` to convert the Markdown source into `.epub`.

### Install Pandoc

Mac:  
```bash
brew install pandoc
```

Ubuntu:  
```bash
sudo apt install pandoc
```

### Convert to EPUB

```bash
pandoc content/*.md -o open-knowledge-systems.epub --metadata title="Open Knowledge Systems"
```

To include cover image and metadata, modify:
```bash
pandoc content/*.md -o open-knowledge-systems.epub \
  --metadata title="Open Knowledge Systems" \
  --metadata author="Final State Press" \
  --epub-cover-image=assets/cover.png
```

---

## Export a PDF

PDF output depends on your system's LaTeX or HTML rendering setup. Two options:

### Option 1: via `weasyprint` (recommended for styled output)

```bash
pip install weasyprint
weasyprint site/index.html open-knowledge-systems.pdf
```

### Option 2: via Pandoc + LaTeX

```bash
pandoc content/*.md -o open-knowledge-systems.pdf
```

If LaTeX is not installed:
```bash
sudo apt install texlive texlive-xetex texlive-fonts-recommended
```

---

## Run Tests

Run the implementation and manuscript quality checks:

```bash
pytest
```

## Run the ETL Slice

Normalize the Markdown corpus into chunk records:

```bash
python -m oks.etl content --output build/chunks.json
```

Generate both chunk and graph-oriented projections:

```bash
python -m oks.etl content \
  --output build/chunks.json \
  --graph-output build/graph.json
```

---

## Maintenance Notes

- Add new chapters in `content/NN_topic.md` and update `mkdocs.yml` navigation.
- Use `scripts/build.sh` for repeatable builds.
- Keep prose claims aligned with the implementation boundary.
- Run `black` or `flake8` for code style checks.
- Use GitHub Issues and PRs for contributions.

---

## Contributing

We welcome issues, suggestions, and pull requests!

1. Fork the repo
2. Create a branch
3. Commit your changes
4. Open a PR

Please follow [semantic commit messages](https://www.conventionalcommits.org/) and write tests for new functionality.

---

## License

This project is licensed under the MIT License. See [LICENSE](./LICENSE) for full terms.

© 2026 Final State Press.
