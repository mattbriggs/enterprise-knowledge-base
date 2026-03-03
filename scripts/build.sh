#!/usr/bin/env bash

# Exit immediately if any command fails
set -euo pipefail

echo "Starting build process for Open Knowledge Systems..."

book_dir="books"
epub_output="${book_dir}/open-knowledge-systems.epub"
pdf_output="${book_dir}/open-knowledge-systems.pdf"

if [ -x "$PWD/ENV/bin/python" ]; then
    python_bin="$PWD/ENV/bin/python"
elif command -v python >/dev/null 2>&1; then
    python_bin="$(command -v python)"
elif command -v python3 >/dev/null 2>&1; then
    python_bin="$(command -v python3)"
else
    echo "Python not found. Activate the virtualenv or install Python first." >&2
    exit 1
fi

# Step 1: Clean build output
echo "Cleaning previous builds..."
rm -rf site/
mkdir -p "${book_dir}"
rm -f "${epub_output}" "${pdf_output}"
rm -rf build/

# Step 2: Build HTML with MkDocs
echo "Building HTML site with MkDocs..."
"${python_bin}" -m mkdocs build --strict

# Step 3: Build EPUB using Pandoc
if command -v pandoc >/dev/null 2>&1; then
    echo "Building EPUB with Pandoc..."
    pandoc content/*.md -o "${epub_output}" \
        --metadata title="Open Knowledge Systems" \
        --metadata author="Final State Press" \
        --toc --epub-chapter-level=2
else
    echo "Pandoc not found. Skipping EPUB generation."
fi

# Step 4: Build PDF with WeasyPrint (requires HTML build)
if [ -x "$PWD/ENV/bin/weasyprint" ] || command -v weasyprint >/dev/null 2>&1; then
    echo "Building PDF from site/index.html using WeasyPrint..."
    scripts/weasyprint.sh site/index.html "${pdf_output}"
else
    echo "WeasyPrint not found. Skipping PDF generation."
fi

# Step 5: Run tests
echo "Running tests with pytest..."
"${python_bin}" -m pytest tests/ || {
    echo "Tests failed!"
    exit 1
}

echo "Build complete."
echo "Output files:"
echo "  - site/ (HTML)"
echo "  - ${epub_output}"
echo "  - ${pdf_output}"
