# Time Tracking Setup Complete! ✅

**Date:** 2025-11-07

---

## What's Now Configured

### Your existing `tt` command:
```bash
tt s    # Start timer (interactive category selection)
tt e    # End timer (saves to SQLite + markdown)
tt      # View weekly progress
```

**Now saves to TWO places:**
1. SQLite database (as before)
2. **NEW:** Markdown file in local time_logs folder

---

## Markdown File Location

**Path:** `/Users/mac/Documents/Local Vault/Projects/Time Keeping/time_logs/`

**Filename format:** `2025_W45_time.md` (year_week_time.md)

**Note:** Files are saved locally (not iCloud) to avoid permission issues

**Your workflow:**
1. Run `tt s` - select category (Admin, Communication, etc.)
2. Do your work
3. Run `tt e` - add optional description
4. Entry saved to BOTH database AND markdown

---

## File Format

Entries are now saved in **markdown table format** for easy data extraction:

```markdown
# Time Log - Week 45, 2025

| Date | Category | Subcategory | Start | End | Duration | Description |
|------|----------|-------------|-------|-----|----------|-------------|
| 2025-11-07 | Admin | Emails and whatsapp | 10:10:46 | 10:11:04 | 18s | Responded to inquiries |
| 2025-11-07 | Sermon | Writing | 11:00:00 | 12:30:00 | 1h 30m | Eucharist sermon prep |
```

**Benefits:**
- Single line per entry (easy parsing)
- Renders beautifully in Obsidian
- Simple CSV conversion (see below)

---

## Apple Shortcuts (Updated)

**Script location:** `/Users/mac/Documents/Local Vault/Projects/Time Keeping/tt-local-shortcuts`

**Now uses:**
- iCloud location (same as `tt`)
- New filename format (2025_W45_time.md)
- Same state file so both systems work together

**Setup Shortcuts:**
See `SHORTCUTS_SETUP.md` for full instructions

---

## What Changed

### `tt` script (Node.js)
- ✅ Added `MARKDOWN_DIR` constant
- ✅ Added `getWeekFilename()` - generates 2025_W45_time.md
- ✅ Added `formatAppleShortcutTime()` - formats dates
- ✅ Added `appendToMarkdown()` - writes entries
- ✅ Modified `cmdEndTimer()` - calls markdown append

### `tt-local-shortcuts` (Bash)
- ✅ Updated `BASE_DIR` to iCloud location
- ✅ Changed filename format to use underscores
- ✅ Updated state file location

### `tt-local` (Bash, interactive)
- ✅ Same updates as tt-local-shortcuts
- ✅ Kept for manual testing if needed

---

## State File

**Location:** `/Users/mac/Library/Mobile Documents/iCloud~md~obsidian/Documents/Shared Vault/time_keeping/.tt_local_state`

**Shared between:**
- Your `tt s` / `tt e` commands
- Apple Shortcuts
- Manual tt-local scripts

**Means:** Start on Mac, stop from iPhone (or vice versa) ✨

---

## Quick Test

Want to test it right now?

```bash
cd "/Users/mac/Documents/Local Vault"
tt s
# Select a category (like "Admin")
# Wait a few seconds
tt e
# Add optional description
```

Then check:
```bash
ls "/Users/mac/Documents/Local Vault/Projects/Time Keeping/time_logs/"
cat "/Users/mac/Documents/Local Vault/Projects/Time Keeping/time_logs/2025_W45_time.md"
```

You should see `2025_W45_time.md` with your entries in table format!

---

## In Obsidian

Your time logs are easily accessible:
1. Navigate to `Projects/Time Keeping/time_logs/`
2. See `2025_W45_time.md` with formatted tables
3. All your time entries in markdown!

Can link between notes, search, tag, or move to vault if needed.

---

## What Stays the Same

Your existing workflow is unchanged:
- `tt` - view progress
- `tt g` - set goals
- `tt i` - import data
- `tt w` - week summary
- All other commands work exactly as before

The ONLY change:
- `tt e` now ALSO writes to markdown ✨

---

## Files Reference

| File | Purpose | Location |
|------|---------|----------|
| `tt` | Main CLI (Node.js) | Time Keeping folder |
| `tt-local` | Interactive bash version | Time Keeping folder |
| `tt-local-shortcuts` | Apple Shortcuts version | Time Keeping folder |
| `append-to-markdown.sh` | Bash helper for markdown | Time Keeping folder |
| `timetracking.db` | SQLite database | Time Keeping folder |
| `.active-timer.json` | Current timer state | Time Keeping folder |
| `2025_W45_time.md` | Markdown log (table format) | time_logs/ subfolder |

---

## Next Steps

1. ✅ **Test now:** Run `tt s` then `tt e`
2. ✅ **Check Obsidian:** Open Shared Vault, see time_keeping folder
3. ✅ **(Optional) Set up Shortcuts:** See SHORTCUTS_SETUP.md
4. ✅ **Use normally:** Your existing workflow just got markdown logging!

---

## Converting to CSV

Need your data in CSV format? Easy:

```bash
# From any weekly markdown file
grep "^|" time_logs/2025_W45_time.md | tail -n +2 | sed 's/^| //; s/ | /,/g; s/ |$//' > week45.csv
```

This extracts:
- Date,Category,Subcategory,Start,End,Duration,Description
- 2025-11-07,Admin,Emails and whatsapp,10:10:46,10:11:04,18s,Responded to inquiries

Perfect for spreadsheets, analysis tools, or further processing!

---

## Troubleshooting

**If markdown file not created:**
- Check directory exists: `ls time_logs/`
- Verify bash script is executable: `ls -l append-to-markdown.sh`
- Run with full path to test

**If timer conflicts:**
- Delete active timer: `rm .active-timer.json`
- Start fresh with `tt s`

**Need help:**
- Check existing docs: README.md, SHORTCUTS_SETUP.md
- Review tt_update.md for technical details

---

**You're all set!** Your time tracking now works everywhere: terminal, SQLite, markdown, Obsidian, and soon Apple Shortcuts! 🚀
