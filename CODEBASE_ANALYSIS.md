# Time Tracking Application - Comprehensive Codebase Overview

## Executive Summary

This is a **ministry time tracking CLI application (v3.0)** built with Node.js that tracks work hours, manages weekly goals, and integrates with Apple Shortcuts. The application uses SQLite for persistent storage and markdown files for supplementary tracking.

**Key Stats:**
- 279 time entries recorded
- 503+ hours tracked
- 7 categories
- 84 KB SQLite database
- Pure Node.js CLI tool (no web framework)

---

## 1. ARCHITECTURE OVERVIEW

### High-Level Design
```
User/Apple Shortcut Input
        ↓
CLI Tool (tt) - Node.js 
        ↓
SQLite Database (timetracking.db)
        ↓
Weekly Markdown Files (time_logs/)
        ↓
CSV Export (Google Sheets compatibility)
```

### Technology Stack
- **Language:** JavaScript (Node.js)
- **Database:** SQLite 3 (better-sqlite3 library)
- **File System:** Markdown files for supplementary storage
- **CLI Framework:** Native Node.js readline module
- **Color Output:** ANSI terminal codes (256-color palette)
- **Version:** 3.0

### Main Entry Point
**File:** `/home/user/repos/time_keeping/tt` (1,558 lines)

This is a Node.js executable script (shebang: `#!/usr/bin/env node`) that serves as the main CLI interface.

---

## 2. CURRENT ARCHITECTURE & HOW IT WORKS

### A. Command Structure

The application supports ~20+ commands organized into categories:

#### Timer Commands (Real-Time Tracking)
```
tt s, tt start          # Start timer (select category/subcategory)
tt e, tt end, tt stop   # End timer (save with optional description)
tt status               # Show weekly progress (DEFAULT command)
```

#### Goal & Planning
```
tt g, tt goal-wizard    # Set weekly goals interactively
```

#### Data Entry
```
tt i, tt import         # Import Apple Shortcut data (paste or file)
tt a, tt add            # Add manual entries (CSV format)
```

#### Reporting & Analysis
```
tt t, tt today          # Today's entries
tt w, tt week           # Last 7 days
tt m, tt month          # Current month
tt l, tt list [n]       # List last n entries (default: 20)
tt st, tt stats         # Database statistics
tt x, tt export         # Export to CSV
```

#### Management
```
tt rn, tt rename        # Rename category retroactively
tt help, tt h           # Show help/usage
```

### B. Database Schema (SQLite)

**Main Tables:**

1. **time_entries** (Primary data store)
   ```sql
   CREATE TABLE IF NOT EXISTS time_entries (
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     category TEXT NOT NULL,
     subcategory TEXT,                    -- Optional (e.g., "Reading")
     description TEXT,
     start_time TEXT NOT NULL,            -- Format: "YYYY-MM-DD HH:MM:SS"
     end_time TEXT NOT NULL,              -- Format: "YYYY-MM-DD HH:MM:SS"
     duration_minutes INTEGER NOT NULL,
     date TEXT NOT NULL,                  -- Indexed for queries
     created_at TEXT DEFAULT CURRENT_TIMESTAMP
   );
   ```
   - **Current size:** ~80 KB
   - **Indexes:** date, category, subcategory, for fast queries

2. **weekly_goals** (Weekly targets tracking)
   ```sql
   CREATE TABLE IF NOT EXISTS weekly_goals (
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     week_start TEXT NOT NULL,
     week_end TEXT NOT NULL,
     category TEXT NOT NULL,
     goal_minutes INTEGER NOT NULL,
     created_at TEXT DEFAULT CURRENT_TIMESTAMP,
     UNIQUE(week_start, category)          -- Only one goal per category/week
   );
   ```

3. **category_history** (Rename audit log)
   ```sql
   CREATE TABLE IF NOT EXISTS category_history (
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     old_name TEXT NOT NULL,
     new_name TEXT NOT NULL,
     changed_at TEXT DEFAULT CURRENT_TIMESTAMP
   );
   ```

### C. Workflow - How Users Track Time

#### Workflow 1: Using CLI Timer (Real-time)
```
1. tt s              → Prompts for category selection
                     → Optionally select subcategory
                     → Timer starts, saves to .active-timer.json
                     
2. [Work happens]    → .active-timer.json persists across sessions
                     → Timer data survives shell restarts
                     
3. tt e              → Prompts for optional description
                     → Saves to database
                     → Appends to markdown time_logs file
                     → Clears .active-timer.json
```

**Key Feature:** Timer state persists in `/home/user/repos/time_keeping/.active-timer.json`:
```json
{
  "category": "Sermon",
  "subcategory": "writing",
  "startTime": "2025-11-13T14:30:00Z"
}
```

#### Workflow 2: Using Apple Shortcuts
1. Apple Shortcut generates formatted time data
2. User pastes output or saves to file
3. `tt i` imports: `tt i` (paste) or `tt i file.txt` (from file)
4. Data automatically appended to markdown files

#### Workflow 3: Manual Entry
1. `tt a` prompts for entries
2. Format: `Category [> Subcategory], Duration, Description`
3. Example: `Sermon > Reading, 2h 30m, Isaiah study`

#### Workflow 4: Weekly Goal Planning
1. `tt g` opens interactive wizard
2. Prompts for each category
3. Saves to weekly_goals table
4. `tt` (default) shows progress against goals

### D. Status Command (Weekly Progress - Most Used)

This is the **default command** when running `tt` with no arguments.

**Output Display:**
- Shows active timer if running
- Progress bars for each category (color-coded)
- Percentage toward goal
- Remaining hours needed
- Per-day calculation to reach goal
- Total weekly hours vs. goal

**Colors (Omarchy Theme):**
- Green (#42): Time durations (achievements)
- Dark Blue (#67): Category names, headers
- Cyan (#80): Progress indicators
- Yellow (#226): Numbers, percentages
- Orange (#214): Remaining time warnings
- Grey (#240): Labels, separators

---

## 3. SQL USAGE DETAILS

### Database Operations

**Initialization:**
```javascript
const db = new sqlite3(DB_PATH);
db.exec(`...CREATE TABLE statements...`);
```

**Query Patterns:**

1. **Insert Entries**
```javascript
db.prepare(`
  INSERT INTO time_entries (category, subcategory, description, 
    start_time, end_time, duration_minutes, date)
  VALUES (?, ?, ?, ?, ?, ?, ?)
`).run(values...);
```

2. **Batch Inserts (Transactions)**
```javascript
const insertMany = db.transaction((entries) => {
  for (const entry of entries) {
    insert.run(...);
  }
});
insertMany(entries);
```

3. **Weekly Progress Queries**
```javascript
// Get this week's entries
db.prepare(`
  SELECT * FROM time_entries
  WHERE date >= ? AND date <= ?
  ORDER BY category, date, start_time
`).all(weekStart, weekEnd);

// Get weekly goals
db.prepare(`
  SELECT * FROM weekly_goals
  WHERE week_start = ?
`).all(weekStart);
```

4. **Aggregation**
```javascript
// By category
const byCategory = {};
for (const entry of entries) {
  byCategory[entry.category] += entry.duration_minutes;
}

// Time range queries
db.prepare(`
  SELECT * FROM time_entries
  WHERE date >= ? AND date <= ?
  ORDER BY date, start_time
`).all(startDate, endDate);
```

5. **Updates**
```javascript
// Rename category across all entries
db.prepare(`
  UPDATE time_entries SET category = ? WHERE category = ?
`).run(newName, oldName);

db.prepare(`
  UPDATE weekly_goals SET category = ? WHERE category = ?
`).run(newName, oldName);
```

**Key Points:**
- Uses `better-sqlite3` (synchronous, faster than async)
- Prepared statements prevent SQL injection
- Transactions for multi-operation consistency
- Indexes on: date, category, subcategory, week_start
- No complex JOINs (normalized schema keeps queries simple)

---

## 4. MARKDOWN FILES PROCESSING

### Markdown File Format

**Location:** `/home/user/repos/time_keeping/time_logs/`

**Naming Convention:** `YYYY_W[week]_time.md` (ISO week format)
- Example: `2025_W45_time.md` (Week 45 of 2025)
- Generated automatically by `getWeekFilename()` function

**File Structure:**
```markdown
# Time Log - Week 45, 2025

| Date       | Category             | Subcategory           | Start    | End      | Duration | Description |
| ---------- | -------------------- | --------------------- | -------- | -------- | -------- | ----------- |
| 2025-11-04 | Sinod                | homeless conversation | 09:11:13 | 16:05:45 | 6h 55m   |             |
| 2025-11-05 | Sermon               | eucharistie           | 10:29:20 | 12:35:55 | 2h 7m    |             |
| 2025-11-05 | Pastoral & Community | dementia dialogues    | 13:28:42 | 16:34:00 | 3h 5m    |             |
```

### Markdown Processing Pipeline

**1. Appending Entries**
- Helper script: `append_to_markdown.sh` (31 lines)
- Called by `appendToMarkdown()` function
- Process:
  1. Checks if file exists
  2. Creates header if needed (title + table header)
  3. Appends row with pipe-delimited format
  4. Called whenever entry is saved (db + markdown)

**Script Flow:**
```bash
# Takes 8 parameters:
# $1 = week file path
# $2 = date
# $3 = category
# $4 = subcategory
# $5 = start time
# $6 = end time
# $7 = duration
# $8 = description

# If file doesn't exist, create with header
# Then append table row
```

**2. ISO Week Calculation**
```javascript
function getWeekFilename(date = new Date()) {
  const d = new Date(date);
  const firstDayOfYear = new Date(d.getFullYear(), 0, 1);
  const pastDaysOfYear = (d - firstDayOfYear) / 86400000;
  const weekNum = Math.ceil((pastDaysOfYear + firstDayOfYear.getDay() + 1) / 7);
  
  const year = d.getFullYear();
  const weekStr = String(weekNum).padStart(2, '0');
  
  return `${year}_W${weekStr}_time.md`;
}
```

### Data Backup

- Markdown files serve as **secondary data backup**
- Primary: SQLite database
- Markdown provides human-readable archive
- Both updated whenever entry saved

---

## 5. CALLBACK FEATURE & REAL-TIME ANALYTICS

### "Callback Feature" = Timer Persistence

The "callback" refers to the **active timer system** that allows users to:
1. Start timer on one device
2. Switch to another device (iPhone via Shortcuts)
3. Stop timer on different device
4. State persists across sessions

**Implementation:**
```javascript
const TIMER_PATH = path.join(__dirname, '.active-timer.json');

function saveTimer(timerData) {
  fs.writeFileSync(TIMER_PATH, JSON.stringify(timerData, null, 2));
}

function loadTimer() {
  if (fs.existsSync(TIMER_PATH)) {
    const data = fs.readFileSync(TIMER_PATH, 'utf-8');
    return JSON.parse(data);
  }
  return null;
}

function getTimerDuration(startTime) {
  const start = new Date(startTime);
  const now = new Date();
  const diffMs = now - start;
  return Math.floor(diffMs / 1000 / 60); // minutes
}
```

**Features:**
- Survives shell restarts
- Cross-device compatible (if using SSH)
- Shows active timer on `tt` (status) command
- Can check duration anytime: `getTimerDuration(timer.startTime)`

### "Real-time Analytics" = Weekly Progress Tracking

The system provides real-time insights through the `cmdStatus()` function:

**What It Calculates:**
1. **Actuals vs. Goals**: Compares tracked hours to weekly targets
2. **Progress Percentage**: (actual / goal) × 100
3. **Remaining Hours**: Max(0, goal - actual)
4. **Per-Day Calculation**: remaining_hours / remaining_days_in_week
5. **Visual Progress Bars**: Color-coded by percentage (25%, 50%, 75%, 100%)
6. **Today's Total**: Separate metric for daily tracking

**Real-Time Data Available:**
```javascript
const weekTotal = entries.reduce((sum, e) => sum + e.duration_minutes, 0);
const todayTotal = todayEntries.reduce((sum, e) => sum + e.duration_minutes, 0);
const remainingDays = 7 - new Date().getDay();
const perDayNeeded = totalRemaining / remainingDays;
```

**Display Features:**
- Active timer display (if running)
- Progress bars for each category
- Percentage complete for week
- Hours needed per remaining day
- Calculations for goal achievement/excess

---

## 6. OVERALL STRUCTURE & DEPENDENCIES

### Directory Structure

```
time_keeping/
├── tt                              # Main CLI executable (1,558 lines)
├── tt_local                        # Bash helper for interactive tracking
├── tt_local_shortcuts              # Bash helper for Apple Shortcuts integration
├── append_to_markdown.sh           # Helper to append entries to markdown files
├── backup.sh                       # Database backup script
├── timetracking.db                 # SQLite database (84 KB)
├── .active-timer.json              # Active timer state (when running)
├── 
├── time_logs/                      # Weekly markdown files
│   ├── 2025_W45_time.md           # Week 45 data
│   ├── 2025_W46_time.md           # Week 46 data
│   └── ...                        # One file per week
├──
├── package.json                    # Dependencies (better-sqlite3, googleapis)
├── package_lock.json               # Locked versions
├── node_modules/                   # npm packages
│
├── DESIGN.md                       # Living design documentation
├── README.md                       # User guide
├── DESIGN.md                       # Architecture docs
├── project_structure.md            # Folder organization
└── [Other documentation files]
```

### Key Dependencies

**package.json:**
```json
{
  "name": "time-tracking",
  "version": "3.0.0",
  "description": "Ministry time tracking with SQLite & Apple Shortcut support",
  "dependencies": {
    "better-sqlite3": "^11.0.0",   // Fast sync SQLite binding
    "googleapis": "^105.0.0"       // Google Sheets API (for exports)
  }
}
```

**better-sqlite3:**
- Synchronous SQLite bindings
- Faster than async libraries
- Required for CLI performance
- Native C++ binding

**googleapis:**
- Only used for CSV export to Google Sheets
- Not core to time tracking functionality

### Core Functions (Key Components)

**Database Management:**
- `initDatabase()` - Initialize/create schema
- `importEntries(db, entries)` - Batch import

**Time Parsing & Formatting:**
- `parseDateTime(dateStr)` - Parse Apple Shortcut format
- `formatDuration(minutes)` - Convert to "Xh Ym" format
- `parseDuration(durationStr)` - Parse "2h 30m", "150m", etc.
- `calculateDuration(start, end)` - Get minutes between times
- `formatAppleShortcutTime(date)` - Format for Shortcut output
- `getWeekStart()` / `getWeekEnd()` - Week boundaries
- `getWeekFilename()` - Generate ISO week filename

**Timer Management:**
- `saveTimer(timerData)` - Save active timer
- `loadTimer()` - Retrieve active timer
- `clearTimer()` - Delete timer state
- `getTimerDuration(startTime)` - Calculate elapsed time

**Apple Shortcut Integration:**
- `parseShortcutData(content)` - Parse Shortcut format with subcategories
- Format expected:
  ```
  ———
  [Category]
  [Optional Subcategory]
  Start time: DD MMM YYYY at HH:MM:SS
  until
  End Time: DD MMM YYYY at HH:MM:SS
  ———
  ```

**Markdown Operations:**
- `appendToMarkdown(category, subcategory, startDate, endDate, description)`
- Calls bash helper script for file operations

**SQL Query Functions:**
- `cmdStatus()` - Weekly progress + active timer
- `cmdToday()` - Today's entries by time
- `cmdWeek()` - Last 7 days grouped by date
- `cmdMonth()` - Current month by category
- `cmdStats()` - Overall statistics
- `cmdExport()` - Export to CSV

**Goal Management:**
- `cmdGoalWizard()` - Interactive weekly goal setting
- Supports: Enter existing, update, or skip with "0"

**Data Management:**
- `cmdRenameCategory(oldName, newName)` - Retroactive renaming
- Updates: entries, goals, history log

---

## 7. FEATURE ANALYSIS

### Implemented Features ✓

1. **Time Tracking**
   - Manual start/stop via CLI (`tt s` / `tt e`)
   - Apple Shortcut import (paste or file)
   - Manual entry addition (`tt a`)
   - Subcategory support

2. **Data Persistence**
   - SQLite database (primary)
   - Weekly markdown files (secondary, human-readable)
   - Active timer JSON state (cross-session)

3. **Weekly Goals**
   - Set goals per category
   - Visual progress bars
   - Percentage calculations
   - Per-day remaining hours
   - Editable goals (press Enter to keep)

4. **Reporting**
   - Daily entries (`tt t`)
   - Weekly summary (`tt w`)
   - Monthly breakdown (`tt m`)
   - Entry listing (`tt l`)
   - Full statistics (`tt st`)
   - CSV export (`tt x`)

5. **Category Management**
   - Subcategories (7 main, multiple subs)
   - Retroactive renaming across all data
   - History logging

6. **UI/UX**
   - Omarchy color theme
   - Interactive CLI prompts
   - Progress bar visualization
   - Responsive design for terminal
   - Context-sensitive help

### Not Implemented (By Design)

- ❌ Web/GUI interface (CLI-only)
- ❌ Real-time notifications
- ❌ Automatic time detection
- ❌ Cross-device sync (except via SSH)
- ❌ Advanced analytics/ML
- ❌ Team features
- ❌ Cloud storage (local only)

---

## 8. DATA FLOW DIAGRAMS

### Import Flow
```
Apple Shortcut Output
    ↓
parseShortcutData() → Array of {category, subcategory, startTime, endTime}
    ↓
importEntries() → SQLite database INSERT
    ↓
appendToMarkdown() → Append to markdown file
    ↓
Display summary by category
```

### Status/Progress Flow
```
getWeekStart() → Query weekly_goals
    ↓
SELECT time_entries WHERE date BETWEEN week_start AND week_end
    ↓
Group by category → Calculate actuals
    ↓
Compare actuals to goals
    ↓
Calculate: percentage, remaining, per-day needed
    ↓
Render with color-coded progress bars
```

### Timer Flow
```
cmdStartTimer() → Get category/subcategory
    ↓
saveTimer() → Write .active-timer.json
    ↓
cmdStatus() → Display active timer info
    ↓
cmdEndTimer() → Load timer, calculate duration
    ↓
Insert to DB + appendToMarkdown() + clearTimer()
```

---

## 9. KEY CODE EXAMPLES

### Example 1: Starting a Timer
```javascript
async function cmdStartTimer() {
  const existingTimer = loadTimer();
  if (existingTimer) {
    console.log(`⏱️  Timer already running!`);
    return;
  }
  
  const category = await prompt("Select category: ");
  const subcategory = await prompt("Subcategory (optional): ");
  
  const timerData = {
    category,
    subcategory,
    startTime: new Date().toISOString()
  };
  
  saveTimer(timerData);
  console.log(`✓ Timer started!`);
}
```

### Example 2: Weekly Progress Query
```javascript
function cmdStatus() {
  const weekStart = getWeekStart();
  const weekEnd = getWeekEnd();
  
  const entries = db.prepare(`
    SELECT * FROM time_entries
    WHERE date >= ? AND date <= ?
  `).all(weekStart, weekEnd);
  
  const goals = db.prepare(`
    SELECT * FROM weekly_goals
    WHERE week_start = ?
  `).all(weekStart);
  
  // Calculate actuals by category
  const actuals = {};
  for (const entry of entries) {
    actuals[entry.category] = (actuals[entry.category] || 0) + 
                               entry.duration_minutes;
  }
  
  // Display with progress bars
  for (const goal of goals) {
    const actual = actuals[goal.category] || 0;
    const percentage = (actual / goal.goal_minutes) * 100;
    const bar = colorProgressBar(percentage);
    console.log(`${goal.category} ${bar} ${percentage}%`);
  }
}
```

### Example 3: Parsing Apple Shortcut Data
```javascript
function parseShortcutData(content) {
  const entries = [];
  const sections = content.split('———').filter(s => s.trim());
  
  for (const section of sections) {
    const lines = section.trim().split('\n').filter(l => l.trim());
    
    let category = lines[0].trim();
    let subcategory = null;
    let startTime = null;
    let endTime = null;
    
    // Check if second line is subcategory
    if (lines[1] && !lines[1].startsWith('Start time:')) {
      if (lines[2]?.startsWith('Start time:')) {
        subcategory = lines[1].trim();
      }
    }
    
    // Find start and end times
    for (const line of lines) {
      if (line.startsWith('Start time:')) {
        startTime = line.replace('Start time:', '').trim();
      }
      if (line.startsWith('End Time:')) {
        endTime = line.replace('End Time:', '').trim();
      }
    }
    
    if (category && startTime && endTime) {
      entries.push({ category, subcategory, startTime, endTime });
    }
  }
  
  return entries;
}
```

---

## 10. DESIGN PATTERNS & BEST PRACTICES

**Patterns Used:**
1. **Command Pattern** - Each command is a function (cmdStatus, cmdImport, etc.)
2. **Singleton** - Database initialized once, passed to functions
3. **Transaction Pattern** - Batch imports wrapped in db.transaction()
4. **State File Pattern** - Timer state persisted in JSON
5. **Markdown Table Format** - Human-readable data storage

**Best Practices:**
- ✓ Prepared statements (prevent SQL injection)
- ✓ Transaction support for multi-step operations
- ✓ ISO week format for consistency
- ✓ Color-coded UI for accessibility
- ✓ Fallback defaults (empty subcategory allowed)
- ✓ Error handling with user-friendly messages
- ✓ Logging changes (category_history table)

**Security Considerations:**
- Local file only (no cloud exposure)
- Prepared statements prevent injection
- No authentication (single-user, local)
- File permissions on scripts (755)

---

## 11. CURRENT LIMITATIONS & FUTURE ENHANCEMENTS

### Current Limitations
1. No multi-device sync (except SSH)
2. No automatic time capture
3. No mobile-native app
4. No web interface
5. Manual start/stop only
6. No advanced analytics

### Planned Enhancements
- [ ] Auto-import from Shortcuts folder
- [ ] Daily digest emails
- [ ] Goal recommendations
- [ ] Year-over-year comparisons
- [ ] Web dashboard (optional)
- [ ] Mobile app wrapper

---

## SUMMARY TABLE

| Aspect | Details |
|--------|---------|
| **Language** | JavaScript (Node.js) |
| **Database** | SQLite (better-sqlite3) |
| **CLI Framework** | Native readline module |
| **Main File** | `tt` (1,558 lines) |
| **Database Size** | ~84 KB |
| **Records** | 279+ entries |
| **Categories** | 7 main + subcategories |
| **Markdown Files** | Weekly (ISO format) |
| **Data Persistence** | DB + Markdown + JSON timer |
| **Color Theme** | Omarchy (green/dark blue) |
| **Key Commands** | tt, tt s, tt e, tt g, tt i, tt a |
| **Version** | 3.0 |

---

**Last Updated:** Nov 13, 2025
**Analysis Date:** Current exploration session
