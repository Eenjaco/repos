#!/usr/bin/env bash
# Helper script to append entry to markdown file in table format
# Called by Node.js tt script

WEEK_FILE="$1"
DATE="$2"
CATEGORY="$3"
SUBCATEGORY="$4"
START_TIME="$5"
END_TIME="$6"
DURATION="$7"
DESCRIPTION="$8"

# Get week number from filename (e.g., 2025_W45_time.md -> Week 45, 2025)
FILENAME=$(basename "$WEEK_FILE")
WEEK_NUM=$(echo "$FILENAME" | sed 's/.*_W\([0-9]*\)_.*/\1/')
YEAR=$(echo "$FILENAME" | sed 's/\([0-9]*\)_W.*/\1/')

# If file doesn't exist, create with header
if [ ! -f "$WEEK_FILE" ]; then
  {
    echo "# Time Log - Week $WEEK_NUM, $YEAR"
    echo ""
    echo "| Date | Category | Subcategory | Start | End | Duration | Description |"
    echo "|------|----------|-------------|-------|-----|----------|-------------|"
  } > "$WEEK_FILE"
fi

# Append table row
echo "| $DATE | $CATEGORY | $SUBCATEGORY | $START_TIME | $END_TIME | $DURATION | $DESCRIPTION |" >> "$WEEK_FILE"
