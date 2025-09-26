# Open Knowledge Systems

*A collaborative book and toolkit for building structured, intelligent enterprise knowledge systems using open-source technologies.*

![Build](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.10+-blue)

---

## Overview

This open-source project is both a book and a toolkit. It explores how to design, build, validate, and publish intelligent knowledge systems using tools like:

- **Markdown** for content
- **Python** for data processing
- **Neo4j** for knowledge graphs
- **MkDocs** for publishing
- **Jupyter Notebooks** for demonstrations

You'll learn how to:
- Create schema-driven modular content
- Store and retrieve content programmatically
- Model knowledge in Neo4j
- Validate your system's consistency
- Publish as HTML, EPUB, and PDF

---

##  Project Structure

```
.
├── content/                # Book chapters in Markdown
├── notebooks/             # Interactive Jupyter demos
├── scripts/               # Build & automation scripts
├── graphs/                # Neo4j schema & examples
├── tests/                 # Python unit tests
├── site/                  # HTML output from MkDocs
├── mkdocs.yml             # Site configuration
├── requirements.txt       # Python dependencies
├── LICENSE                # MIT License
└── README.md              # You're here!
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
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Building the Book

### 1. Serve HTML locally (live preview)

```bash
mkdocs serve
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) to view the site.

###  2. Build HTML static site

```bash
mkdocs build
```

Output is saved in the `/site/` folder.

---

## Create an EPUB

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

## Create a PDF

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

Test Python utilities, ETL, and validation logic:

```bash
pytest
```

---

## Tips for Maintenance

- Add new chapters in `content/NN_topic.md` and update `mkdocs.yml` nav.
- Use `scripts/build.sh` for repeatable builds (you can create this to wrap `mkdocs`, `pandoc`, and tests).
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

© 2025 Final State Press.
