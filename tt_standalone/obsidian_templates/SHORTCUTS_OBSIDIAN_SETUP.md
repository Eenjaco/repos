# Apple Shortcuts → Obsidian Setup Guide

## Overview

This guide shows you how to create Apple Shortcuts that add time entries directly to Obsidian markdown files, which are then auto-synced to SQLite via the watchdog script.

## Prerequisites

1. **Obsidian** installed on iPhone/Mac
2. **Obsidian vault** synced via iCloud
3. **Watchdog script** running on your Mac: `python3 watch_markdown.py`

## File Structure

Your Obsidian vault should have:
```
Your Vault/
  └── time_logs/
      ├── 2025_W45_time.md
      ├── 2025_W46_time.md
      └── ...
```

## Method 1: Simple Shortcut (Recommended)

### Step 1: Create "Add Time Entry" Shortcut

1. Open **Shortcuts** app
2. Create new shortcut: **Add Time Entry**
3. Add these actions:

```
1. [Ask] What category?
   - Choices: Sermon, Admin, Study, Pastoral Care, Meetings, Prayer, Other

2. [Ask] What subcategory? (optional)
   - Allow text input

3. [Ask] Start time?
   - Input type: Time

4. [Ask] End time?
   - Input type: Time

5. [Calculate] Duration in minutes
   - (End Time - Start Time) / 60

6. [Format] Duration as text
   - If minutes >= 60:
     - hours = minutes / 60 (rounded down)
     - remaining = minutes % 60
     - format = "{hours}h {remaining}m"
   - Else:
     - format = "{minutes}m"

7. [Get] Current date
   - Format: YYYY-MM-DD

8. [Get] Current week number
   - Format as: YYYY_W{week}_time.md

9. [Create] Table row text:
   | {date} | {category} | {subcategory} | {start} | {end} | {duration} | {description} |

10. [Append] to file in Obsidian
    - File path: time_logs/{filename}
    - Text: {table_row}

11. [Show] notification "✓ Time entry added"
```

### Step 2: Add to Home Screen

1. Long press shortcut → **Details**
2. Enable **Add to Home Screen**
3. Choose icon and name
4. Tap **Add**

Now you have a one-tap time entry button!

## Method 2: Quick Add (Even Faster)

For preset categories (e.g., "Sermon Writing"):

```
1. [Set Variable] category = "Sermon"
2. [Set Variable] subcategory = "Writing"
3. [Ask] Description? (optional)
4. [Get] Current time → start_time
5. [Wait] for timer...
6. [Get] Current time → end_time
7. [Calculate & Append] same as above
```

## Method 3: Timer-Based Entry

Start/Stop timer like the CLI:

### "Start Timer" Shortcut:
```
1. [Ask] Category
2. [Ask] Subcategory
3. [Get] Current time
4. [Save to File] .timer_state.json
   {
     "category": "{category}",
     "subcategory": "{subcategory}",
     "start": "{time}"
   }
5. [Show] "Timer started for {category}"
```

### "Stop Timer" Shortcut:
```
1. [Read] .timer_state.json
2. [Get] Current time → end_time
3. [Calculate] duration
4. [Append] to weekly markdown
5. [Delete] .timer_state.json
6. [Show] "Timer stopped: {duration}"
```

## Obsidian Plugin Recommendations

### 1. **Templater** (for dynamic templates)

Install and set template folder: `obsidian_templates/`

```javascript
// Example Templater script for time entry
<%*
const now = tp.date.now("YYYY-MM-DD");
const week = tp.date.now("YYYY_W[W]_time");
const category = await tp.system.prompt("Category?");
const start = await tp.system.prompt("Start time (HH:MM)?");
const end = await tp.system.prompt("End time (HH:MM)?");

// Calculate duration
const [sh, sm] = start.split(':').map(Number);
const [eh, em] = end.split(':').map(Number);
const minutes = (eh * 60 + em) - (sh * 60 + sm);
const hours = Math.floor(minutes / 60);
const mins = minutes % 60;
const duration = hours > 0 ? `${hours}h ${mins}m` : `${mins}m`;

tR = `| ${now} | ${category} | | ${start} | ${end} | ${duration} | |`;
%>
```

### 2. **QuickAdd** (for fast entries)

1. Install QuickAdd plugin
2. Create new "Capture" choice
3. Set template: `Quick_Time_Entry.md`
4. Set target: `time_logs/{{date:YYYY_W[W]_time}}.md`
5. Assign hotkey or create button

### 3. **Dataview** (for viewing stats in Obsidian)

Query your time logs directly in notes:

```dataview
TABLE
  sum(rows.Duration) as "Total Hours",
  count(rows) as "Entries"
FROM "time_logs"
WHERE file.name = "2025_W46_time"
GROUP BY Category
```

### 4. **Buttons** (for mobile quick entry)

Create a button in any note:

```button
name Add Time Entry
type command
action QuickAdd: Time Entry
```

## Automatic Sync

Once you've added entries to Obsidian markdown:

1. **Obsidian Sync** or **iCloud** syncs the file to your Mac
2. **Watchdog** detects the change: `python3 watch_markdown.py`
3. **Auto-parses** and inserts to SQLite
4. **CLI** shows updated stats immediately: `./tt`

## File Naming Convention

Always use ISO week format:
```
YYYY_W##_time.md
```

Examples:
- `2025_W45_time.md` (Week 45 of 2025)
- `2025_W01_time.md` (Week 1 of 2025)

## Troubleshooting

**Issue:** Entries not syncing to SQLite

**Solutions:**
1. Check watchdog is running: `ps aux | grep watch_markdown`
2. Check file format matches table structure
3. Run manual sync: `./tt i time_logs/2025_W46_time.md`

**Issue:** Week number doesn't match CLI

**Solution:**
- iOS uses local week numbers
- CLI uses ISO week (Monday start)
- Use `date +%V` on Mac to verify

## Tips

1. **Create multiple shortcuts** for frequent categories
2. **Use Siri** to trigger shortcuts hands-free
3. **Sync via iCloud** for fastest updates
4. **Keep watchdog running** in background on Mac
5. **Check `./tt st`** to verify entries synced

## Example Workflow

**On iPhone:**
1. Tap "Add Sermon Time" shortcut
2. Select "Writing" subcategory
3. Enter times: 2:00 PM → 3:30 PM
4. Obsidian file updated

**On Mac (automatic):**
1. iCloud syncs file (< 5 seconds)
2. Watchdog detects change
3. Parses and inserts to SQLite
4. Run `./tt` to see updated stats

No manual import needed! 🎉
