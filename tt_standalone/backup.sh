#!/bin/bash

# Time Tracker Database Backup Script
# Backs up timetracking.db with dated filename
# Keeps last 8 weeks of backups

# Colors for output
GREEN='\033[38;5;42m'
GREY='\033[38;5;240m'
RESET='\033[0m'

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Create backups directory if it doesn't exist
mkdir -p backups

# Generate backup filename with date
DATE=$(date +%Y-%m-%d)
BACKUP_FILE="backups/timetracking-${DATE}.db"

# Check if database exists
if [ ! -f "timetracking.db" ]; then
  echo "Error: timetracking.db not found"
  exit 1
fi

# Create backup
cp timetracking.db "$BACKUP_FILE"

if [ $? -eq 0 ]; then
  echo -e "${GREEN}✓${RESET} Database backed up: ${GREY}${BACKUP_FILE}${RESET}"

  # Get file size
  SIZE=$(ls -lh "$BACKUP_FILE" | awk '{print $5}')
  echo -e "  ${GREY}Size: ${SIZE}${RESET}"

  # Count entries
  ENTRIES=$(sqlite3 timetracking.db "SELECT COUNT(*) FROM time_entries;")
  echo -e "  ${GREY}Entries: ${ENTRIES}${RESET}"
else
  echo "Error: Backup failed"
  exit 1
fi

# Clean up old backups (keep last 8 weeks = ~56 days)
echo ""
echo -e "${GREY}Cleaning up old backups (keeping last 8 weeks)...${RESET}"

# Find and delete backups older than 56 days
find backups -name "timetracking-*.db" -type f -mtime +56 -delete

# Count remaining backups
BACKUP_COUNT=$(ls -1 backups/timetracking-*.db 2>/dev/null | wc -l | tr -d ' ')
echo -e "${GREY}Total backups: ${BACKUP_COUNT}${RESET}"

# List recent backups
if [ $BACKUP_COUNT -gt 0 ]; then
  echo ""
  echo -e "${GREY}Recent backups:${RESET}"
  ls -lht backups/timetracking-*.db | head -5 | awk '{print "  " $9 " (" $5 ")"}'
fi

echo ""
echo -e "${GREEN}✓ Backup complete${RESET}"
