#!/usr/bin/env bash
# pdf_to_md_interactive.sh - Interactive PDF to Markdown converter
#
# Usage: Just run the script and follow the prompts

set -eo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

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

# Check dependencies
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
        echo "Install with: brew install ghostscript tesseract pandoc"
        exit 1
    fi
}

# Main conversion function
convert_pdf_to_md() {
    local input_pdf="$1"
    local output_md="$2"

    # Validate input
    if [[ ! -f "$input_pdf" ]]; then
        log_error "File not found: $input_pdf"
        exit 1
    fi

    log_info "Converting: $input_pdf → $output_md"

    # Create temp directory
    local temp_dir
    temp_dir=$(mktemp -d)
    trap "rm -rf '$temp_dir'" EXIT

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
    > "$ocr_output"

    for page in "$temp_dir"/page_*.png; do
        local page_num
        page_num=$(basename "$page" .png | sed 's/page_//')
        log_info "  OCR page $page_num..."

        tesseract "$page" "$temp_dir/temp_ocr" -l eng --psm 3 2>/dev/null || {
            log_warn "OCR failed for page $page_num, skipping"
            continue
        }

        echo "" >> "$ocr_output"
        echo "<!-- Page $page_num -->" >> "$ocr_output"
        echo "" >> "$ocr_output"
        cat "$temp_dir/temp_ocr.txt" >> "$ocr_output"
        rm -f "$temp_dir/temp_ocr.txt"
    done

    # Step 3: Convert to markdown
    log_info "Step 3/4: Converting to markdown..."

    {
        echo "# $(basename "$input_pdf" .pdf)"
        echo ""
        echo "> Converted from scanned PDF on $(date '+%Y-%m-%d')"
        echo ""
        cat "$ocr_output"
    } | pandoc -f plain -t markdown -o "$output_md" || {
        {
            echo "# $(basename "$input_pdf" .pdf)"
            echo ""
            echo "> Converted from scanned PDF on $(date '+%Y-%m-%d')"
            echo ""
            cat "$ocr_output"
        } > "$output_md"
    }

    # Step 4: Cleanup
    log_info "Step 4/4: Cleaning up..."
    sed -i.bak '/^$/N;/^\n$/d' "$output_md" && rm -f "${output_md}.bak"

    log_info "✓ Conversion complete: $output_md"

    # Show preview
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "First 15 lines of output:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    head -n 15 "$output_md"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo -e "${GREEN}Done! Press any key to exit...${NC}"
    read -n 1 -s
}

# Main interactive script
main() {
    echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║     PDF to Markdown - Interactive Converter    ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}"
    echo ""

    # Check dependencies
    check_dependencies

    # Prompt for input file
    echo -e "${YELLOW}Enter the full path to your PDF file:${NC}"
    echo -e "${YELLOW}(You can drag and drop the file into the terminal)${NC}"
    read -r input_pdf

    # Remove any surrounding quotes or whitespace
    input_pdf=$(echo "$input_pdf" | xargs)

    # Check if file exists
    if [[ ! -f "$input_pdf" ]]; then
        log_error "File not found: $input_pdf"
        echo ""
        echo "Press any key to exit..."
        read -n 1 -s
        exit 1
    fi

    echo ""
    log_info "Input file: $input_pdf"
    echo ""

    # Prompt for output location
    echo -e "${YELLOW}Enter the full path for the output markdown file:${NC}"
    echo -e "${YELLOW}(Example: /Users/mac/Documents/output.md)${NC}"
    echo -e "${YELLOW}Or press Enter to use same location as PDF${NC}"
    read -r output_md

    # Remove any surrounding quotes or whitespace
    output_md=$(echo "$output_md" | xargs)

    # If empty, use same directory as input with .md extension
    if [[ -z "$output_md" ]]; then
        output_md="${input_pdf%.pdf}.md"
    fi

    # If output doesn't end with .md, add it
    if [[ ! "$output_md" =~ \.md$ ]]; then
        output_md="${output_md}.md"
    fi

    echo ""
    log_info "Output file: $output_md"
    echo ""

    # Confirm
    echo -e "${YELLOW}Ready to convert?${NC}"
    echo "  Input:  $input_pdf"
    echo "  Output: $output_md"
    echo ""
    echo "Press Enter to continue or Ctrl+C to cancel..."
    read -r

    # Run conversion
    convert_pdf_to_md "$input_pdf" "$output_md"
}

# Run main
main
