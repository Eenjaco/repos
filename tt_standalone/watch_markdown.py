#!/usr/bin/env python3
"""
Markdown File Watcher for Time Tracker
Watches time_logs/*.md files for changes and auto-syncs to SQLite

Features:
- Monitors time_logs directory for markdown changes
- Parses markdown table format
- Inserts new entries into SQLite database
- Avoids duplicate entries
- Runs as background daemon

Usage:
    python3 watch_markdown.py
    python3 watch_markdown.py --daemon  # Run in background
"""

import time
import re
import sqlite3
import sys
import os
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Get script directory
SCRIPT_DIR = Path(__file__).parent.resolve()
DB_PATH = SCRIPT_DIR / 'timetracking.db'
LOGS_DIR = SCRIPT_DIR / 'time_logs'

# Colors for output
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color


class MarkdownTimeLogHandler(FileSystemEventHandler):
    """Handles file system events for markdown time log files"""

    def __init__(self):
        self.processed_entries = set()
        self.load_existing_entries()

    def load_existing_entries(self):
        """Load existing entries from database to avoid duplicates"""
        try:
            conn = sqlite3.connect(str(DB_PATH))
            cursor = conn.cursor()

            # Get all existing entries as a unique key
            cursor.execute("""
                SELECT date, category, subcategory, start_time, end_time
                FROM time_entries
            """)

            for row in cursor.fetchall():
                key = self.make_entry_key(*row)
                self.processed_entries.add(key)

            conn.close()
            print(f"{GREEN}✓{NC} Loaded {len(self.processed_entries)} existing entries from database")
        except Exception as e:
            print(f"{RED}Error loading existing entries: {e}{NC}")

    def make_entry_key(self, date, category, subcategory, start_time, end_time):
        """Create unique key for entry to detect duplicates"""
        return f"{date}|{category}|{subcategory}|{start_time}|{end_time}"

    def on_modified(self, event):
        """Called when a file is modified"""
        if event.is_directory:
            return

        if event.src_path.endswith('.md'):
            print(f"{BLUE}Detected change in: {os.path.basename(event.src_path)}{NC}")
            self.process_markdown_file(event.src_path)

    def on_created(self, event):
        """Called when a file is created"""
        if event.is_directory:
            return

        if event.src_path.endswith('.md'):
            print(f"{BLUE}New file created: {os.path.basename(event.src_path)}{NC}")
            self.process_markdown_file(event.src_path)

    def process_markdown_file(self, filepath):
        """Parse markdown file and insert new entries to database"""
        try:
            with open(filepath, 'r') as f:
                content = f.read()

            # Parse markdown table rows
            # Format: | Date | Category | Subcategory | Start | End | Duration | Description |
            pattern = r'\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|'

            new_entries = 0
            for match in re.finditer(pattern, content):
                date, category, subcategory, start, end, duration, description = match.groups()

                # Skip header row
                if 'Date' in date or '---' in date:
                    continue

                # Check if already processed
                entry_key = self.make_entry_key(date, category, subcategory, start, end)
                if entry_key in self.processed_entries:
                    continue

                # Parse duration (convert to minutes)
                duration_minutes = self.parse_duration(duration)

                # Insert to database
                if self.insert_entry(date, category, subcategory, start, end, duration_minutes, description):
                    self.processed_entries.add(entry_key)
                    new_entries += 1
                    print(f"{GREEN}✓{NC} Added: {date} | {category} | {subcategory} | {duration}")

            if new_entries == 0:
                print(f"  No new entries found")
            else:
                print(f"{GREEN}✓{NC} Imported {new_entries} new entries")

        except Exception as e:
            print(f"{RED}Error processing file: {e}{NC}")

    def parse_duration(self, duration_str):
        """Convert duration string to minutes"""
        # Try to extract hours and minutes
        duration_str = duration_str.strip()

        # Format: "2h 30m" or "2.5h" or "90m" or "90"
        hours = 0
        minutes = 0

        # Check for "Xh Ym" format
        h_match = re.search(r'(\d+)h', duration_str)
        m_match = re.search(r'(\d+)m', duration_str)

        if h_match:
            hours = int(h_match.group(1))
        if m_match:
            minutes = int(m_match.group(1))

        # Check for decimal hours: "2.5h"
        if 'h' in duration_str and '.' in duration_str:
            decimal_hours = float(re.search(r'([\d.]+)h', duration_str).group(1))
            return int(decimal_hours * 60)

        # If only minutes or plain number
        if not h_match and not m_match:
            # Assume it's minutes
            minutes = int(re.search(r'(\d+)', duration_str).group(1))

        return hours * 60 + minutes

    def insert_entry(self, date, category, subcategory, start_time, end_time, duration_minutes, description):
        """Insert entry into SQLite database"""
        try:
            conn = sqlite3.connect(str(DB_PATH))
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO time_entries
                (date, category, subcategory, start_time, end_time, duration_minutes, description)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (date, category, subcategory, start_time, end_time, duration_minutes, description))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            print(f"{RED}Error inserting entry: {e}{NC}")
            return False


def main():
    """Main function to start the watcher"""
    print(f"{BLUE}=================================={NC}")
    print(f"{BLUE}Time Tracker Markdown Watcher{NC}")
    print(f"{BLUE}=================================={NC}")
    print(f"Watching: {LOGS_DIR}")
    print(f"Database: {DB_PATH}")
    print(f"Press Ctrl+C to stop")
    print(f"{BLUE}=================================={NC}\n")

    # Create observer
    event_handler = MarkdownTimeLogHandler()
    observer = Observer()
    observer.schedule(event_handler, str(LOGS_DIR), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Stopping watcher...{NC}")
        observer.stop()

    observer.join()
    print(f"{GREEN}✓{NC} Watcher stopped")


if __name__ == "__main__":
    # Check if watchdog is installed
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except ImportError:
        print(f"{RED}Error: watchdog package not installed{NC}")
        print(f"Run: pip install watchdog")
        sys.exit(1)

    # Check if database exists
    if not DB_PATH.exists():
        print(f"{RED}Error: Database not found at {DB_PATH}{NC}")
        sys.exit(1)

    # Check if time_logs directory exists
    if not LOGS_DIR.exists():
        print(f"{YELLOW}Creating time_logs directory...{NC}")
        LOGS_DIR.mkdir(parents=True, exist_ok=True)

    main()
