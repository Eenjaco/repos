#!/usr/bin/env python3
"""
Aster Inbox Watcher - Automatic document processing daemon

Monitors an iCloud Drive folder for new files and automatically processes them
with Aster, moving results to your Obsidian vault.

Usage:
    # Start watcher
    ./aster_watcher.py start

    # Run in foreground (for testing)
    ./aster_watcher.py run

    # Check status
    ./aster_watcher.py status

    # Stop watcher
    ./aster_watcher.py stop
"""

import sys
import time
import os
import re
import shutil
import hashlib
import json
import sqlite3
import subprocess
import signal
from pathlib import Path
from datetime import datetime
from queue import PriorityQueue
from threading import Thread, Event
from dataclasses import dataclass, asdict
from typing import Optional, Dict, List
import logging

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("❌ Error: watchdog not installed")
    print("Install with: pip install watchdog")
    sys.exit(1)

# =============================================================================
# Configuration
# =============================================================================

class Config:
    """Configuration for Aster Watcher"""

    # Folders
    INBOX = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/Aster/inbox"
    PROCESSING = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/Aster/processing"
    PROCESSED = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/Aster/processed"
    FAILED = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/Aster/failed"
    VAULT = Path.home() / "Library/Mobile Documents/iCloud~md~obsidian/Vault/Inbox"

    # State
    STATE_DIR = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/Aster/.aster-watcher"
    STATE_DB = STATE_DIR / "state.db"
    PID_FILE = STATE_DIR / "watcher.pid"
    LOG_FILE = STATE_DIR / "watcher.log"

    # Processing
    ASTER_SCRIPT = Path(__file__).parent / "aster.py"
    MODEL = "llama3.2:1b"
    CONCURRENT_JOBS = 1
    MAX_RETRIES = 3
    TIMEOUT = 300  # 5 minutes

    # Scheduling
    CHECK_INTERVAL = 5  # seconds
    IDLE_THRESHOLD = 120  # 2 minutes

    # Patterns for auto-priority
    PRIORITY_PATTERNS = {
        r'urgent_.*': 1,
        r'receipt_.*\.(jpg|png|pdf)': 1,
        r'meeting.*\.(jpg|png)': 2,
        r'whiteboard.*': 2,
        r'audio.*\.(mp3|m4a)': 2,
        r'.*\.docx': 3,
        r'.*\.csv': 3,
        r'book.*\.pdf': 4,
        r'.*\.epub': 4,
        r'archive_.*': 4,
        r'newsletter.*': 5,
        r'bulk_.*': 5,
    }

    @classmethod
    def ensure_directories(cls):
        """Create all required directories"""
        for folder in [cls.INBOX, cls.PROCESSING, cls.PROCESSED, cls.FAILED,
                      cls.VAULT, cls.STATE_DIR]:
            folder.mkdir(parents=True, exist_ok=True)

        # Create logs directory
        (cls.STATE_DIR / "logs").mkdir(exist_ok=True)

# =============================================================================
# Data Models
# =============================================================================

@dataclass
class Job:
    """Processing job"""
    file_path: Path
    priority: int
    added: datetime
    hash: str
    retries: int = 0
    status: str = "queued"  # queued, processing, complete, failed
    error: Optional[str] = None

    def __lt__(self, other):
        """For priority queue ordering"""
        if self.priority == other.priority:
            return self.added < other.added
        return self.priority < other.priority

# =============================================================================
# State Management
# =============================================================================

class StateManager:
    """Manages processing state and history"""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.conn = None
        self._init_db()

    def _init_db(self):
        """Initialize SQLite database"""
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS processed_files (
                hash TEXT PRIMARY KEY,
                filename TEXT,
                processed_at TEXT,
                status TEXT,
                output_path TEXT
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS processing_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                action TEXT,
                timestamp TEXT,
                details TEXT
            )
        """)
        self.conn.commit()

    def is_processed(self, file_hash: str) -> bool:
        """Check if file already processed"""
        cursor = self.conn.execute(
            "SELECT 1 FROM processed_files WHERE hash = ?",
            (file_hash,)
        )
        return cursor.fetchone() is not None

    def mark_processed(self, job: Job, output_path: Path):
        """Mark file as processed"""
        self.conn.execute("""
            INSERT OR REPLACE INTO processed_files
            (hash, filename, processed_at, status, output_path)
            VALUES (?, ?, ?, ?, ?)
        """, (
            job.hash,
            job.file_path.name,
            datetime.now().isoformat(),
            job.status,
            str(output_path)
        ))
        self.conn.commit()

    def log_action(self, filename: str, action: str, details: str = ""):
        """Log an action"""
        self.conn.execute("""
            INSERT INTO processing_log (filename, action, timestamp, details)
            VALUES (?, ?, ?, ?)
        """, (
            filename,
            action,
            datetime.now().isoformat(),
            details
        ))
        self.conn.commit()

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

# =============================================================================
# Queue Manager
# =============================================================================

class QueueManager:
    """Manages processing queue with priorities"""

    def __init__(self, state_manager: StateManager):
        self.queue = PriorityQueue()
        self.state = state_manager
        self.current_job = None
        self.stop_event = Event()

    def add_job(self, file_path: Path) -> Optional[Job]:
        """Add file to processing queue"""

        # Calculate file hash
        file_hash = self._hash_file(file_path)

        # Skip if already processed
        if self.state.is_processed(file_hash):
            logging.info(f"⏭️  Skipping {file_path.name} (already processed)")
            return None

        # Determine priority
        priority = self._get_priority(file_path)

        # Create job
        job = Job(
            file_path=file_path,
            priority=priority,
            added=datetime.now(),
            hash=file_hash
        )

        # Add to queue
        self.queue.put(job)
        self.state.log_action(file_path.name, "queued", f"priority={priority}")

        logging.info(f"📥 Queued: {file_path.name} (priority={priority})")
        return job

    def _hash_file(self, file_path: Path) -> str:
        """Calculate SHA256 hash of file"""
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                sha256.update(chunk)
        return sha256.hexdigest()

    def _get_priority(self, file_path: Path) -> int:
        """Determine priority based on filename patterns"""
        filename = file_path.name.lower()

        for pattern, priority in Config.PRIORITY_PATTERNS.items():
            if re.match(pattern, filename):
                return priority

        return 3  # Default: normal priority

    def get_next_job(self) -> Optional[Job]:
        """Get next job from queue (blocking)"""
        if self.stop_event.is_set():
            return None

        try:
            job = self.queue.get(timeout=1)
            self.current_job = job
            return job
        except:
            return None

    def stop(self):
        """Stop the queue"""
        self.stop_event.set()

# =============================================================================
# File Watcher
# =============================================================================

class InboxWatcher(FileSystemEventHandler):
    """Watches inbox folder for new files"""

    def __init__(self, queue_manager: QueueManager):
        self.queue_manager = queue_manager
        super().__init__()

    def on_created(self, event):
        """Handle new file creation"""
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Skip hidden files and queue.md
        if file_path.name.startswith('.') or file_path.name == 'queue.md':
            return

        # Wait for file to be fully written (iCloud sync)
        time.sleep(2)

        # Add to queue
        self.queue_manager.add_job(file_path)

# =============================================================================
# Processor
# =============================================================================

class Processor:
    """Processes files with Aster"""

    def __init__(self, queue_manager: QueueManager, state_manager: StateManager):
        self.queue = queue_manager
        self.state = state_manager

    def process_job(self, job: Job) -> bool:
        """Process a single job"""

        try:
            # Move to processing folder
            processing_path = Config.PROCESSING / job.file_path.name
            shutil.move(str(job.file_path), str(processing_path))
            job.file_path = processing_path
            job.status = "processing"

            logging.info(f"🔄 Processing: {job.file_path.name}")
            self.state.log_action(job.file_path.name, "processing_started")

            # Run Aster
            output_path = Config.VAULT / f"{job.file_path.stem}.md"

            cmd = [
                sys.executable,
                str(Config.ASTER_SCRIPT),
                str(job.file_path),
                "-o", str(output_path),
                "--model", Config.MODEL
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=Config.TIMEOUT
            )

            if result.returncode == 0 and output_path.exists():
                # Success!
                job.status = "complete"

                # Archive original
                archive_folder = Config.PROCESSED / datetime.now().strftime("%Y-%m")
                archive_folder.mkdir(parents=True, exist_ok=True)
                archive_path = archive_folder / job.file_path.name
                shutil.move(str(job.file_path), str(archive_path))

                # Update state
                self.state.mark_processed(job, output_path)
                self.state.log_action(
                    job.file_path.name,
                    "completed",
                    f"output={output_path.name}"
                )

                logging.info(f"✅ Completed: {job.file_path.name} → {output_path.name}")
                return True

            else:
                # Failed
                raise Exception(f"Aster failed: {result.stderr}")

        except Exception as e:
            # Handle failure
            job.status = "failed"
            job.error = str(e)
            job.retries += 1

            logging.error(f"❌ Failed: {job.file_path.name} - {e}")
            self.state.log_action(job.file_path.name, "failed", str(e))

            # Move to failed folder if max retries reached
            if job.retries >= Config.MAX_RETRIES:
                failed_path = Config.FAILED / job.file_path.name
                if job.file_path.exists():
                    shutil.move(str(job.file_path), str(failed_path))
                logging.error(f"💀 Max retries reached: {job.file_path.name}")
                return False

            # Retry
            logging.info(f"🔁 Retrying: {job.file_path.name} (attempt {job.retries + 1})")
            self.queue.queue.put(job)
            return False

    def run(self):
        """Main processing loop"""
        logging.info("🚀 Processor started")

        while not self.queue.stop_event.is_set():
            job = self.queue.get_next_job()
            if job:
                self.process_job(job)

        logging.info("⏹️  Processor stopped")

# =============================================================================
# Daemon
# =============================================================================

class WatcherDaemon:
    """Main watcher daemon"""

    def __init__(self):
        Config.ensure_directories()

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(Config.LOG_FILE),
                logging.StreamHandler()
            ]
        )

        # Initialize components
        self.state = StateManager(Config.STATE_DB)
        self.queue = QueueManager(self.state)
        self.processor = Processor(self.queue, self.state)

        # Watchdog observer
        self.observer = Observer()
        event_handler = InboxWatcher(self.queue)
        self.observer.schedule(event_handler, str(Config.INBOX), recursive=False)

        # Processing thread
        self.processor_thread = None

    def scan_existing_files(self):
        """Scan inbox for existing files on startup"""
        logging.info(f"📂 Scanning inbox: {Config.INBOX}")

        for file_path in Config.INBOX.iterdir():
            if file_path.is_file() and not file_path.name.startswith('.'):
                if file_path.name != 'queue.md':
                    self.queue.add_job(file_path)

    def start(self):
        """Start the watcher daemon"""
        logging.info("="*60)
        logging.info("✨ Aster Inbox Watcher Starting")
        logging.info("="*60)
        logging.info(f"📥 Watching: {Config.INBOX}")
        logging.info(f"📤 Output: {Config.VAULT}")
        logging.info(f"🧠 Model: {Config.MODEL}")
        logging.info("="*60)

        # Write PID file
        with open(Config.PID_FILE, 'w') as f:
            f.write(str(os.getpid()))

        # Scan existing files
        self.scan_existing_files()

        # Start processor thread
        self.processor_thread = Thread(target=self.processor.run, daemon=True)
        self.processor_thread.start()

        # Start file watcher
        self.observer.start()
        logging.info("👀 Watching for new files...")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """Stop the watcher daemon"""
        logging.info("\n⏹️  Stopping Aster Watcher...")

        # Stop queue
        self.queue.stop()

        # Stop observer
        self.observer.stop()
        self.observer.join()

        # Wait for processor
        if self.processor_thread:
            self.processor_thread.join(timeout=5)

        # Close state
        self.state.close()

        # Remove PID file
        if Config.PID_FILE.exists():
            Config.PID_FILE.unlink()

        logging.info("✅ Stopped")

# =============================================================================
# CLI
# =============================================================================

def main():
    """Main entry point"""

    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "run":
        # Run in foreground
        daemon = WatcherDaemon()
        daemon.start()

    elif command == "start":
        # Start as background daemon (TODO: proper daemonization)
        print("✨ Starting Aster Watcher...")
        print(f"📥 Inbox: {Config.INBOX}")
        print(f"📤 Output: {Config.VAULT}")
        print("\n💡 Tip: Run './aster_watcher.py run' to see live logs")
        print("\nFor now, run './aster_watcher.py run' in a separate terminal")
        print("Proper background daemon coming soon!")

    elif command == "stop":
        # Stop daemon
        if not Config.PID_FILE.exists():
            print("❌ Watcher not running")
            sys.exit(1)

        with open(Config.PID_FILE, 'r') as f:
            pid = int(f.read().strip())

        os.kill(pid, signal.SIGTERM)
        print("✅ Stopped")

    elif command == "status":
        # Show status
        if Config.PID_FILE.exists():
            with open(Config.PID_FILE, 'r') as f:
                pid = f.read().strip()
            print(f"✅ Watcher: Active (PID: {pid})")
        else:
            print("❌ Watcher: Not running")

        # Show queue size
        inbox_files = list(Config.INBOX.glob('*'))
        inbox_files = [f for f in inbox_files if f.is_file() and not f.name.startswith('.')]
        print(f"📥 Inbox: {len(inbox_files)} files")

    else:
        print(f"❌ Unknown command: {command}")
        print(__doc__)
        sys.exit(1)

if __name__ == '__main__':
    main()
