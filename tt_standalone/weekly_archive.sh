#!/bin/bash
#
# Weekly Archive Script
# Copies current_task_timer.md to timelog_archive.md and clears current file
#
# Run this every Sunday to archive the week's timer entries
#
# Usage: ./weekly_archive.sh

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Paths
OBSIDIAN_BASE="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/Shared Vault/time_keeping"
CURRENT_TIMER="$OBSIDIAN_BASE/current_task_timer.md"
ARCHIVE="$OBSIDIAN_BASE/timelog_archive.md"
LOCAL_BACKUP="$HOME/Documents/Applications/tt_standalone/backups/timelog_archive_$(date +%Y%m%d).md"

echo -e "${BLUE}==================================${NC}"
echo -e "${BLUE}Weekly Time Log Archive${NC}"
echo -e "${BLUE}==================================${NC}"

# Check if current timer file exists
if [ ! -f "$CURRENT_TIMER" ]; then
    echo -e "${RED}Error: Current timer file not found${NC}"
    echo -e "  Expected: $CURRENT_TIMER"
    exit 1
fi

# Check if file is empty
if [ ! -s "$CURRENT_TIMER" ]; then
    echo -e "${YELLOW}Current timer file is empty - nothing to archive${NC}"
    exit 0
fi

# Get week info
WEEK_NUM=$(date +%V)
YEAR=$(date +%Y)
TODAY=$(date +"%d %b %Y")

echo -e "\n${BLUE}Week ${WEEK_NUM}, ${YEAR} (archived on ${TODAY})${NC}\n"

# Show what we're archiving
echo -e "${YELLOW}Entries to archive:${NC}"
grep -c "^———" "$CURRENT_TIMER" || ENTRY_COUNT=0
ENTRY_COUNT=$(grep -c "^———" "$CURRENT_TIMER" 2>/dev/null || echo "0")
echo -e "  ${GREEN}${ENTRY_COUNT}${NC} timer entries found"

# Process existing entries one last time
echo -e "\n${BLUE}Processing final sync to SQLite...${NC}"
python3 "$(dirname "$0")/parse_timer_format.py" "$CURRENT_TIMER"

# Create archive header
ARCHIVE_HEADER="

═══════════════════════════════════════════════════
Week ${WEEK_NUM}, ${YEAR} - Archived on ${TODAY}
═══════════════════════════════════════════════════

"

# Append to archive file
echo -e "\n${BLUE}Archiving to: timelog_archive.md${NC}"
echo "$ARCHIVE_HEADER" >> "$ARCHIVE"
cat "$CURRENT_TIMER" >> "$ARCHIVE"
echo -e "" >> "$ARCHIVE"  # Add blank line after

echo -e "${GREEN}✓${NC} Archived to timelog_archive.md"

# Create local backup
echo -e "\n${BLUE}Creating local backup...${NC}"
mkdir -p "$(dirname "$LOCAL_BACKUP")"
cp "$ARCHIVE" "$LOCAL_BACKUP"
echo -e "${GREEN}✓${NC} Backup saved to: $(basename "$LOCAL_BACKUP")"

# Clear current timer file
echo -e "\n${BLUE}Clearing current_task_timer.md for new week...${NC}"

# Keep a header in the cleared file
cat > "$CURRENT_TIMER" << EOF
# Current Task Timer

Week $(date +%V), $(date +%Y) - Started $(date +"%d %b %Y")

EOF

echo -e "${GREEN}✓${NC} Cleared current timer file"

# Summary
echo -e "\n${BLUE}==================================${NC}"
echo -e "${GREEN}✓ Archive Complete!${NC}"
echo -e "${BLUE}==================================${NC}"
echo -e "\n${BLUE}Summary:${NC}"
echo -e "  • Archived ${ENTRY_COUNT} entries"
echo -e "  • Saved to: ${GREEN}timelog_archive.md${NC}"
echo -e "  • Backed up: ${GREEN}$(basename "$LOCAL_BACKUP")${NC}"
echo -e "  • Cleared: ${GREEN}current_task_timer.md${NC}"
echo -e "\n${YELLOW}Ready for Week $(date -v+1d +%V)!${NC}\n"
