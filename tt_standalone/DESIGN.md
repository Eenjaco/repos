# Time Keeping - Living Design Document

**Last Updated:** 2025-10-31
**Status:** Production Ready - v3.0 with Omarchy colors
**Claude Sessions:** 4 major sessions

---

## Project Vision

**What:** Ministry time tracking with weekly goal setting and progress visualization
**Why:** Track ministry work hours, set weekly goals, monitor progress daily
**For Whom:** Ministry worker tracking sermon prep, pastoral care, administrative work, and more

---

## Current State

**Version:** 3.0 - CLI Time Tracker with Weekly Goals & Colors
**Working Features:**
- ✅ **CLI tool (`tt`)** - Super short commands, works from anywhere
- ✅ **SQLite database** (`timetracking.db`) - 279+ entries, 503h 48m tracked
- ✅ **Apple Shortcut import** - Direct paste (`tt i`) or file import
- ✅ **Weekly goal setting** (`tt g`) - Set goals, see total hours planned
- ✅ **Progress tracking** - Visual progress bars, remaining hours calculation
- ✅ **Daily progress alerts** - Shows hours needed per day to meet goals
- ✅ **Subcategories** - Track detailed breakdowns (Sermon > Reading, etc.)
- ✅ **Category management** - Rename categories retroactively
- ✅ **Omarchy color theme** - Green + dark grey-blue terminal colors
- ✅ **Editable goals** - Press Enter to keep, change only what you need
- ✅ **Migrated historical data** - All .tsx files → SQLite (269 entries)
- ✅ CSV export for Google Sheets compatibility
- ✅ Comprehensive documentation (QUICK-REF.md, COLOR-GUIDE.md)

**Categories (7):**
- Sermon, Operations, Pastoral & Community, Admin, Communication, Sinod, Prayer

**Consolidated duplicates:**
- Communications → Communication
- Sinode → Sinod

**Known Issues:**
- None currently - system production ready

---

## Quick Commands

| Command | Action |
|---------|--------|
| `tt` | Show weekly progress (default) |
| `tt g` | Set weekly goals |
| `tt i` | Import Apple Shortcut (paste) |
| `tt a` | Add manual entries |
| `tt w` | Week summary |
| `tt m` | Month summary |
| `tt l` | List entries |
| `tt st` | Stats |
| `tt x` | Export CSV |

---

## Color Customization

**Omarchy Theme Active:**
- Bright Green (#00D787 / code 42) - Time durations, achievements
- Dark Grey-Blue (code 67) - Category names, headers
- Cyan (code 80) - Progress indicators
- Yellow (code 226) - Numbers, percentages
- Orange (code 214) - Remaining time warnings
- Dark Grey (code 240) - Labels, separators

**To customize:** See `COLOR-GUIDE.md` for full color palette and instructions

**Edit colors:** `tt` file, lines 16-38

---

## Architecture Overview

**High-Level Design:**
React dashboards (.tsx) contain hardcoded time tracking data → Node.js scripts extract data using regex → CSV files generated → Manual or automated Google Sheets import

**Key Components:**
1. **Source Data** - 16 .tsx files with React components containing time entries
2. **Export Engine** - Node.js scripts that parse .tsx files
3. **CSV Output** - Standardized data files ready for spreadsheets
4. **Import Helpers** - Scripts to upload to Google Sheets

**Data Flow:**
```
.tsx files → export-to-csv.js → time-tracking-export.csv
                ↓
        create-summaries.js
                ↓
    summary-by-week.csv
    summary-by-month.csv
    summary-by-category.csv
                ↓
        Google Sheets (manual/auto import)
```

**Tech Stack:**
- Language: JavaScript (Node.js)
- Key Libraries: googleapis@105 (for Google Sheets API)
- Storage: CSV files (plain text, universal format)
- Source: TypeScript/React components (not executed, just parsed)

---

## Design Decisions

### Decision 1: CSV Export Instead of Live Dashboards
**Date:** 2025-10-30
**Context:** User had React dashboards but wanted simple, manageable data in spreadsheets
**Decision:** Extract data to CSV rather than deploy web dashboards
**Rationale:**
- User explicitly wanted "most basic if possible"
- CSV works everywhere (Excel, Google Sheets, any tool)
- No hosting needed, no dependencies to run
- Spreadsheets better for ad-hoc analysis
**Tradeoffs:**
- Lost interactive charts (acceptable - not needed)
- Manual re-export if .tsx data changes (rare, acceptable)

### Decision 2: Parse .tsx with Regex Not AST Parser
**Date:** 2025-10-30
**Context:** Need to extract JavaScript objects from .tsx files
**Decision:** Use regex pattern matching instead of full AST parser
**Rationale:**
- Simple, direct, works for this specific data structure
- No heavy dependencies (like Babel)
- Fast execution
- Data structure is consistent across files
**Tradeoffs:**
- Brittle if data structure changes drastically
- Won't work for complex nested structures
- Good enough for current needs

### Decision 3: Separate Summaries from Raw Data
**Date:** 2025-10-30
**Context:** 288 entries is lot to analyze, need summaries
**Decision:** Generate 3 separate summary CSVs (week/month/category)
**Rationale:**
- Quick overview without scrolling 288 rows
- Pre-aggregated data saves user time
- Can import as separate sheets in Google Sheets
- Each summary <5KB - fast to work with
**Tradeoffs:**
- More files to manage (acceptable - only 4 total)
- Redundant data (acceptable - storage cheap)

### Decision 4: Keep Google Drive Links in JSON
**Date:** 2025-10-30
**Context:** User has live Google Docs, don't want to lose access
**Decision:** Store all Drive links in one JSON file
**Rationale:**
- Centralized link management
- Easy to update when URLs change
- Machine-readable format
- Separates live (Drive) from static (local) data
**Tradeoffs:**
- Extra file to maintain (but only one place to update)

---

## Evolution History

### Phase 1: Initial Situation (Before 2025-10-30)
**State:**
- Time tracking data in 16+ React .tsx files
- Each file = self-contained dashboard component
- Beautiful visualizations but data trapped in code
- Hard to do cross-week/month analysis

### Phase 2: First Export Attempt (2025-10-30 Morning)
**Goal:** Combine all time tracking data for analysis
**Approach:** Created combined-time-tracking-data.ts (TypeScript file)
**Issue:** User said "pause" - wanted simpler solution
**Learning:** User prefers basic CSV over complex data structures

### Phase 3: CSV Export Solution (2025-10-30 Afternoon)
**Goal:** Export to CSV for Excel/Google Sheets
**Built:**
- `export-to-csv.js` - Extracts data from all .tsx files
- `create-summaries.js` - Generates week/month/category summaries
- 4 CSV files created (288 entries extracted)
**Result:** Success! Data now in universally usable format

### Phase 4: Google Sheets Integration (2025-10-30 Late)
**Goal:** Get CSVs into Google Sheets
**Built:**
- `upload-to-sheets.js` - Manual import helper
- `auto-create-sheet.js` - Automated OAuth uploader
- Documentation for both methods
**Result:** User successfully imported data to Google Sheets

### Phase 5: Documentation & Organization (2025-10-30 Evening)
**Goal:** Set up system for future projects
**Built:**
- `PROJECT-ORGANIZATION.md` - Strategy for organizing files
- `EXAMPLE-CONVERSION-MASTER-DNA.md` - How to convert complex docs
- `LEARNING-ROADMAP.md` - Linux/CLI learning path
- `LIVING-DOCUMENTATION-SYSTEM.md` - This documentation approach
- `DESIGN.md` - This file!
**Result:** Framework for managing all future Claude projects

---

## File Structure

```
Time Keeping/
├── Source Data (React Dashboards):
│   ├── time_tracking_jul21_27.tsx      # Week data
│   ├── time_tracking_aug2025.tsx       # Month summaries
│   ├── time_tracking_oct2025.tsx       # Latest data
│   └── ... (13 more .tsx files)
│
├── Export Scripts:
│   ├── export-to-csv.js                # Main export engine
│   ├── create-summaries.js             # Aggregation engine
│   ├── upload-to-sheets.js             # Manual helper
│   └── auto-create-sheet.js            # OAuth uploader
│
├── Generated Data:
│   ├── time-tracking-export.csv        # All 288 entries
│   ├── summary-by-week.csv             # 18 weeks
│   ├── summary-by-month.csv            # 5 months
│   └── summary-by-category.csv         # 7 categories
│
├── Documentation:
│   ├── README-GOOGLE-SHEETS.md         # Import guide
│   ├── IMPORT-INSTRUCTIONS.txt         # Quick reference
│   ├── DESIGN.md                       # This file
│   └── package.json                    # Node dependencies
│
└── Configuration:
    └── node_modules/                   # googleapis package
```

**Key Files:**
- `export-to-csv.js` - Heart of the system, parses .tsx files
- `time-tracking-export.csv` - Complete dataset, 288 entries
- `summary-by-category.csv` - Best overview (7 categories, totals)

---

## Data Summary

**Time Period:** June 30 - October 27, 2025 (4 months)
**Total Time:** 918 hours 22 minutes (55,102 minutes)
**Total Entries:** 288 time tracking entries
**Categories:** 7 (Sermon, Operations, Pastoral, Admin, Sinod, Communication, Prayer)
**Weeks:** 18 weeks tracked
**Months:** 5 months (partial Jun, full Jul/Aug/Sep, partial Oct)
**Active Days:** 79 days with activity

**Top Categories:**
1. Sermon: 500h 37m (54.5%)
2. Operations: 146h 30m (16.0%)
3. Pastoral & Community: 119h 4m (13.0%)

---

## Connections to Other Projects

**Depends On:** None (standalone project)

**Used By:** None currently

**Related:**
- Part of broader ministry framework projects
- Example implementation for PROJECT-ORGANIZATION.md
- Reference for future data export projects

**Future Potential:**
- Could feed into ministry reporting dashboard
- Could integrate with calendar system
- Could export to accounting/billing systems

→ See `CONNECTIONS.md` when this starts linking to other projects

---

## Next Steps

**Immediate (Complete):**
- [x] Extract all data from .tsx files
- [x] Generate summary reports
- [x] Import to Google Sheets
- [x] Document the system

**Short Term (Optional):**
- [ ] Add automation: watch .tsx files, auto-regenerate CSVs
- [ ] Create script to add new time entries from command line
- [ ] Build simple CLI tool: "track sermon 2h 30m"
- [ ] Add data validation (catch errors in source data)

**Long Term (Ideas):**
- [ ] Real-time tracking app (instead of manual .tsx editing)
- [ ] Integration with calendar for automatic time logging
- [ ] Predictive analytics (time allocation recommendations)
- [ ] Multi-user support (team time tracking)

---

## For Claude AI

**Quick Context:**
Ministry time tracking system. Data lives in 16 .tsx React files. Node.js scripts extract to CSV. User imports CSVs to Google Sheets for analysis. User wanted "most basic solution" - we delivered CSV export instead of complex web app.

**Key Files to Read First:**
1. `export-to-csv.js` - Understand extraction logic
2. `time-tracking-export.csv` - See actual data structure
3. `summary-by-category.csv` - Quick data overview

**Common Tasks:**
- "Re-export data" → `node export-to-csv.js && node create-summaries.js`
- "Add new feature" → Check this DESIGN.md first, maintain simplicity
- "Fix export" → Check regex patterns in export-to-csv.js
- "Update docs" → Update this file + README-GOOGLE-SHEETS.md

**User Preferences:**
- Keep it simple! "Most basic if possible"
- CSV over complex formats
- Local files over cloud dependencies
- Documentation that's easy to find and update

---

## Session Log

### Session 4: 2025-10-30 Late Evening - SQLite Database + CLI Tool (v2.0)
**Built:**
- `track.js` - Complete CLI tool with 8 commands (import, today, week, month, list, stats, export, help)
- SQLite database schema with time_entries table
- Apple Shortcut format parser
- Database query functions (today, week, month summaries)
- CSV export from database (maintains compatibility with v1.0)
- `README-CLI.md` - Comprehensive CLI documentation
- `sample-shortcut-data.txt` - Test data in Apple Shortcut format
- Updated package.json to v2.0 with better-sqlite3 dependency

**Major Upgrade:**
Version 1.0 → 2.0: From static .tsx files to dynamic database with CLI

**User Workflow Change:**
- **Before:** Edit .tsx files → Run export scripts → Get CSV
- **After:** Apple Shortcut output → `track import` → Query anytime → Export when needed

**Tested:**
- ✅ Import from Apple Shortcut format (8 test entries)
- ✅ Database creation and schema
- ✅ Query commands (today, week, month, list, stats)
- ✅ CSV export (compatible with Google Sheets import)
- ✅ Summary generation by category and month

**Learned:**
- User has effective Apple Shortcut for time tracking
- Shortcut outputs specific format (Category, Description, Start/End times)
- User values simple command-line tools
- Database approach much more accessible than .tsx editing

**Design Decisions:**
1. **SQLite over other databases** - Local, no server, single file, cross-platform
2. **Node.js for CLI** - Already have Node.js installed, easy to use
3. **Maintain CSV export** - Keep compatibility with existing Google Sheets workflow
4. **Parse Apple Shortcut format** - User already has working system, don't change it

**Next Steps for User:**
1. Use Apple Shortcut to generate time tracking data
2. Save output to text file
3. Import with `track import filename.txt`
4. Query with `track today/week/month`
5. Export to Google Sheets when needed with `track export`

**Future Enhancement Ideas:**
- Migration script to import historical .tsx data into SQLite
- Direct Apple Shortcut integration (if possible)
- Mobile-friendly web interface (optional)
- Automated weekly reports

### Session 3: 2025-10-30 Evening - Documentation & Future Planning
**Built:**
- Living Documentation System concept
- PROJECT-ORGANIZATION.md strategy
- LEARNING-ROADMAP.md (35 KB comprehensive guide)
- This DESIGN.md file

**Learned:**
- User wants to migrate all Claude projects to local disk
- Planning move to Omarchy Linux
- Total beginner to CLI/development but motivated
- Values organization and AI-friendly documentation

**Next:** User will start Phase 1 of learning roadmap, migrate other projects

### Session 2: 2025-10-30 Afternoon - Google Sheets Integration
**Built:**
- `upload-to-sheets.js` - Opens Sheets, shows import instructions
- `auto-create-sheet.js` - Full OAuth automation
- README-GOOGLE-SHEETS.md - Complete import guide
- Installed googleapis package

**Success:** User successfully imported all 4 CSVs to Google Sheets

**Design Decision:** Offer both manual and automated import (user chose manual - simpler)

### Session 1: 2025-10-30 Morning - Initial Export
**Built:**
- `export-to-csv.js` - Core extraction script
- `create-summaries.js` - Aggregation by week/month/category
- 4 CSV files generated
- package.json setup

**Learned:**
- User has 15+ .tsx files with time tracking data
- Data format is consistent (dailyData + taskSessions objects)
- Regex parsing works well for this structure
- User values simple solutions

---

## Technical Notes

**Why This Approach Works:**
- .tsx files are just text - don't need React to parse them
- Data structure is consistent across all files
- Regex sufficient for current complexity
- CSV is universal - works everywhere

**Limitations:**
- Manual process (need to run scripts after .tsx changes)
- No real-time updates
- Regex brittle if data structure changes significantly
- No data validation on source files

**Acceptable Because:**
- .tsx files rarely change (historical data)
- Re-export takes <5 seconds
- Data structure hasn't changed in months
- User familiar with data, unlikely to have errors

---

**Document Purpose:** Central source of truth for Time Keeping project
**Update Frequency:** After every Claude session
**Maintained By:** User + Claude together
**Last Session:** 2025-10-30 Late Evening (Session 4)
