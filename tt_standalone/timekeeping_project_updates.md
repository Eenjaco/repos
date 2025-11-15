# CLAUDE.md - Claude Projects Directory

This directory contains projects and work created with Claude Code.

## Directory Structure

```
Projects/
├── Time Keeping/              # Ministry time tracking project (Jun-Oct 2025)
│   ├── *.tsx                  # 16+ React dashboard components
│   ├── *.js                   # Node.js export scripts
│   ├── *.csv                  # Generated data exports
│   ├── package.json           # Node.js dependencies
│   ├── node_modules/          # Installed packages (googleapis)
│   └── README-GOOGLE-SHEETS.md
│
├── Omarchy/                   # (Other project directory)
└── CLAUDE.md                  # This file
```

---

# Time Keeping Project

## Overview

**Ministry time tracking and analysis system** covering June 30 - October 27, 2025.

- **Total Time Tracked:** 918 hours 22 minutes
- **Total Entries:** 288 detailed time entries
- **Period:** 4+ months of ministry work
- **Categories:** Sermon (54.5%), Operations (16%), Pastoral & Community (13%), Admin (6.6%), Sinod (5.9%), Communication (3.7%), Prayer (0.3%)

## Project Structure

### React Dashboard Components (*.tsx files)

**Location:** `Time Keeping/`

16 TypeScript/React files containing interactive dashboards with:
- Daily/weekly/monthly time breakdowns
- Pie charts and bar charts (using Recharts)
- Category summaries with percentages
- Detailed session timestamps

**File Types:**
- Monthly summaries: `time_tracking_july2025.tsx`, `time_tracking_aug2025.tsx`, `time_tracking_oct2025.tsx`
- Weekly details: `time_tracking_jul21_27.tsx`, `time_tracking_aug4_10.tsx`, etc.
- Individual dashboards: `timesheet-dashboard.tsx`

**Data Structure in Each File:**
```javascript
// Summary totals
const overallData = [
  { name: 'Sermon', value: 1242, display: '20h 42m', percentage: 63.7 }
];

// Daily breakdown
const dailyData = {
  '21 Jul 2025': [
    { name: 'Sermon', value: 216, display: '3h 36m' }
  ]
};

// Detailed sessions with timestamps
const taskSessions = {
  '21 Jul 2025': {
    'Sermon': [
      '11:38:07 – 13:31:58 (1h 54m)',
      '14:19:56 – 16:02:09 (1h 42m)'
    ]
  }
};
```

### Node.js Export Scripts

**Location:** `Time Keeping/`

#### 1. export-to-csv.js
**Purpose:** Extracts all time tracking data from .tsx files and exports to CSV

**How it works:**
- Scans directory for .tsx files (excludes dashboard files)
- Uses regex to extract `dailyData` and `taskSessions` objects
- Parses JavaScript object notation to extract values
- Outputs: `time-tracking-export.csv` (288 entries, 29 KB)

**Output Format:**
```csv
Date,Category,Minutes,Time Display,Percentage,Session Details
13 Oct 2025,Sermon,80,1h 20m,,09:42:58 – 11:02:48 (1h 20m)
```

**Run:**
```bash
cd "/Users/mac/Documents/Terminal/Claude/Time Keeping"
node export-to-csv.js
```

#### 2. create-summaries.js
**Purpose:** Creates aggregated summary reports by week, month, and category

**How it works:**
- Reads `time-tracking-export.csv`
- Parses dates and groups entries by week/month
- Calculates totals and percentages for each category
- Generates 3 summary CSV files

**Outputs:**
- `summary-by-week.csv` - 18 weeks of data (4.5 KB)
- `summary-by-month.csv` - 5 months breakdown (1.4 KB)
- `summary-by-category.csv` - 7 categories totaled (335 B)

**Run:**
```bash
cd "/Users/mac/Documents/Terminal/Claude/Time Keeping"
node create-summaries.js
```

#### 3. upload-to-sheets.js
**Purpose:** Helper script for manual Google Sheets import

**How it works:**
- Lists all CSV files with their locations
- Opens Google Sheets in browser
- Displays step-by-step import instructions
- Creates `IMPORT-INSTRUCTIONS.txt` for reference

**Run:**
```bash
cd "/Users/mac/Documents/Terminal/Claude/Time Keeping"
node upload-to-sheets.js
```

#### 4. auto-create-sheet.js
**Purpose:** Automated Google Sheets creation with OAuth

**How it works:**
- Authenticates via Google OAuth 2.0
- Creates new spreadsheet with 4 tabs
- Uploads all CSV data automatically
- Formats headers (blue background, white text)
- Opens finished sheet in browser

**Requirements:**
- `credentials.json` from Google Cloud Console
- First-time OAuth authorization

**Run:**
```bash
cd "/Users/mac/Documents/Terminal/Claude/Time Keeping"
node auto-create-sheet.js
```

### Package Configuration

**File:** `Time Keeping/package.json`

```json
{
  "name": "time-keeping",
  "version": "1.0.0",
  "description": "Time tracking data export and Google Sheets integration",
  "main": "export-to-csv.js",
  "scripts": {
    "export": "node export-to-csv.js",
    "summaries": "node create-summaries.js",
    "sheets": "node upload-to-sheets.js",
    "auto-sheets": "node auto-create-sheet.js"
  },
  "dependencies": {
    "googleapis": "^105.0.0"
  }
}
```

**Installed Dependencies:**
- `googleapis@105` - Google Sheets API integration (51 packages total)

**Installation:**
```bash
cd "/Users/mac/Documents/Terminal/Claude/Time Keeping"
npm install
```

### Generated CSV Files

**Location:** `Time Keeping/`

1. **time-tracking-export.csv** (29 KB)
   - 288 detailed entries
   - Columns: Date, Category, Minutes, Time Display, Percentage, Session Details
   - All data from all .tsx files combined

2. **summary-by-week.csv** (4.5 KB)
   - 18 weeks tracked
   - Weekly totals per category
   - Percentage of week for each category

3. **summary-by-month.csv** (1.4 KB)
   - 5 months: Jun, Jul, Aug, Sep, Oct 2025
   - Monthly totals per category
   - Percentage of month for each category

4. **summary-by-category.csv** (335 B)
   - 7 categories total
   - Grand totals with percentages
   - Days active for each category

### Documentation Files

**Location:** `Time Keeping/`

- `README-GOOGLE-SHEETS.md` - Complete Google Sheets import guide
- `IMPORT-INSTRUCTIONS.txt` - Quick reference for manual import

---

## Common Workflows

### Export All Data to CSV
```bash
cd "/Users/mac/Documents/Terminal/Claude/Time Keeping"
node export-to-csv.js
node create-summaries.js
```

### Import to Google Sheets (Manual)
```bash
cd "/Users/mac/Documents/Terminal/Claude/Time Keeping"
node upload-to-sheets.js
# Follow on-screen instructions
```

### Import to Google Sheets (Automated)
```bash
cd "/Users/mac/Documents/Terminal/Claude/Time Keeping"
node auto-create-sheet.js
# Requires credentials.json setup
```

### Add New Time Tracking Data
1. User creates new .tsx file with time tracking data
2. Run export scripts:
   ```bash
   cd "/Users/mac/Documents/Terminal/Claude/Time Keeping"
   node export-to-csv.js
   node create-summaries.js
   ```
3. Re-import CSVs to Google Sheets

### Check Data Summary
```bash
cd "/Users/mac/Documents/Terminal/Claude/Time Keeping"
node create-summaries.js
cat summary-by-category.csv
```

---

## Data Categories

### 1. Sermon (54.5%)
- **Total:** 500h 37m
- **Activities:** Reading, writing, slides, presentation
- **Days Active:** 79 days
- **Primary focus** of ministry work

### 2. Operations (16.0%)
- **Total:** 146h 30m
- **Activities:** Facility management, administrative operations, planning
- **Days Active:** 49 days

### 3. Pastoral & Community (13.0%)
- **Total:** 119h 4m
- **Activities:** Community engagement, spiritual direction, pastoral visits
- **Days Active:** 36 days

### 4. Admin (6.6%)
- **Total:** 60h 58m
- **Activities:** Emails, administrative tasks, documentation
- **Days Active:** 30 days

### 5. Sinod (5.9%)
- **Total:** 54h 37m
- **Activities:** Denominational governance, ring meetings, reports
- **Days Active:** 11 days

### 6. Communication (3.7%)
- **Total:** 33h 57m
- **Activities:** Ministry communications, coordination
- **Days Active:** 14 days

### 7. Prayer (0.3%)
- **Total:** 2h 39m
- **Activities:** Dedicated prayer time
- **Days Active:** 6 days

---

## Technical Details

### Color Coding (Used in Dashboards)
```javascript
const colors = {
  'Sermon': '#8B5CF6',              // Purple
  'Operations': '#3B82F6',          // Blue
  'Pastoral & Community': '#10B981', // Green
  'Admin': '#F59E0B',               // Amber
  'Communication': '#EF4444',        // Red
  'Prayer': '#06B6D4',              // Cyan
  'Sinod': '#EC4899'                // Pink
};
```

### Date Parsing
- Format: "DD MMM YYYY" (e.g., "13 Oct 2025")
- Week calculation: ISO week number
- Month grouping: "MMM YYYY" (e.g., "Oct 2025")

### Time Display Format
- Input: Minutes as integer
- Output: "Xh Ym" format (e.g., "20h 42m")

### File Processing Logic
1. **Scan** - Find all .tsx files
2. **Extract** - Use regex to find dailyData and taskSessions
3. **Parse** - Convert JavaScript objects to structured data
4. **Combine** - Merge all files into single dataset
5. **Export** - Write to CSV format
6. **Summarize** - Aggregate by week/month/category

---

## User Preferences

**Important Context:**
- User wants **"the most basic if possible"** - prefer simple solutions
- No complex graphs needed initially - CSV/Excel export is primary goal
- Google Sheets integration for easy management and sharing
- Data is from ministry/pastoral work - treat as confidential

---

## Quick Reference Commands

```bash
# Navigate to project
cd "/Users/mac/Documents/Terminal/Claude/Time Keeping"

# List all tracking files
ls *.tsx

# Export everything
node export-to-csv.js && node create-summaries.js

# View summaries
head summary-by-category.csv
head summary-by-month.csv
head -30 summary-by-week.csv

# Check CSV output
wc -l *.csv

# Import to Google Sheets helper
node upload-to-sheets.js

# Reinstall dependencies if needed
npm install
```

---

## Troubleshooting

### "Module not found" error
```bash
cd "/Users/mac/Documents/Terminal/Claude/Time Keeping"
npm install
```

### CSV files not generating
- Check you're in correct directory
- Verify .tsx files exist: `ls *.tsx`
- Run with full path: `node /Users/mac/Documents/Terminal/Claude/Time\ Keeping/export-to-csv.js`

### Google Sheets import issues
- Use manual method first (easier)
- Ensure all 4 CSV files exist
- Import files one at a time
- First file: "Replace spreadsheet"
- Other files: "Insert new sheet(s)"

### Data looks incorrect
- Re-run export scripts after any .tsx changes
- Verify source data in .tsx files
- Check CSV files directly: `cat summary-by-category.csv`

---

## Future Enhancements (Potential)

- [ ] Deploy React dashboards to web
- [ ] Add year-over-year comparisons
- [ ] Automated weekly data entry
- [ ] Budget/goal tracking per category
- [ ] PDF report generation
- [ ] Email automated summaries
- [ ] Mobile app integration

---

## Statistics Summary

```
Period: June 30 - October 27, 2025 (4 months)
Total Time: 918h 22m (55,102 minutes)
Total Entries: 288
Categories: 7
Weeks: 18
Months: 5 (partial)
Active Days: 79 (with sermon work)
Average per day: ~4.5 hours
Files: 16 .tsx dashboard files
Scripts: 4 Node.js export scripts
Dependencies: googleapis (51 packages)
CSV Files: 4 (total 35.5 KB)
```

---

**Last Updated:** October 30, 2025
**Project Status:** ✅ Complete - Ready for Google Sheets import
**Next Steps:** User will manually import CSV files to Google Sheets

---

## Living Documentation System 🔄

**IMPORTANT:** All projects use living documentation that auto-updates with each session.

### How It Works:

**Start Every Session:**
```
1. Read project's DESIGN.md for current state
2. Check CONNECTIONS.md if project links to others
3. Review recent decisions in DECISIONS.md
```

**End Every Session:**
```
1. Update DESIGN.md with today's changes
2. Document design decisions made
3. Update CONNECTIONS.md if added integrations
4. Log session in DESIGN.md session log
```

### Documentation Files:

- **DESIGN.md** - Living design document (current state, decisions, history)
- **CONNECTIONS.md** - Project relationships and data flows
- **DECISIONS.md** - Architecture Decision Records (ADRs)
- **README.md** - User-facing quick start

**Full System:** See `LIVING-DOCUMENTATION-SYSTEM.md`

**Example:** See `Time Keeping/DESIGN.md` for reference implementation

---

## Quick Start for New Claude Session

1. **Understand the project:**
   ```bash
   cd "/Users/mac/Documents/Terminal/Claude"
   cat CLAUDE.md | head -50
   ```

2. **Read living documentation:**
   ```bash
   cd "Project-Name"
   cat DESIGN.md           # Current state & decisions
   cat CONNECTIONS.md      # If exists - project links
   ```

3. **Check current data:**
   ```bash
   cd "Time Keeping"
   ls *.tsx *.csv *.js
   ```

4. **Re-export if needed:**
   ```bash
   node export-to-csv.js
   node create-summaries.js
   ```

5. **Update documentation before ending session:**
   ```bash
   nano DESIGN.md          # Add today's work to session log
   ```

**Remember:**
- Keep it simple! User prefers basic, straightforward solutions
- Update DESIGN.md after every session
- Document WHY not just WHAT
