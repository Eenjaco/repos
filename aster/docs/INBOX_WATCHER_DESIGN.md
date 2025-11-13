# Aster Inbox Watcher - Design Document

## 🎯 Concept

**Goal:** Seamless iPhone → iCloud Drive → Aster → Obsidian workflow with zero manual intervention.

**User Story:**
1. Take photo/save file on iPhone
2. Share to iCloud "Aster Inbox" folder
3. Desktop automatically detects and processes
4. Processed markdown appears in Obsidian vault
5. Original archived automatically

**Key Advantage:** Works anywhere (not limited to WiFi like web interface)

---

## 🏗️ Architecture

### Components

```
┌─────────────────────────────────────────────────────────────┐
│  iPhone                                                       │
│  - Take photo / Save file                                    │
│  - Share to "Aster Inbox" folder (iCloud Drive)             │
└───────────────────┬─────────────────────────────────────────┘
                    │
                    │ iCloud Sync
                    ▼
┌─────────────────────────────────────────────────────────────┐
│  iCloud Drive Folder                                         │
│  ~/Library/Mobile Documents/com~apple~CloudDocs/Aster/      │
│                                                              │
│  ├── inbox/           ← Drop files here                     │
│  ├── processing/      ← Files being processed               │
│  ├── processed/       ← Completed originals                 │
│  ├── failed/          ← Failed processing                   │
│  ├── queue.md         ← Status & configuration              │
│  └── .aster-watcher   ← Watcher state/logs                  │
└───────────────────┬─────────────────────────────────────────┘
                    │
                    │ Watchdog monitors
                    ▼
┌─────────────────────────────────────────────────────────────┐
│  Aster Inbox Watcher (Mac daemon)                           │
│  - Detects new files                                         │
│  - Reads priority from queue.md                              │
│  - Queues processing jobs                                    │
│  - Updates status in real-time                               │
└───────────────────┬─────────────────────────────────────────┘
                    │
                    │ Process with Aster
                    ▼
┌─────────────────────────────────────────────────────────────┐
│  Aster Processing                                            │
│  - Extract → Structure → Clean → Connect                    │
│  - Ollama processing with llama3.2:1b                        │
└───────────────────┬─────────────────────────────────────────┘
                    │
                    │ Save output
                    ▼
┌─────────────────────────────────────────────────────────────┐
│  Obsidian Vault (iCloud synced)                             │
│  ~/Library/Mobile Documents/iCloud~md~obsidian/Vault/       │
│  └── Inbox/ ← Processed markdown files appear here          │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 Queue System Design

### Priority Levels

```python
PRIORITY = {
    "urgent": 1,      # Process immediately
    "high": 2,        # Process within 5 minutes
    "normal": 3,      # Process when idle
    "low": 4,         # Process overnight
    "batch": 5        # Process during scheduled batch time
}
```

### Queue Document (`queue.md`)

Located in iCloud folder, edited from iPhone or Mac:

```markdown
# Aster Processing Queue

## Status
- **Watching**: ✅ Active
- **Last Check**: 2025-11-13 15:30:22
- **Queue Size**: 3 files
- **Processing**: receipt_20251113.jpg

## Priority Rules

### Urgent (Process Immediately)
- receipt_*.jpg, receipt_*.pdf
- meeting_notes_*.jpg
- urgent_*.*

### High (Within 5 minutes)
- whiteboard_*.jpg
- audio_*.mp3, *.m4a
- *.docx (work documents)

### Normal (When idle)
- book_*.pdf, *.epub
- article_*.pdf
- *.csv

### Low (Overnight)
- archive_*.*
- old_*.*

### Batch (Scheduled: 2am)
- newsletter_*.pdf
- bulk_*.*

## Current Queue

| File | Priority | Status | Started | ETA |
|------|----------|--------|---------|-----|
| receipt_20251113.jpg | urgent | processing | 15:30 | 1 min |
| meeting_notes.jpg | high | queued | - | 5 min |
| Deep_Work_Ch3.pdf | normal | queued | - | pending |

## Completed Today

- ✅ whiteboard_standup.jpg → Obsidian/Meetings/ (15:25)
- ✅ expenses_nov.csv → Obsidian/Finance/ (14:10)
- ✅ sermon_notes.docx → Obsidian/Religious/ (13:45)

## Failed

- ❌ corrupted_image.jpg - Error: Cannot read file
```

---

## 🔧 Implementation

### Technology Stack

**File Watching:**
- `watchdog` (Python library) - Cross-platform file system monitoring
- Monitors `~/Library/Mobile Documents/com~apple~CloudDocs/Aster/inbox/`

**Queue Management:**
- `queue.PriorityQueue` - Thread-safe priority queue
- Custom job scheduler

**Configuration:**
- `queue.md` - Human-editable markdown in inbox folder
- Auto-reload on change
- LLM can update status

**State Management:**
- SQLite database (`.aster-watcher/state.db`)
- Tracks processing history
- Prevents duplicate processing

---

## 🚀 Features

### Phase 1: Basic Watcher (MVP)
- ✅ Monitor inbox folder
- ✅ Auto-detect new files
- ✅ Simple FIFO queue
- ✅ Process with Aster
- ✅ Move to Obsidian vault
- ✅ Archive originals

### Phase 2: Priority Queue
- ✅ Read priority from queue.md
- ✅ Pattern matching for auto-priority
- ✅ Manual priority override
- ✅ Status updates in queue.md

### Phase 3: Smart Scheduling
- ✅ Idle detection (only process when Mac not in use)
- ✅ Batch processing at scheduled times
- ✅ Resource-aware (don't process during video calls)
- ✅ Battery-aware (skip heavy processing on battery)

### Phase 4: AI Enhancement
- ✅ LLM suggests priority based on content
- ✅ Auto-categorization (receipts → Finance, meetings → Meetings)
- ✅ Smart file naming
- ✅ Duplicate detection

---

## 📁 Folder Structure

```
~/Library/Mobile Documents/com~apple~CloudDocs/Aster/
├── inbox/                    # Drop files here from iPhone
│   ├── receipt_20251113.jpg
│   ├── meeting_notes.jpg
│   └── book_chapter.pdf
│
├── processing/               # Currently being processed
│   └── receipt_20251113.jpg
│
├── processed/                # Archived originals
│   └── 2025-11/
│       ├── receipt_20251113.jpg
│       └── meeting_notes.jpg
│
├── failed/                   # Failed processing
│   └── corrupted_file.jpg
│
├── queue.md                  # Queue status & config (editable)
├── .aster-watcher/           # Watcher state (hidden)
│   ├── state.db
│   ├── logs/
│   └── config.yaml
│
└── README.md                 # Instructions

~/Library/Mobile Documents/iCloud~md~obsidian/Vault/
└── Inbox/                    # Processed files appear here
    ├── receipt_20251113.md
    ├── meeting_notes.md
    └── book_chapter.md
```

---

## 🎮 User Experience

### From iPhone

**Scenario 1: Receipt**
1. Take photo of receipt
2. Share → Save to Files → Aster Inbox
3. *Walk away* - processing happens automatically
4. 2 minutes later: Open Obsidian → See formatted receipt in Finance/

**Scenario 2: Meeting Notes (Urgent)**
1. Take photo of whiteboard
2. Rename to `urgent_meeting_notes.jpg`
3. Share to Aster Inbox
4. Processes immediately (bypasses queue)
5. Notification: "Meeting notes ready in Obsidian"

**Scenario 3: Batch Books**
1. Download 10 PDF books to iPhone
2. Share all to Aster Inbox
3. Edit queue.md on iPhone: "Process overnight, low priority"
4. Go to sleep
5. Wake up: All books processed and in Vault/Books/

### From Mac

**Check Status:**
```bash
# Quick status
aster-watcher status

# Output:
# ✅ Watcher: Active
# 📥 Queue: 3 files
# 🔄 Processing: receipt_20251113.jpg (30% complete)
# ⏱️  ETA: 2 minutes
```

**Manual Control:**
```bash
# Start watcher
aster-watcher start

# Stop watcher
aster-watcher stop

# Process specific file with priority
aster-watcher queue urgent meeting_notes.jpg

# Clear queue
aster-watcher clear

# View logs
aster-watcher logs
```

---

## 🔍 Smart Features

### Auto-Priority Detection

```python
PATTERNS = {
    r'receipt_.*\.(jpg|png|pdf)': 'urgent',
    r'urgent_.*': 'urgent',
    r'meeting.*\.(jpg|png)': 'high',
    r'whiteboard.*': 'high',
    r'audio.*\.(mp3|m4a)': 'high',
    r'book.*\.pdf': 'low',
    r'archive_.*': 'low',
    r'newsletter.*': 'batch',
}
```

### LLM-Assisted Categorization

When processing completes, Ollama:
1. **Suggests category**: "This looks like a receipt → Finance/"
2. **Extracts metadata**: Date, vendor, amount
3. **Generates filename**: `2025-11-13_starbucks_receipt.md`
4. **Creates tags**: `#receipt #coffee #expense`

### Idle Detection

Only process when Mac is idle:
- No keyboard/mouse input for 2 minutes
- Not on video call (checks camera usage)
- Not running intensive apps
- Battery > 20% (if on battery)

---

## 🛡️ Safety Features

### Duplicate Prevention
- SHA256 hash of each file
- Skip if already processed
- Warn if similar file processed recently

### Error Handling
- Corrupted files → `failed/` folder
- Processing timeout → retry 3 times
- Network issues → queue until available

### Data Safety
- Never delete original until output verified
- Atomic moves (never partial files)
- Transaction log for all operations
- Backup of queue.md on every change

---

## 🔧 Configuration Examples

### `.aster-watcher/config.yaml`

```yaml
# Aster Inbox Watcher Configuration

# Folders
inbox: "~/Library/Mobile Documents/com~apple~CloudDocs/Aster/inbox"
processing: "~/Library/Mobile Documents/com~apple~CloudDocs/Aster/processing"
processed: "~/Library/Mobile Documents/com~apple~CloudDocs/Aster/processed"
failed: "~/Library/Mobile Documents/com~apple~CloudDocs/Aster/failed"
vault: "~/Library/Mobile Documents/iCloud~md~obsidian/Vault/Inbox"

# Processing
model: "llama3.2:1b"
concurrent_jobs: 1  # Process one at a time
max_retries: 3
timeout: 300  # 5 minutes per file

# Scheduling
batch_time: "02:00"  # Process batch jobs at 2am
idle_threshold: 120  # Wait 2 minutes idle before processing
check_interval: 5  # Check inbox every 5 seconds

# Safety
min_battery: 20  # Don't process on battery below 20%
pause_on_camera: true  # Pause during video calls
max_file_size: 100  # MB

# Notifications
notify_on_complete: true
notify_on_error: true
play_sound: true

# Logging
log_level: "INFO"
log_retention_days: 30
```

---

## 📊 Status Dashboard (Future)

### Menu Bar App

```
┌─────────────────────────┐
│ ⭐ Aster Watcher        │
├─────────────────────────┤
│ ✅ Active               │
│ 📥 Queue: 3 files       │
│ 🔄 Processing receipt   │
│ ⏱️  ETA: 2 min          │
├─────────────────────────┤
│ ▶ Pause                 │
│ 📊 View Queue           │
│ ⚙️  Settings            │
│ 📝 Open Queue.md        │
└─────────────────────────┘
```

---

## 💡 Advanced Ideas

### 1. Smart Context
- Time of day: Work hours = urgent receipts, Evening = relax and batch
- Location: At office = work docs urgent, At home = personal high

### 2. Learning
- Track what you process most
- Suggest priority adjustments
- "You usually mark meeting photos as urgent, auto-mark next time?"

### 3. Collaboration
- Multiple users sharing inbox
- Per-user priority preferences
- Conflict resolution

### 4. Mobile App Integration
- iOS Shortcuts integration
- Direct upload with priority selection
- Push notifications on completion

---

## 🚀 Implementation Roadmap

### Week 1: MVP
- Basic file watcher with watchdog
- Simple FIFO queue
- Aster integration
- Move to Obsidian vault

### Week 2: Priority System
- Parse queue.md for priorities
- Priority queue implementation
- Status updates to queue.md
- Pattern-based auto-priority

### Week 3: Polish
- Error handling
- Duplicate detection
- Logging and monitoring
- Command-line interface

### Week 4: Smart Features
- Idle detection
- Batch scheduling
- LLM categorization
- Menu bar app (optional)

---

## 🔍 Similar Projects for Reference

Based on research, these are good reference implementations:

1. **watchdog** - Core library for file system monitoring
2. **FolderWatcher** (gciftci) - Good example of plugin-based processing
3. **Watcher** (gregghz) - YAML-based configuration approach
4. **pyicloud** - If we need programmatic iCloud access

---

## 🎯 Success Metrics

- **Speed**: New file processed within 5 minutes (urgent) or next idle period (normal)
- **Reliability**: 99%+ success rate, no lost files
- **Transparency**: Always know queue status from queue.md
- **Flexibility**: Easy to adjust priorities and rules
- **Seamless**: "It just works" - zero configuration needed after setup

---

## ✨ Why This is Better Than Web Interface

| Feature | Web Interface | Inbox Watcher |
|---------|---------------|---------------|
| WiFi Required | ✅ Yes | ❌ No |
| Works Anywhere | ❌ No | ✅ Yes (iCloud) |
| Automatic | ❌ Manual upload | ✅ Fully automatic |
| Priority | ⚠️ Manual | ✅ Smart |
| Batch Processing | ❌ No | ✅ Yes |
| Offline Queue | ❌ No | ✅ Yes |
| Resource Aware | ❌ No | ✅ Yes |

**Best of Both Worlds:**
- Use web interface when on WiFi (faster feedback)
- Use inbox watcher when away (seamless background processing)

---

**Next Steps:** Implement Phase 1 MVP with basic watchdog integration!
