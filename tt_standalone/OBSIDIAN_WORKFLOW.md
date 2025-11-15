# Obsidian Workflow Guide

Complete setup for your Apple Notes → Obsidian → SQLite workflow.

## 📁 File Structure

```
iCloud Obsidian (Phone + Mac):
└── Shared Vault/
    └── time_keeping/
        ├── current_task_timer.md  ← Active timer (appended by Shortcuts)
        └── timelog_archive.md     ← Weekly archives (historical)

Local Mac Only:
└── ~/Documents/Applications/tt_standalone/
    ├── timetracking.db            ← SQLite database (analytics)
    ├── parse_timer_format.py      ← Parser for timer format
    ├── watch_obsidian_timer.py    ← Auto-sync daemon
    ├── weekly_archive.sh          ← Sunday archive script
    └── backups/                   ← Local archive backups
        └── timelog_archive_YYYYMMDD.md
```

---

## 🔄 Complete Workflow

### Monday - Saturday: Time Tracking

**On Phone (via Shortcuts):**

1. **Start Timer:**
   - Run "Time Tracker Start" shortcut
   - Select category (Sermon, Pastoral, etc.)
   - Enter subcategory
   - Appends to `current_task_timer.md`:
     ```
     ———
     Sermon
     writing
     Start time: 15 Nov 2025 at 10:30:45
     until
     ```

2. **Stop Timer:**
   - Run "Time Tracker Stop" shortcut
   - Replaces "until" with end time:
     ```
     ———
     Sermon
     writing
     Start time: 15 Nov 2025 at 10:30:45
     End Time: 15 Nov 2025 at 12:15:20
     ```

**On Mac (Automatic):**

3. **Watchdog Detects Change:**
   - iCloud syncs markdown file (< 5 seconds)
   - Watchdog detects file change
   - Parses timer format
   - Inserts to SQLite database

4. **View Analytics:**
   ```bash
   tt              # Show weekly progress
   tt t            # Today's entries
   tt w            # This week's summary
   ```

---

### Sunday: Weekly Archive

**Run on Mac:**

```bash
# Archive the week (run from anywhere with alias)
ttarchive

# Or manually:
cd ~/Documents/Applications/tt_standalone
./weekly_archive.sh
```

**What it does:**

1. ✅ Processes all remaining entries to SQLite
2. ✅ Appends current week to `timelog_archive.md` with header
3. ✅ Creates local backup: `backups/timelog_archive_20251115.md`
4. ✅ Clears `current_task_timer.md` for new week
5. ✅ Adds header for new week

---

## ⚙️ Setup Instructions

### 1. Create Obsidian Files

```bash
# Create the directory structure
mkdir -p "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/Shared Vault/time_keeping"

# Create current timer file
cat > "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/Shared Vault/time_keeping/current_task_timer.md" << 'EOF'
# Current Task Timer

Week 46, 2025 - Started 15 Nov 2025

EOF

# Create archive file
cat > "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/Shared Vault/time_keeping/timelog_archive.md" << 'EOF'
# Time Log Archive

Historical weekly time tracking entries.

EOF
```

### 2. Set Up Apple Shortcuts

Follow: `shortcuts/APPLE_SHORTCUTS_SETUP.md`

Create three shortcuts:
- **Time Tracker Start** (begin timer)
- **Time Tracker Stop** (end timer)
- **Time Tracker Status** (check active)

### 3. Start Watchdog on Mac

```bash
# Terminal 1: Run watchdog (keeps running)
ttwatch

# Or in background:
ttwatch &

# Or use tmux (persistent):
tmux new -s timer-watch
ttwatch
# Detach: Ctrl+B, then D
```

The watchdog will:
- Monitor `current_task_timer.md`
- Auto-parse when file changes
- Insert to SQLite immediately

### 4. Add Weekly Archive Alias

Add to `~/.zshrc`:

```bash
alias ttarchive='(cd "$TT_HOME" && ./weekly_archive.sh)'
```

Then reload:
```bash
source ~/.zshrc
```

---

## 📱 Daily Usage

### Starting Your Day

**On Phone:**
1. Open Shortcuts
2. Run "Time Tracker Start"
3. Select: Sermon → Research
4. Work...

**Check Progress on Mac:**
```bash
tt              # See weekly progress
```

### During the Day

**Switch Tasks:**
1. Run "Time Tracker Stop"
2. Run "Time Tracker Start"
3. Select new category

**Check Status:**
- Run "Time Tracker Status" shortcut
- Shows active timer details

### End of Week (Sunday)

**On Mac:**
```bash
# Archive the week
ttarchive

# Check stats
tt w            # This week's summary
tt st           # Database stats
```

---

## 🔍 Monitoring & Debugging

### Check Watchdog Status

```bash
# See if watchdog is running
ps aux | grep watch_obsidian_timer

# View watchdog output
ttwatch

# Manual sync (if watchdog not running)
python3 parse_timer_format.py "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/Shared Vault/time_keeping/current_task_timer.md"
```

### Check iCloud Sync

```bash
# View current timer file
cat "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/Shared Vault/time_keeping/current_task_timer.md"

# Check modification time
ls -lh "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/Shared Vault/time_keeping/current_task_timer.md"
```

### View Archive

```bash
# View archive file
cat "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/Shared Vault/time_keeping/timelog_archive.md"

# Count archived entries
grep -c "^———" "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/Shared Vault/time_keeping/timelog_archive.md"

# View local backups
ls -lh ~/Documents/Applications/tt_standalone/backups/
```

---

## 🚨 Troubleshooting

### Timer Not Syncing

**Issue:** Phone adds timer but Mac doesn't see it

**Solutions:**
1. Check iCloud sync status (System Preferences → iCloud)
2. Open Obsidian on Mac (forces sync)
3. Check watchdog is running: `ps aux | grep watch_obsidian`
4. Manual sync: `python3 parse_timer_format.py <path>`

### Duplicate Entries

**Issue:** Same entry appears multiple times

**Solution:**
- Parser checks for duplicates automatically
- If duplicates exist, they were added before parser ran
- Use CLI to remove: `tt` → check database

### Watchdog Not Detecting Changes

**Issue:** File changes but watchdog doesn't process

**Solutions:**
1. Restart watchdog: `pkill -f watch_obsidian && ttwatch`
2. Check file path is correct in script
3. Ensure iCloud Drive is online
4. Try manual parse to test

### Archive Failed

**Issue:** `weekly_archive.sh` errors

**Solutions:**
1. Check file exists: `ls -la "$HOME/Library/Mobile Documents/iCloud~md~obsidian/..."`
2. Check permissions: `ls -l weekly_archive.sh`
3. Run manually: `bash -x weekly_archive.sh` (debug mode)

---

## 📊 Example Weekly Flow

### Monday, 9:00 AM

**Phone:**
- Start: Sermon / Research
- Timer appends to markdown

**Mac (automatic):**
- Watchdog detects → syncs to SQLite
- Run `tt`: Shows 0h progress

### Monday, 12:00 PM

**Phone:**
- Stop timer
- 3h logged

**Mac:**
- Run `tt`: Shows 3h Sermon progress

### Week continues...

Daily: Start/stop timers via phone
Periodic: Check `tt` for progress

### Sunday, 5:00 PM

**Mac:**
```bash
ttarchive       # Archive the week
```

**Output:**
```
Week 46, 2025 - Archived on 17 Nov 2025

Entries to archive:
  28 timer entries found

Processing final sync to SQLite...
✓ Imported 28 entries

✓ Archived to timelog_archive.md
✓ Backup saved to: timelog_archive_20251117.md
✓ Cleared current timer file

Summary:
  • Archived 28 entries
  • Saved to: timelog_archive.md
  • Backed up: timelog_archive_20251117.md
  • Cleared: current_task_timer.md

Ready for Week 47!
```

---

## 🎯 Best Practices

1. **Start watchdog on Mac login** (use launchd - see `SETUP_TERMINAL.md`)
2. **Archive every Sunday** (set calendar reminder)
3. **Keep backups** (already automatic to `backups/` folder)
4. **Don't edit timer file manually** (use shortcuts only)
5. **Check `tt` weekly** (monitor goals)

---

## 📈 Analytics

View your time with CLI:

```bash
tt              # Weekly progress with goals
tt t            # Today's entries
tt w            # This week summary
tt m            # This month summary
tt l 10         # Last 10 entries
tt st           # Database statistics
```

All data lives in SQLite, so you can:
- Query with SQL
- Export to CSV
- Sync with Google Sheets
- Build custom reports

---

## 🔐 Data Safety

Your data is stored in **three places**:

1. **iCloud Obsidian** (phone + Mac, synced)
   - `current_task_timer.md` (active)
   - `timelog_archive.md` (historical)

2. **SQLite Database** (Mac only)
   - `timetracking.db`
   - Real-time analytics

3. **Local Backups** (Mac only)
   - `backups/timelog_archive_YYYYMMDD.md`
   - Weekly snapshots

**If Mac dies:**
- All data safe in iCloud Obsidian
- Re-run parser to rebuild SQLite

**If iCloud dies:**
- Data safe in SQLite + local backups
- Export and re-import

---

Happy time tracking! 🎉
