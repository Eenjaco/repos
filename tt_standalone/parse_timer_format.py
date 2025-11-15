#!/usr/bin/env python3
"""
Timer Format Parser for Watchdog
Parses the Apple Notes-style timer format and syncs to SQLite

Format:
———
Category
Subcategory
Start time: 13 Nov 2025 at 11:04:13
until
End Time: 14 Nov 2025 at 13:08:33
"""

import re
import sqlite3
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
DB_PATH = SCRIPT_DIR / 'timetracking.db'

# Colors
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
BLUE = '\033[0;34m'
NC = '\033[0m'


def parse_timer_entries(content):
    """Parse Apple Notes style timer format"""
    entries = []

    # Split by ———
    blocks = re.split(r'———+', content)

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        lines = [l.strip() for l in block.split('\n') if l.strip()]
        if len(lines) < 3:
            continue

        # Parse structure
        category = lines[0] if len(lines) > 0 else ""
        subcategory = lines[1] if len(lines) > 1 else ""

        # Find start and end times
        start_time = None
        end_time = None

        for line in lines:
            if line.startswith("Start time:"):
                start_match = re.search(r'Start time:\s*(.+?)(?:\s+until)?$', line)
                if start_match:
                    start_time = start_match.group(1).strip()
            elif line.startswith("End Time:"):
                end_match = re.search(r'End Time:\s*(.+)$', line)
                if end_match:
                    end_time = end_match.group(1).strip()

        # Skip if no start time or still running (ends with "until")
        if not start_time:
            continue
        if not end_time:
            print(f"{YELLOW}⏱️  Timer still running: {category} / {subcategory}{NC}")
            continue

        # Parse dates
        try:
            # Format: "13 Nov 2025 at 11:04:13"
            start_dt = datetime.strptime(start_time, "%d %b %Y at %H:%M:%S")
            end_dt = datetime.strptime(end_time, "%d %b %Y at %H:%M:%S")

            # Calculate duration
            duration_seconds = (end_dt - start_dt).total_seconds()
            duration_minutes = int(duration_seconds / 60)

            entry = {
                'category': category,
                'subcategory': subcategory,
                'start_time': start_dt.strftime("%H:%M:%S"),
                'end_time': end_dt.strftime("%H:%M:%S"),
                'date': start_dt.strftime("%Y-%m-%d"),
                'duration_minutes': duration_minutes,
                'description': ''
            }

            entries.append(entry)

        except ValueError as e:
            print(f"{RED}Error parsing dates: {e}{NC}")
            print(f"  Start: {start_time}")
            print(f"  End: {end_time}")
            continue

    return entries


def insert_entry(entry):
    """Insert entry into SQLite database"""
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()

        # Check for duplicates
        cursor.execute("""
            SELECT COUNT(*) FROM time_entries
            WHERE date = ? AND category = ? AND subcategory = ?
            AND start_time = ? AND end_time = ?
        """, (entry['date'], entry['category'], entry['subcategory'],
              entry['start_time'], entry['end_time']))

        if cursor.fetchone()[0] > 0:
            conn.close()
            return False  # Already exists

        # Insert new entry
        cursor.execute("""
            INSERT INTO time_entries
            (date, category, subcategory, start_time, end_time, duration_minutes, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (entry['date'], entry['category'], entry['subcategory'],
              entry['start_time'], entry['end_time'], entry['duration_minutes'],
              entry['description']))

        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print(f"{RED}Error inserting entry: {e}{NC}")
        return False


def process_timer_file(filepath):
    """Process the current_task_timer.md file"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()

        entries = parse_timer_entries(content)

        new_count = 0
        for entry in entries:
            if insert_entry(entry):
                new_count += 1
                hours = entry['duration_minutes'] // 60
                mins = entry['duration_minutes'] % 60
                duration_str = f"{hours}h {mins}m" if hours > 0 else f"{mins}m"
                print(f"{GREEN}✓{NC} Added: {entry['date']} | {entry['category']} / {entry['subcategory']} | {duration_str}")

        if new_count == 0:
            print(f"  No new entries")
        else:
            print(f"{GREEN}✓{NC} Imported {new_count} new entries")

        return new_count

    except Exception as e:
        print(f"{RED}Error processing file: {e}{NC}")
        return 0


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 parse_timer_format.py <path_to_current_task_timer.md>")
        sys.exit(1)

    filepath = sys.argv[1]
    process_timer_file(filepath)
