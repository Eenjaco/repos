# Quick Start: Obsidian Workflow

Move from Apple Notes to Obsidian with auto-sync to SQLite.

## 📦 What You Got

New files added to your repo:

1. **parse_timer_format.py** - Parses Apple Notes-style timer format
2. **watch_obsidian_timer.py** - Watches Obsidian timer file, auto-syncs to SQLite
3. **weekly_archive.sh** - Archives week's timers every Sunday
4. **OBSIDIAN_WORKFLOW.md** - Complete workflow guide
5. **shortcuts/APPLE_SHORTCUTS_SETUP.md** - Create Apple Shortcuts
6. **ALIASES_ZSHRC.sh** - Updated aliases including `ttwatch` and `ttarchive`

---

## ⚡ 5-Minute Setup

### Step 1: Update Aliases

```bash
# Add new aliases to .zshrc
cat ALIASES_ZSHRC.sh >> ~/.zshrc
source ~/.zshrc
```

**New commands:**
- `ttwatch` - Start Obsidian watcher
- `ttarchive` - Archive weekly timers

### Step 2: Create Obsidian Files

```bash
# Create directory
mkdir -p "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/Shared Vault/time_keeping"

# Create current timer file
cat > "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/Shared Vault/time_keeping/current_task_timer.md" << 'EOF'
# Current Task Timer

Week 46, 2025

EOF

# Create archive file
touch "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/Shared Vault/time_keeping/timelog_archive.md"
```

### Step 3: Start Watchdog

```bash
# In a new terminal (or background)
ttwatch
```

**Or run in background:**
```bash
ttwatch &
```

**Or use tmux (recommended):**
```bash
tmux new -s timer
ttwatch
# Detach: Ctrl+B, then D
# Reattach later: tmux attach -t timer
```

### Step 4: Create Apple Shortcuts

Open `shortcuts/APPLE_SHORTCUTS_SETUP.md` and follow the guide to create:

1. **Time Tracker Start** - Begin timer
2. **Time Tracker Stop** - End timer
3. **Time Tracker Status** - Check active timer

---

## 🎯 Using It

### Daily Workflow

**On Phone:**
1. Run "Time Tracker Start" shortcut
2. Select: Sermon → Writing
3. Work...
4. Run "Time Tracker Stop" shortcut

**On Mac (automatic):**
- iCloud syncs markdown
- Watchdog detects change
- Parses and inserts to SQLite
- Run `tt` to see progress

### Weekly Archive (Sunday)

```bash
ttarchive
```

This will:
- Process all entries to SQLite
- Append to `timelog_archive.md`
- Create local backup
- Clear `current_task_timer.md`

---

## 📊 Commands

| Command | What it does |
|---------|-------------|
| `tt` | Show weekly progress |
| `ttb` | Begin timer (CLI) |
| `tte` | End timer (CLI) |
| `ttwatch` | Start Obsidian watcher |
| `ttarchive` | Archive weekly timers |
| `ttcd` | Jump to tt directory |
| `ttsync` | Pull latest changes |

---

## 📁 File Locations

**iCloud (Phone + Mac):**
```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Shared Vault/time_keeping/
├── current_task_timer.md   (active timers)
└── timelog_archive.md       (weekly archives)
```

**Local (Mac only):**
```
~/Documents/Applications/tt_standalone/
├── timetracking.db          (SQLite analytics)
└── backups/                 (local archive backups)
    └── timelog_archive_YYYYMMDD.md
```

---

## 🔍 Verification

### Test the Flow

1. **Add a test entry** to `current_task_timer.md`:
```markdown
———
Test Category
test
Start time: 15 Nov 2025 at 10:00:00
End Time: 15 Nov 2025 at 11:00:00
```

2. **Watch it sync:**
   - Watchdog should detect change
   - Parse and insert to SQLite
   - Show: "✓ Added: 2025-11-15 | Test Category / test | 1h"

3. **Check database:**
```bash
tt l 1    # Show last entry
```

---

## 📚 Full Documentation

- **OBSIDIAN_WORKFLOW.md** - Complete workflow guide
- **shortcuts/APPLE_SHORTCUTS_SETUP.md** - Shortcuts setup
- **SETUP_TERMINAL.md** - Terminal configuration

---

## 🚀 Ready to Go!

You're all set! Start using the shortcuts on your phone and watch the magic happen.

Questions? Check `OBSIDIAN_WORKFLOW.md` for troubleshooting.
