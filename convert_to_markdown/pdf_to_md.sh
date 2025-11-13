#!/usr/bin/env bash
# pdf_to_md.sh - Convert scanned PDF to markdown using OCR
# 
# Unix Philosophy: Do one thing well, compose with other tools
# Dependencies: tesseract, ghostscript (gs), pandoc
#
# Usage: ./pdf_to_md.sh input.pdf [output.md]

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Colors for output (optional, follows Unix convention)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

check_dependencies() {
    local missing=()
    
    for cmd in gs tesseract pandoc; do
        if ! command -v "$cmd" &> /dev/null; then
            missing+=("$cmd")
        fi
    done
    
    if [ ${#missing[@]} -ne 0 ]; then
        log_error "Missing required tools: ${missing[*]}"
        echo ""
        echo "Install on macOS with Homebrew:"
        echo "  brew install ghostscript tesseract pandoc"
        echo ""
        echo "Install on Linux (Debian/Ubuntu):"
        echo "  sudo apt install ghostscript tesseract-ocr pandoc"
        exit 1
    fi
}

# Main conversion function
convert_pdf_to_md() {
    local input_pdf="$1"
    local output_md="${2:-${input_pdf%.pdf}.md}"
    
    # Validate input
    if [[ ! -f "$input_pdf" ]]; then
        log_error "File not found: $input_pdf"
        exit 1
    fi
    
    log_info "Converting: $input_pdf → $output_md"
    
    # Create temp directory (Unix: use mktemp for safety)
    local temp_dir
    temp_dir=$(mktemp -d)
    trap "rm -rf '$temp_dir'" EXIT  # Cleanup on exit
    
    log_info "Created temporary directory: $temp_dir"
    
    # Step 1: Convert PDF pages to images
    log_info "Step 1/4: Extracting pages as images..."
    gs -dNOPAUSE -dBATCH -sDEVICE=png16m \
       -r300 \
       -sOutputFile="$temp_dir/page_%03d.png" \
       "$input_pdf" 2>/dev/null || {
        log_error "Failed to extract PDF pages"
        exit 1
    }
    
    local page_count
    page_count=$(find "$temp_dir" -name "page_*.png" | wc -l)
    log_info "Extracted $page_count pages"
    
    # Step 2: OCR each page
    log_info "Step 2/4: Running OCR on pages..."
    local ocr_output="$temp_dir/ocr_text.txt"
    > "$ocr_output"  # Create empty file
    
    for page in "$temp_dir"/page_*.png; do
        local page_num
        page_num=$(basename "$page" .png | sed 's/page_//')
        log_info "  OCR page $page_num..."
        
        # Tesseract outputs base filename, adds .txt automatically
        tesseract "$page" "$temp_dir/temp_ocr" -l eng --psm 3 2>/dev/null || {
            log_warn "OCR failed for page $page_num, skipping"
            continue
        }
        
        # Append with page marker
        echo "" >> "$ocr_output"
        echo "<!-- Page $page_num -->" >> "$ocr_output"
        echo "" >> "$ocr_output"
        cat "$temp_dir/temp_ocr.txt" >> "$ocr_output"
        rm -f "$temp_dir/temp_ocr.txt"
    done
    
    # Step 3: Convert to markdown
    log_info "Step 3/4: Converting to markdown..."
    
    # Add title and metadata
    {
        echo "# $(basename "$input_pdf" .pdf)"
        echo ""
        echo "> Converted from scanned PDF on $(date '+%Y-%m-%d')"
        echo ""
        cat "$ocr_output"
    } | pandoc -f plain -t markdown -o "$output_md" || {
        # If pandoc fails, just copy the text as-is with markdown header
        {
            echo "# $(basename "$input_pdf" .pdf)"
            echo ""
            echo "> Converted from scanned PDF on $(date '+%Y-%m-%d')"
            echo ""
            cat "$ocr_output"
        } > "$output_md"
    }
    
    # Step 4: Basic cleanup (optional)
    log_info "Step 4/4: Cleaning up..."
    
    # Remove multiple blank lines
    sed -i.bak '/^$/N;/^\n$/d' "$output_md" && rm -f "${output_md}.bak"
    
    log_info "✓ Conversion complete: $output_md"
    
    # Show preview
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "First 15 lines of output:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    head -n 15 "$output_md"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# Show usage
usage() {
    cat << EOF
Usage: $0 <input.pdf> [output.md]

Convert scanned PDF to markdown using OCR.

Arguments:
  input.pdf   Input PDF file (scanned document)
  output.md   Output markdown file (optional, defaults to input name)

Examples:
  $0 scan.pdf
  $0 scan.pdf notes.md

Requirements:
  - ghostscript (gs)  - PDF to image conversion
  - tesseract         - OCR engine
  - pandoc            - Format conversion

Tips for better OCR results:
  - Use high-resolution scans (300+ DPI)
  - Ensure text is clear and not skewed
  - Use good lighting for document scans

EOF
    exit 0
}

# Main script logic
main() {
    # Parse arguments
    if [[ $# -eq 0 ]] || [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
        usage
    fi
    
    # Check dependencies
    check_dependencies
    
    # Run conversion
    convert_pdf_to_md "$@"
}

# Run main function
main "$@"
