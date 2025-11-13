# Time Tracking v3.0 - Quick Start Guide

🎉 **Your time tracking system has been upgraded!**

## What's New in v3.0

✅ **SQLite Database** - All your data in one fast, queryable file
✅ **Subcategories** - Track more detailed breakdowns (Sermon > Reading, Operations > Planning)
✅ **Weekly Goals** - Set time goals each week and track progress
✅ **Progress Tracking** - See weekly progress with visual bars
✅ **Interactive Add** - Paste entries from notes for manual tracking
✅ **Category Rename** - Retroactively rename categories (Operations → Bestuur)
✅ **269 Historical Entries Imported** - All your .tsx data is now in the database!

---

## ✅ Migration Complete!

**Your historical data:**
- 269 entries imported
- 485 hours of ministry work tracked
- Date range: July 8 - October 24, 2025
- 109 days tracked
- Average: 4h 27m per day

**Categories found:**
- Sermon
- Operations
- Pastoral & Community
- Admin
- Communication
- Sinode
- Prayer

---

## Daily Workflow (NEW!)

### Monday Morning: Set Weekly Goals

```bash
cd "/Users/mac/Documents/Terminal/Claude/Projects/Time Keeping"
node track.js goal-wizard
```

**Interactive prompt:**
```
🎯 Set Weekly Goals (Oct 28 - Nov 3)

Common categories:
  1. Sermon
  2. Operations
  3. Pastoral & Community
  4. Admin
  5. Communication
  6. Sinode
  7. Prayer

Sermon goal (default 12h, or "0" to skip): 12h
Operations goal (or press Enter to skip): 8h
Pastoral & Community goal (or press Enter to skip): 5h
Admin goal (or press Enter to skip): 3h
...
```

---

### Throughout the Week: Check Progress

```bash
node track.js status
```

**Output:**
```
📊 This Week's Progress (Oct 28 - Nov 3):

  Sermon                    8h 15m     / 12h 0m     [████████░░░░] 68%  ← 3h 45m remaining
  Operations                5h 30m     / 8h 0m      [███████░░░░░] 69%  ← 2h 30m remaining
  Pastoral & Community      2h 15m     / 5h 0m      [█████░░░░░░░] 45%  ← 2h 45m remaining
  Admin                     3h 20m     / 3h 0m      [████████████] 100% ← 0m remaining

────────────────────────────────────────────────────────────
Total Week:        19h 20m
Today (Thu):       4h 45m
```

---

### Add Manual Entries (Optional)

If you need to add entries you forgot to track:

```bash
node track.js add
```

**Interactive prompt:**
```
📝 Add Time Entries
Paste your entries (one per line or multiple lines)
Format: Category, Duration, Description
Example: Sermon, 2h 30m, Reading Isaiah
With subcategory: Sermon > Reading, 2h 30m, Isaiah study

Press Ctrl+D (Mac/Linux) or Ctrl+Z (Windows) when done.

Sermon, 2h 30m, Sermon prep
Operations > Planning, 1h 15m, Weekly schedule
Admin, 45m, Emails

✓ Added: Sermon - 2h 30m
✓ Added: Operations > Planning - 1h 15m
✓ Added: Admin - 45m

✓ Added 3 entries
```

---

### Import from Apple Shortcut

When your Apple Shortcut gives you time data, save it to a file and import:

```bash
node track.js import my-shortcut-data.txt
```

**Your Shortcut format (with subcategories):**
```
Current Task Timer
...
———
Sermon
Reading
Start time: 28 Oct 2025 at 10:52:18
until
End Time: 28 Oct 2025 at 12:38:20
———
Operations
Planning
Start time: 28 Oct 2025 at 13:23:04
until
End Time: 28 Oct 2025 at 14:38:06
———
```

---

## All Commands

### Weekly Goals & Progress
```bash
node track.js status          # Check weekly progress
node track.js goal-wizard     # Set weekly goals (Mon morning)
```

### Data Entry
```bash
node track.js import file.txt # Import Apple Shortcut data
node track.js add             # Add entries interactively
```

### View Data
```bash
node track.js today           # Today's entries
node track.js week            # Last 7 days
node track.js month           # Current month
node track.js list [n]        # List last n entries
node track.js stats           # Database statistics
```

### Export
```bash
node track.js export          # Export to CSV for Google Sheets
```

### Category Management
```bash
node track.js rename-category "Old Name" "New Name"
# Example: node track.js rename-category "Operations" "Bestuur"
# Updates ALL historical entries!
```

---

## Subcategories

Track more detailed breakdowns:

**Format in Apple Shortcut (separate lines):**
```
Sermon
Reading
Start time: ...
```

**Format when adding manually:**
```
Sermon > Reading, 2h 30m, Isaiah study
Operations > Planning, 1h, Weekly schedule
Pastoral > Visits, 2h, Hospital visit
```

**Common subcategories you might use:**
- Sermon > Reading, Writing, Slides, Presentation
- Operations > Planning, Facility, Admin
- Pastoral > Visits, Funerals, Counseling
- Admin > Emails, Reports, Correspondence

---

## Weekly Workflow

### Monday Morning
1. `track goal-wizard` - Set this week's goals
   - Sermon defaults to 12h (or skip if no preaching)
   - Set other categories based on this week's needs

### Daily (Anytime)
2. `track status` - Check progress toward goals
3. Track time in your Apple Shortcut throughout the day
4. `track add` - Add any forgotten entries

### End of Week
5. `track week` - Review full week breakdown
6. `track export` - Export to Google Sheets (if needed)

---

## Tips & Tricks

### Create an Alias (Recommended!)

Add to your `~/.zshrc`:
```bash
alias track='node "/Users/mac/Documents/Terminal/Claude/Projects/Time Keeping/track.js"'
```

Then just use:
```bash
track status
track goal-wizard
track add
```

### Goal History

Your weekly goals are saved! Over time you'll build up:
- Historical weekly goals
- Average time per category
- Trend data

Future enhancement: `track goal-history` to see averages

### Category Rename

Need to change "Operations" to "Bestuur" across all 269 entries?
```bash
node track.js rename-category "Operations" "Bestuur"
```

This updates:
- All time entries (past and future)
- All weekly goals
- Logs the change in category_history table

---

## Your Apple Shortcut Format

**Current format (Category only):**
```
———
Admin
Emails and whatsapp
Start time: 27 Oct 2025 at 13:11:56
until
End Time: 27 Oct 2025 at 15:14:58
———
```

**Enhanced format (with Subcategory):**
```
———
Sermon
Reading
Start time: 27 Oct 2025 at 13:11:56
until
End Time: 27 Oct 2025 at 15:14:58
———
```

The second line becomes the subcategory if it's followed by "Start time".
Otherwise it's treated as part of the description.

---

## Database Location

**File:** `/Users/mac/Documents/Terminal/Claude/Projects/Time Keeping/timetracking.db`

**Backup:** Just copy this one file!
```bash
cp timetracking.db timetracking-backup-$(date +%Y%m%d).db
```

**Portable:** Works on Linux, Mac, Windows - just move the file!

---

## What Happened to .tsx Files?

Your .tsx files are still there as **historical records**. They contain:
- Original React dashboards
- Visual charts
- Weekly summaries

The data has been **imported** into the database, not moved.

You can:
- Keep them for reference
- Archive them to a backup folder
- Delete them (data is now in database)

---

## Next Steps

1. **Test the new workflow:**
   ```bash
   node track.js status    # Should show no entries this week
   node track.js stats     # Should show 269 total entries
   node track.js month     # Should show October data
   ```

2. **Set up for next week:**
   - Wait until Monday
   - Run `track goal-wizard`
   - Set your goals for the week

3. **Update your Apple Shortcut** (optional):
   - Add subcategory line for more detailed tracking
   - Format: Category on line 1, Subcategory on line 2

4. **Create shell alias** for quick access (see Tips above)

---

## Troubleshooting

### "Module not found"
```bash
cd "/Users/mac/Documents/Terminal/Claude/Projects/Time Keeping"
npm install
```

### Want to re-migrate .tsx files?
```bash
# Delete database
rm timetracking.db

# Run migration again
node migrate-tsx.js
```

### Check specific category data
```bash
node track.js list 50 | grep "Sermon"
```

### Export and verify in spreadsheet
```bash
node track.js export
# Open time-tracking-export.csv in Excel/Numbers
```

---

## Future Enhancements (Coming Soon)

Ideas for future versions:
- [ ] `track goal-history` - Show average weekly goals over time
- [ ] Auto-import from Apple Shortcut (watch folder)
- [ ] Scheduled daily summary (cron job at 5pm)
- [ ] Web interface for mobile access
- [ ] Backup automation
- [ ] Goal recommendations based on history

---

**Questions?** Just ask Claude for help!

**Version:** 3.0
**Updated:** October 31, 2025
**Migration Status:** ✅ Complete - 269 entries imported
