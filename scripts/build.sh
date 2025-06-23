#!/usr/bin/env bash

# Exit immediately if any command fails
set -e

echo "📦 Starting build process for Open Knowledge Systems..."

# Step 1: Clean build output
echo "🧹 Cleaning previous builds..."
rm -rf site/
rm -f open-knowledge-systems.epub open-knowledge-systems.pdf

# Step 2: Build HTML with MkDocs
echo "🌐 Building HTML site with MkDocs..."
mkdocs build

# Step 3: Build EPUB using Pandoc
if command -v pandoc >/dev/null 2>&1; then
    echo "📘 Building EPUB with Pandoc..."
    pandoc content/*.md -o open-knowledge-systems.epub \
        --metadata title="Open Knowledge Systems" \
        --metadata author="Final State Press" \
        --toc --epub-chapter-level=2
else
    echo "⚠️ Pandoc not found. Skipping EPUB generation."
fi

# Step 4: Build PDF with WeasyPrint (requires HTML build)
if command -v weasyprint >/dev/null 2>&1; then
    echo "🖨 Building PDF from site/index.html using WeasyPrint..."
    weasyprint site/index.html open-knowledge-systems.pdf
else
    echo "⚠️ WeasyPrint not found. Skipping PDF generation."
fi

# Step 5: Run tests
echo "✅ Running tests with pytest..."
pytest tests/ || {
    echo "❌ Tests failed!"
    exit 1
}

echo "🎉 Build complete!"
echo "📂 Output files:"
echo "  - site/ (HTML)"
echo "  - open-knowledge-systems.epub"
echo "  - open-knowledge-systems.pdf"