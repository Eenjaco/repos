# Time Keeping Project

**Status:** ✅ Active - tt-local implemented
**Purpose:** Simple, flexible time tracking using markdown files

---

## Quick Start

### Terminal (Interactive)
```bash
# Start timer
./tt-local s

# Stop timer
./tt-local e
```

### Apple Shortcuts
See [SHORTCUTS_SETUP.md](SHORTCUTS_SETUP.md) for full setup instructions

---

## What This Does

**Simple time tracking that:**
- ✅ Tracks start/stop times
- ✅ Saves to weekly markdown files (ISO week format)
- ✅ Works from terminal or iPhone (via Shortcuts)
- ✅ Uses plain text (Obsidian-friendly)
- ✅ Persists across sessions

**Output format:**
```
———
Task Title
Optional Subtitle
Start time: 07 Nov 2025 at 09:00:00
until
End Time: 07 Nov 2025 at 10:30:00
```

---

## Files

### Scripts
- `tt-local` - Interactive version (terminal use)
- `tt-local-shortcuts` - Non-interactive version (for Shortcuts)

### Documentation
- `README.md` - This file (overview)
- `SHORTCUTS_SETUP.md` - How to set up Apple Shortcuts
- `tt_update.md` - Technical design notes

### Data Files
- `2025-W[XX].md` - Weekly time tracking files (ISO week format)
- `.tt_local_state` - Temporary state file (don't edit manually)

---

## Usage Modes

### 1. Terminal (Mac)

**Interactive:**
```bash
cd "/Users/mac/Documents/Local Vault/Projects/Time Keeping"
./tt-local s     # Prompts for title/subtitle
./tt-local e     # Stops timer
```

**Scripted:**
```bash
./tt-local-shortcuts s "Task" "Subtitle" "/path/to/Time Keeping"
./tt-local-shortcuts e "/path/to/Time Keeping"
```

### 2. Apple Shortcuts (iPhone or Mac)

Create two shortcuts:
- "Start Timer" - Prompts for task info, starts timer
- "Stop Timer" - Stops active timer

See [SHORTCUTS_SETUP.md](SHORTCUTS_SETUP.md) for step-by-step setup.

### 3. SSH (iPhone → Mac)

From iPhone with SSH access:
```bash
ssh mac@192.168.68.58
cd "/Users/mac/Documents/Local Vault/Projects/Time Keeping"
./tt-local s
./tt-local e
```

Or use Apple Shortcuts (runs commands via SSH automatically).

---

## Features

### Weekly Files (ISO Week Format)
Files named: `2025-W45.md` (year + ISO week number)

**Why ISO weeks?**
- Standard format
- Consistent across tools
- Week starts Monday (international standard)

### State Persistence
`.tt_local_state` file tracks active timer across:
- Terminal sessions
- SSH connections
- Computer restarts

Can start on Mac, stop from iPhone (or vice versa).

### Plain Text
All data in markdown:
- Easy to read
- Easy to edit
- Works with Obsidian
- Version control friendly
- Future-proof

---

## Workflow Examples

### Example 1: Full Day Tracking

```bash
# Morning
./tt-local s
# Title: Morning planning
# Subtitle: Review priorities

# Later
./tt-local e
./tt-local s
# Title: Code implementation
# Subtitle: tt-local feature

# Afternoon
./tt-local e
./tt-local s
# Title: Documentation
# Subtitle: Shortcuts setup guide

# End of day
./tt-local e
```

**Result:** Three entries in `2025-W45.md` with all times tracked.

### Example 2: Mixed Usage

```bash
# Morning on Mac (terminal)
./tt-local s
# Title: Planning

# Afternoon from iPhone (Shortcuts)
Run "Stop Timer" shortcut
Run "Start Timer" shortcut
# Title: Meetings

# Evening back on Mac
./tt-local e
```

**Works seamlessly** - state file tracks across devices.

### Example 3: Quick Sessions

```bash
./tt-local s
# Title: Quick admin
# Subtitle: [leave blank]

# 15 minutes later
./tt-local e
```

**Subtitle is optional** - use when you need it, skip when you don't.

---

## Limitations

### What It Doesn't Do

❌ **Automatic tracking** - Must manually start/stop
❌ **Duration calculation** - Saves start/end times only
❌ **Reports/analytics** - Just raw data (for now)
❌ **Database** - Uses markdown files only
❌ **Sync** - Manual sync if using across devices

### Design Choices

These are intentional:
- **Manual start/stop** - Encourages intentional time tracking
- **Plain markdown** - Maximum flexibility, minimal lock-in
- **No auto-calculation** - Can add later if needed, easy to parse
- **Simple format** - Easy to understand and edit

---

## Future Enhancements

**Possible additions (see `/Projects/project-ideas-tracker.md`):**
- [ ] Duration calculation in entries
- [ ] Weekly/monthly reports script
- [ ] SQLite backend (optional)
- [ ] Export to other formats (CSV, JSON)
- [ ] Integration with session-summary script
- [ ] Automatic tagging/categorization

**Current status:** Phase 1 complete (basic tracking works)

---

## Troubleshooting

### Timer Already Running
```bash
# Problem: Started timer twice
# Solution: Stop first timer
./tt-local e
./tt-local s  # Now start new one
```

### No Running Timer
```bash
# Problem: Trying to stop when nothing running
# Solution: Start a timer first
./tt-local s
# ... work ...
./tt-local e
```

### Permission Denied
```bash
# Problem: Script not executable
# Solution:
chmod +x tt-local tt-local-shortcuts
```

### Wrong Output Location
Check the BASE_DIR in scripts:
- Default: `/Users/mac/Documents/Local Vault/Projects/Time Keeping`
- Pass custom path as argument if needed

---

## Integration

### With Obsidian
Weekly files open directly in Obsidian:
- Navigate to Time Keeping folder
- View/edit weekly files
- Use Obsidian search to find specific tasks

### With Session Summaries
Complement, don't duplicate:
- **Session summaries:** What you accomplished, learnings, reflections
- **Time tracking:** When you worked, what tasks
- Together: Complete picture of your work

### With Project Tracking
Track time on specific projects:
- Use project name in Title or Subtitle
- Later can filter/analyze by project

---

## Tips

### Be Consistent
Use similar patterns:
```
✅ "Email and admin"
✅ "Code: feature name"
✅ "Meeting: topic"

❌ "emails"
❌ "coding stuff"
❌ "mtg"
```

### Don't Overthink
- Start timer → do work → stop timer
- If you forget details, add them later (markdown is editable)
- Focus on tracking, not perfection

### Review Weekly
- Look at your week file
- See patterns
- Adjust as needed

---

## Technical Details

### File Format
- Weekly files: `YYYY-W[week].md` (ISO 8601 week format)
- State file: `.tt_local_state` (three lines: title, subtitle, start time)

### Date Format
`DD Mmm YYYY at HH:MM:SS` (e.g., "07 Nov 2025 at 09:30:00")

### Dependencies
- Bash 3.2+ (macOS default works)
- `date` command (standard on macOS)
- No external dependencies

---

## Quick Reference

| Action | Command |
|--------|---------|
| Start (interactive) | `./tt-local s` |
| Stop | `./tt-local e` |
| Start (scripted) | `./tt-local-shortcuts s "Title" "Sub" "/path"` |
| Stop (scripted) | `./tt-local-shortcuts e "/path"` |
| View week file | `cat 2025-W45.md` |
| Check if timer running | `[ -f .tt_local_state ] && echo "Running" || echo "Stopped"` |

---

## Support

- **Shortcuts setup:** See [SHORTCUTS_SETUP.md](SHORTCUTS_SETUP.md)
- **Technical details:** See [tt_update.md](tt_update.md)
- **SSH setup:** See `/Projects/ssh/README.md`
- **Project planning:** See `/Projects/project-ideas-tracker.md`

---

**Start tracking!** It's as simple as `./tt-local s` 🚀
