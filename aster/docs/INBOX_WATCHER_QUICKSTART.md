# Inbox Watcher - Quick Start

**Automatic file processing from iPhone to Obsidian via iCloud Drive**

---

## 🚀 Setup (5 Minutes)

### 1. Install Dependencies

```bash
cd /Users/mac/Documents/Applications/repos/aster
source venv/bin/activate
pip install watchdog
```

### 2. Create Folders

```bash
chmod +x setup_inbox_watcher.sh
./setup_inbox_watcher.sh
```

This creates:
- `~/Library/Mobile Documents/com~apple~CloudDocs/Aster/inbox/` (iCloud folder)
- Processing, archive, and state folders
- Configuration files

### 3. Start the Watcher

```bash
./aster_watcher.py run
```

Leave this running in a terminal. You'll see:
```
✨ Aster Inbox Watcher Starting
📥 Watching: ~/Library/.../Aster/inbox
📤 Output: ~/Library/.../Vault/Inbox
👀 Watching for new files...
```

---

## 📱 From iPhone

### First Time Setup

1. Open **Files** app on iPhone
2. Go to **iCloud Drive**
3. Find **Aster → inbox** folder
4. **Add to Favorites** (star icon) for quick access

### Daily Use

**Method 1: Take Photo**
1. Take photo of receipt/whiteboard/note
2. Tap **Share** → **Save to Files**
3. Navigate to **Aster/inbox**
4. Save
5. *Done!* - Processing happens automatically

**Method 2: Save File**
1. Save PDF/document from app
2. Share to Files → Aster/inbox
3. *Done!*

**Method 3: Multiple Files**
1. Select multiple files
2. Share → Save to Files → Aster/inbox
3. All process in queue

### Check Results

1. Open **Obsidian** on iPhone
2. Go to **Inbox/** folder
3. See your processed markdown files!

---

## 🎯 Priority System

Name files with prefixes for smart processing:

| Prefix | Priority | Processing Time | Use For |
|--------|----------|-----------------|---------|
| `urgent_*` | Urgent | Immediate | Meetings, deadlines |
| `receipt_*` | Urgent | Immediate | Receipts, bills |
| `meeting_*` | High | ~5 minutes | Meeting notes |
| `whiteboard_*` | High | ~5 minutes | Whiteboard photos |
| (no prefix) | Normal | When idle | General documents |
| `book_*` | Low | Overnight | Books, long PDFs |
| `archive_*` | Low | Overnight | Archive materials |

**Examples:**
```
urgent_meeting_notes.jpg       → Processes immediately
receipt_starbucks_2025.jpg     → Processes immediately
whiteboard_standup.jpg         → Processes in 5 min
book_deep_work_ch3.pdf         → Processes overnight
```

---

## 🔍 Monitoring

### Check Status

```bash
# Quick status
./aster_watcher.py status

# Output:
# ✅ Watcher: Active (PID: 12345)
# 📥 Inbox: 2 files
```

### View Logs (Live)

```bash
tail -f ~/Library/Mobile\ Documents/com~apple~CloudDocs/Aster/.aster-watcher/watcher.log
```

### View Queue Status

Open in any text editor (iPhone or Mac):
```
~/Library/Mobile Documents/com~apple~CloudDocs/Aster/inbox/queue.md
```

---

## 💡 Tips & Tricks

### 1. iPhone Shortcuts (Advanced)

Create iOS Shortcut "Process with Aster":
1. Shortcuts app → New Shortcut
2. Add "Get File"
3. Add "Save File" → Destination: Aster/inbox
4. Add "Show Notification" → "Processing..."

Now: Share any file → **Process with Aster**

### 2. Batch Processing

Drop 20 files at once:
- Files process one at a time
- Queue managed automatically
- Check progress in `queue.md`

### 3. Work from Anywhere

iCloud syncs everywhere:
- Add file on iPhone in café
- Mac at home processes it
- View in Obsidian on iPad

---

## 🛠️ Troubleshooting

### Files Not Processing?

**Check 1: Is watcher running?**
```bash
./aster_watcher.py status
```

**Check 2: Are files in inbox?**
```bash
ls ~/Library/Mobile\ Documents/com~apple~CloudDocs/Aster/inbox/
```

**Check 3: View logs**
```bash
tail -f ~/Library/Mobile\ Documents/com~apple~CloudDocs/Aster/.aster-watcher/watcher.log
```

**Check 4: Restart watcher**
```bash
# Stop (if running)
./aster_watcher.py stop

# Start fresh
./aster_watcher.py run
```

### File Failed Processing?

Failed files move to:
```
~/Library/Mobile Documents/com~apple~CloudDocs/Aster/failed/
```

Check the error in watcher.log

### iCloud Sync Issues?

- Make sure iCloud Drive is enabled: System Settings → Apple ID → iCloud
- Check storage space
- Wait for sync (can take 30 seconds)

---

## ⚙️ Configuration

Edit `aster_watcher.py` to customize:

**Change Ollama model:**
```python
MODEL = "llama3.2:1b"  # Change to qwen2.5:0.5b for faster
```

**Change vault location:**
```python
VAULT = Path.home() / "your/obsidian/vault/path/Inbox"
```

**Add custom priority patterns:**
```python
PRIORITY_PATTERNS = {
    r'urgent_.*': 1,
    r'your_pattern.*': 2,
    # ...
}
```

---

## 🎮 Workflow Examples

### Morning Routine
```
1. Wake up
2. Review Obsidian Inbox/
3. See all yesterday's files processed overnight
4. Move to appropriate folders
```

### Meeting Flow
```
1. During meeting: Photo whiteboard
2. Name: whiteboard_standup.jpg
3. Share to Aster inbox
4. Keep discussing
5. After meeting: Notes ready in Obsidian
```

### Receipt Management
```
1. Buy coffee
2. Photo receipt: receipt_starbucks.jpg
3. Share to Aster inbox
4. Done - auto-extracted, categorized, ready for expenses
```

### Book Notes
```
1. Reading at night
2. Photo interesting page
3. Name: book_atomic_habits_p45.jpg
4. Share to inbox
5. Morning: Full transcription in Obsidian/Books/
```

---

## 🚀 Next Level Features (Coming Soon)

Planned enhancements:
- [ ] Battery-aware processing (skip on low battery)
- [ ] Video call detection (pause during meetings)
- [ ] LLM auto-categorization
- [ ] Menu bar status app
- [ ] Push notifications on completion
- [ ] Smart file naming suggestions

---

## 📖 Learn More

- **Full Design:** [INBOX_WATCHER_DESIGN.md](INBOX_WATCHER_DESIGN.md)
- **Implementation:** `aster_watcher.py`
- **Setup Script:** `setup_inbox_watcher.sh`

---

## 💬 Feedback

This is a new feature! Let us know:
- What works well?
- What's confusing?
- What features do you need?

**Status:** ⚡ **Beta** - Ready to use, actively improving

---

**Enjoy seamless iPhone → Obsidian workflows!** ✨
