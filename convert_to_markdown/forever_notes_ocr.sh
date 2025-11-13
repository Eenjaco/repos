#!/usr/bin/env bash
# forever_notes_ocr.sh - Integrate scanned notes with Forever Notes Journal
#
# Usage: 
#   ./forever_notes_ocr.sh scan.pdf              # Add to today
#   ./forever_notes_ocr.sh scan.pdf 2025-11-05   # Add to specific date
#
# This script:
# 1. Converts scanned PDF to markdown using OCR
# 2. Appends content to the correct Forever Notes daily file
# 3. Preserves existing structure

set -euo pipefail

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Configuration - EDIT THESE FOR YOUR SETUP
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VAULT_PATH="$HOME/Notes/ObsidianVault/Journal"
YEAR="2025"  # Current year for Forever Notes

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1" >&2; }

# Check if PDF to MD script exists
if [[ ! -f "./pdf_to_md.sh" ]]; then
    log_error "pdf_to_md.sh not found in current directory"
    exit 1
fi

# Parse arguments
INPUT_PDF="${1:?Usage: $0 scan.pdf [YYYY-MM-DD]}"
TARGET_DATE="${2:-$(date +%Y-%m-%d)}"

if [[ ! -f "$INPUT_PDF" ]]; then
    log_error "File not found: $INPUT_PDF"
    exit 1
fi

# Convert date format: 2025-11-03 → nov_03
month_abbr=$(date -d "$TARGET_DATE" +%b 2>/dev/null || date -j -f "%Y-%m-%d" "$TARGET_DATE" +%b)
day_num=$(date -d "$TARGET_DATE" +%d 2>/dev/null || date -j -f "%Y-%m-%d" "$TARGET_DATE" +%d)
month_abbr_lower=$(echo "$month_abbr" | tr '[:upper:]' '[:lower:]')
forever_note="${month_abbr_lower}_${day_num}"

DAILY_NOTE="$VAULT_PATH/${forever_note}.md"

if [[ ! -f "$DAILY_NOTE" ]]; then
    log_error "Daily note not found: $DAILY_NOTE"
    log_error "Expected format: ${forever_note}.md"
    exit 1
fi

log_info "Target: $DAILY_NOTE"

# Convert PDF to markdown
TEMP_MD=$(mktemp).md
log_info "Converting PDF to markdown..."
./pdf_to_md.sh "$INPUT_PDF" "$TEMP_MD" > /dev/null 2>&1 || {
    log_error "OCR conversion failed"
    exit 1
}

# Extract just the content (skip title and metadata from OCR output)
CONTENT=$(sed '1,/^>/d' "$TEMP_MD" | sed '/^$/d')

if [[ -z "$CONTENT" ]]; then
    log_error "No content extracted from PDF"
    rm -f "$TEMP_MD"
    exit 1
fi

# Create backup
cp "$DAILY_NOTE" "${DAILY_NOTE}.backup"
log_info "Created backup: ${DAILY_NOTE}.backup"

# Append to the YEAR section
# Find the ## YEAR section and add content under Notes
log_info "Appending content to $YEAR section..."

# Use awk to insert after "- Notes:" line in the correct year section
awk -v year="$YEAR" -v content="$CONTENT" '
    /^## / { current_year = $2 }
    /^- Notes:/ && current_year == year {
        print
        print "  - 📄 Scanned notes from: '"$(basename "$INPUT_PDF")"'"
        while (getline line < "/dev/stdin") {
            gsub(/^/, "    ", line)
            print line
        }
        next
    }
    { print }
' "$DAILY_NOTE" > "${DAILY_NOTE}.tmp"

# If content was added, replace the file
if grep -q "Scanned notes from:" "${DAILY_NOTE}.tmp"; then
    mv "${DAILY_NOTE}.tmp" "$DAILY_NOTE"
    log_info "✓ Content added to $forever_note.md"
else
    # Fallback: append to end of year section
    log_info "Using fallback method..."
    
    # Find the ## YEAR section and append before next ## or end
    sed -i.bak "/^## $YEAR/,/^## [0-9]\{4\}\|^## Metadata/ {
        /^- Notes:/a\\
  - 📄 Scanned notes from: $(basename "$INPUT_PDF")\\
$(echo "$CONTENT" | sed 's/^/    /')
    }" "$DAILY_NOTE"
    
    log_info "✓ Content appended to $YEAR section"
fi

# Cleanup
rm -f "$TEMP_MD" "${DAILY_NOTE}.tmp" "${DAILY_NOTE}.bak"

# Show preview
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Preview of $forever_note.md ($YEAR section):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
sed -n "/^## $YEAR/,/^## [0-9]\{4\}\|^## Metadata/p" "$DAILY_NOTE" | head -n 20
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
log_info "Done! Open in Obsidian to review."
log_info "Backup available at: ${DAILY_NOTE}.backup"

# Offer to cleanup backup
read -p "Delete backup? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -f "${DAILY_NOTE}.backup"
    log_info "Backup deleted"
fi
