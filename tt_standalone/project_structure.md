# Time Keeping - Project Structure

## 📁 Clean Folder Organization

```
Time Keeping/
│
├── 🎯 Active Files (Use These!)
│   ├── tt                      # CLI tool - your main command
│   ├── timetracking.db         # SQLite database (279 entries, 503h 48m)
│   ├── backup.sh               # Weekly backup script
│   └── package.json            # Dependencies (better-sqlite3)
│
├── 📚 Documentation
│   ├── DESIGN.md               # Living design document
│   ├── QUICK-REF.md            # Quick command reference
│   ├── QUICK-START-v3.md       # Getting started guide
│   ├── COLOR-GUIDE.md          # Color customization
│   ├── BACKUP-GUIDE.md         # Backup instructions
│   └── PROJECT-STRUCTURE.md    # This file
│
├── 💾 Backups
│   └── backups/
│       └── timetracking-YYYY-MM-DD.db   # Dated backups (auto-cleanup)
│
├── 📦 Archive (Historical)
│   └── archive/
│       ├── old-tsx-files/      # 16 React dashboards (v1.0)
│       ├── old-scripts/        # CSV export scripts (v1.0, v2.0)
│       └── old-docs/           # Superseded documentation
│
└── 🔧 Dependencies
    └── node_modules/           # npm packages (better-sqlite3)
```

---

## 🚀 Quick Start

### Your Daily Commands

```bash
tt              # Check weekly progress
tt s            # Start timer
tt e            # End timer
tt g            # Set weekly goals
```

**That's it!** Those 4 commands handle 90% of your usage.

---

## 📊 What's What

### Active System Files

| File | Purpose | Touch It? |
|------|---------|-----------|
| `tt` | CLI executable | Only to customize colors |
| `timetracking.db` | All your data | Never directly - use `tt` commands |
| `backup.sh` | Backup script | Run `./backup.sh` anytime |
| `package.json` | npm config | Only if adding dependencies |

### Documentation Files

| File | When to Read |
|------|--------------|
| `QUICK-REF.md` | Quick command lookup |
| `DESIGN.md` | Understand system architecture |
| `COLOR-GUIDE.md` | Want to change colors |
| `BACKUP-GUIDE.md` | Set up automated backups |

### Folders

| Folder | Purpose |
|--------|---------|
| `backups/` | Database backups (auto-managed) |
| `archive/` | Old files from v1.0 & v2.0 |
| `node_modules/` | npm packages (auto-managed) |

---

## 🎨 Current Version: 3.0

**Features:**
- ✅ Super-short CLI commands (`tt`, `tt s`, `tt e`, `tt g`)
- ✅ SQLite database (fast, local, reliable)
- ✅ Real-time timer with category selection
- ✅ Weekly goal tracking with visual progress
- ✅ Omarchy color theme (green + dark grey-blue)
- ✅ Active timer display in status
- ✅ Apple Shortcut integration
- ✅ Subcategory support
- ✅ Retroactive category renaming
- ✅ CSV export for Google Sheets
- ✅ Automated backup script

**Stats:**
- 279 entries tracked
- 503h 48m total time
- 7 categories
- Database: 84 KB

---

## 🗂️ Where Everything Lives

### Main Command
```bash
/Users/mac/Documents/Terminal/Claude/Projects/Time Keeping/tt
```

But since it's globally installed via npm, just type:
```bash
tt
```

### Database
```bash
/Users/mac/Documents/Terminal/Claude/Projects/Time Keeping/timetracking.db
```

### Backups
```bash
/Users/mac/Documents/Terminal/Claude/Projects/Time Keeping/backups/
```

---

## 🧹 Cleanup Complete!

**Moved to archive:**
- 16 .tsx React dashboard files
- Old CSV export scripts
- Superseded documentation
- Old track.js (v2.0 CLI)

**Removed:**
- All .DS_Store files
- Old CSV exports
- Duplicate files

**Result:** Clean, organized project with only active files in root!

---

## 📱 Future: SSH/Phone Access

**Plan:** Access `tt` from phone via SSH using terminal emulators:
- a-Shell (iOS)
- Blink Shell (iOS)
- Terminus (iOS)

This will enable you to:
```bash
ssh mac@your-laptop
tt s            # Start timer from phone
# ... do work ...
tt e            # End timer from phone
```

**Setup:** Coming soon (need to configure SSH on laptop)

---

## 🔄 Version History

| Version | Date | Key Features |
|---------|------|--------------|
| **v1.0** | Oct 30 | CSV export from .tsx files |
| **v2.0** | Oct 30 | SQLite database + CLI tool |
| **v3.0** | Oct 31 | Timer commands + Omarchy colors + backups |

---

## 💡 Tips

1. **Just run `tt`** - That's your go-to command for checking progress
2. **Set goals Monday** - `tt g` to set the week's targets
3. **Use the timer** - `tt s` and `tt e` for real-time tracking
4. **Backup before changes** - Run `./backup.sh` before major edits
5. **Explore colors** - See `COLOR-GUIDE.md` to customize

---

**Organization Date:** 2025-10-31
**System Status:** ✅ Clean, organized, production-ready
