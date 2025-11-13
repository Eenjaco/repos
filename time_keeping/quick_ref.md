# tt - Quick Reference Card

## Super Quick Commands

| Command | What It Does |
|---------|--------------|
| `tt` | Show weekly progress (default) |
| `tt g` | Set weekly goals |
| `tt a` | Add entries |
| `tt i <file>` | Import data |
| `tt t` | Today |
| `tt w` | Week |
| `tt m` | Month |
| `tt l` | List entries |
| `tt st` | Stats |
| `tt x` | Export |
| `tt h` | Help |

---

## Your Weekly Rhythm

### Monday Morning
```bash
tt g    # Set goals for the week
```

### Throughout the Week
```bash
tt      # Check progress anytime
```

### Friday Afternoon
```bash
tt w    # Review the week
tt x    # Export to Google Sheets
```

---

## Common Tasks

### Check Your Progress
```bash
tt              # Weekly progress
tt t            # Today's detail
tt w            # Week summary
tt m            # Month summary
```

### Add Time Entries
```bash
tt a
# Then paste:
# Sermon, 2h 30m, Reading Isaiah
# Operations > Planning, 1h 15m, Weekly schedule
# Ctrl+D when done
```

### Import from Apple Shortcut
```bash
tt i mydata.txt
```

### View Recent Work
```bash
tt l            # Last 20 entries
tt l 50         # Last 50 entries
tt ls 10        # Alternative (ls = list)
```

### Database Info
```bash
tt st           # Statistics
```

### Export to Sheets
```bash
tt x            # Creates CSVs
```

---

## All Command Aliases

| Short | Long | Alternative |
|-------|------|-------------|
| `tt` | `tt status` | `tt s` |
| `tt g` | `tt goals` | `tt goal-wizard` |
| `tt a` | `tt add` | |
| `tt i` | `tt import` | |
| `tt t` | `tt today` | |
| `tt w` | `tt week` | |
| `tt m` | `tt month` | |
| `tt l` | `tt list` | `tt ls` |
| `tt st` | `tt stats` | |
| `tt x` | `tt export` | `tt e` |
| `tt rn` | `tt rename` | `tt rename-category` |
| `tt h` | `tt help` | |

---

## Advanced

### Rename Category (Retroactive!)
```bash
tt rn "Operations" "Bestuur"
# Updates ALL 269+ historical entries
```

### Add with Subcategories
```bash
tt a
# Sermon > Reading, 2h 30m, Isaiah study
# Operations > Planning, 1h, Weekly calendar
# Pastoral > Visits, 2h, Hospital visit
```

---

## Pro Tips

### Just Type `tt`
- No command needed for your most common action (status)
- Quick check: `tt`
- That's it!

### Short is Sweet
- All commands have 1-2 letter shortcuts
- `tt g` beats `tt goal-wizard`
- `tt l` beats `tt list`
- `tt st` beats `tt stats`

### Works Anywhere
- No need to `cd` to project folder
- Just type `tt` from any directory

### Goal-Oriented Workflow
```bash
# Monday
tt g            # Set: Sermon 12h, Ops 8h, Pastoral 5h

# Wednesday check
tt              # Sermon: 8h/12h (67%) ← 4h remaining

# Thursday check
tt              # Sermon: 10h/12h (83%) ← 2h remaining

# Friday
tt w            # Review week
tt x            # Export if needed
```

---

## Remember

**Most common workflow:**
1. Monday: `tt g` (set goals)
2. Daily: `tt` (check progress)
3. Friday: `tt w` (review)

**That's it!** Just 3 commands for 90% of your usage.

---

## Full Help
```bash
tt h            # See all commands and examples
```

---

**Tip:** Bookmark this file for quick reference!

**Location:** `~/Documents/Terminal/Claude/Projects/Time Keeping/QUICK-REF.md`
