#!/usr/bin/env python3
"""
Obsidian Timer Watcher
Watches current_task_timer.md in Obsidian vault and auto-syncs to SQLite

Monitors:
  /Users/mac/Library/Mobile Documents/iCloud~md~obsidian/Documents/Shared Vault/time_keeping/current_task_timer.md
"""

import time
import sys
import os
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from parse_timer_format import process_timer_file

# Colors
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
BLUE = '\033[0;34m'
NC = '\033[0m'

# Obsidian vault path
OBSIDIAN_TIMER_FILE = Path.home() / "Library/Mobile Documents/iCloud~md~obsidian/Documents/Shared Vault/time_keeping/current_task_timer.md"


class TimerFileHandler(FileSystemEventHandler):
    """Handles file system events for timer file"""

    def __init__(self, filepath):
        self.filepath = filepath
        self.last_processed = 0

    def on_modified(self, event):
        """Called when file is modified"""
        if event.is_directory:
            return

        if Path(event.src_path) == self.filepath:
            # Debounce: only process if 2 seconds have passed
            current_time = time.time()
            if current_time - self.last_processed < 2:
                return

            self.last_processed = current_time
            print(f"\n{BLUE}Detected change in: {self.filepath.name}{NC}")
            process_timer_file(str(self.filepath))


def main():
    """Main function to start the watcher"""
    print(f"{BLUE}=================================={NC}")
    print(f"{BLUE}Obsidian Timer Watcher{NC}")
    print(f"{BLUE}=================================={NC}")

    # Check if file exists
    if not OBSIDIAN_TIMER_FILE.exists():
        print(f"{YELLOW}Creating timer file: {OBSIDIAN_TIMER_FILE}{NC}")
        OBSIDIAN_TIMER_FILE.parent.mkdir(parents=True, exist_ok=True)
        OBSIDIAN_TIMER_FILE.touch()

    print(f"Watching: {OBSIDIAN_TIMER_FILE}")
    print(f"Press Ctrl+C to stop")
    print(f"{BLUE}=================================={NC}\n")

    # Process existing entries once
    print(f"{BLUE}Processing existing entries...{NC}")
    process_timer_file(str(OBSIDIAN_TIMER_FILE))

    # Start watching
    event_handler = TimerFileHandler(OBSIDIAN_TIMER_FILE)
    observer = Observer()
    observer.schedule(event_handler, str(OBSIDIAN_TIMER_FILE.parent), recursive=False)
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

    main()
