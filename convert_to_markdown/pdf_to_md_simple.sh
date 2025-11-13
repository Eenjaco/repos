#!/usr/bin/env bash
# pdf_to_md_simple.sh - Simpler OCR PDF to markdown conversion
# 
# Uses ocrmypdf for better integration
# Unix Philosophy: Leverage existing specialized tools
#
# Usage: ./pdf_to_md_simple.sh input.pdf [output.md]

set -euo pipefail

# Check for ocrmypdf and pandoc
if ! command -v ocrmypdf &> /dev/null; then
    echo "Error: ocrmypdf not found"
    echo "Install on macOS: brew install ocrmypdf"
    echo "Install on Linux: sudo apt install ocrmypdf"
    exit 1
fi

if ! command -v pandoc &> /dev/null; then
    echo "Error: pandoc not found"
    echo "Install: brew install pandoc (macOS) or sudo apt install pandoc (Linux)"
    exit 1
fi

# Parse arguments
INPUT_PDF="${1:?Usage: $0 input.pdf [output.md]}"
OUTPUT_MD="${2:-${INPUT_PDF%.pdf}.md}"

if [[ ! -f "$INPUT_PDF" ]]; then
    echo "Error: File not found: $INPUT_PDF"
    exit 1
fi

echo "[1/3] Running OCR on PDF..."
TEMP_PDF=$(mktemp).pdf
ocrmypdf --force-ocr --output-type pdf "$INPUT_PDF" "$TEMP_PDF" 2>/dev/null || {
    echo "Error: OCR failed"
    rm -f "$TEMP_PDF"
    exit 1
}

echo "[2/3] Extracting text..."
TEMP_TXT=$(mktemp).txt
pdftotext "$TEMP_PDF" "$TEMP_TXT" || {
    echo "Error: Text extraction failed"
    rm -f "$TEMP_PDF" "$TEMP_TXT"
    exit 1
}

echo "[3/3] Converting to markdown..."
{
    echo "# $(basename "$INPUT_PDF" .pdf)"
    echo ""
    echo "> Converted from scanned PDF on $(date '+%Y-%m-%d')"
    echo "> Original: $INPUT_PDF"
    echo ""
    cat "$TEMP_TXT"
} > "$OUTPUT_MD"

# Cleanup
rm -f "$TEMP_PDF" "$TEMP_TXT"

echo "✓ Done: $OUTPUT_MD"
echo ""
head -n 15 "$OUTPUT_MD"
