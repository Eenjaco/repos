# Database Backup Guide

## Quick Backup

**Run a backup anytime:**
```bash
cd "/Users/mac/Documents/Terminal/Claude/Projects/Time Keeping"
./backup.sh
```

This creates: `backups/timetracking-YYYY-MM-DD.db`

---

## What Gets Backed Up

- **Database:** `timetracking.db` (all entries, goals, history)
- **Current stats:** 279 entries, ~84 KB
- **Backup location:** `backups/` folder
- **Naming:** `timetracking-2025-10-31.db` (dated)

---

## Automatic Cleanup

The script **automatically deletes backups older than 8 weeks** (56 days).

This keeps your backups folder manageable while preserving ~2 months of history.

---

## Weekly Automation (Optional)

### Set up weekly backups with cron:

1. **Edit your crontab:**
   ```bash
   crontab -e
   ```

2. **Add this line** (runs every Sunday at 11 PM):
   ```bash
   0 23 * * 0 cd "/Users/mac/Documents/Terminal/Claude/Projects/Time Keeping" && ./backup.sh >> backups/backup.log 2>&1
   ```

3. **Save and exit** (in nano: Ctrl+X, then Y, then Enter)

### Verify it's scheduled:
```bash
crontab -l
```

---

## Alternative Schedule Options

**Daily at 11 PM:**
```bash
0 23 * * * cd "/Users/mac/Documents/Terminal/Claude/Projects/Time Keeping" && ./backup.sh >> backups/backup.log 2>&1
```

**Every Monday at 9 AM:**
```bash
0 9 * * 1 cd "/Users/mac/Documents/Terminal/Claude/Projects/Time Keeping" && ./backup.sh >> backups/backup.log 2>&1
```

**First day of every month at midnight:**
```bash
0 0 1 * * cd "/Users/mac/Documents/Terminal/Claude/Projects/Time Keeping" && ./backup.sh >> backups/backup.log 2>&1
```

---

## Restore from Backup

### View available backups:
```bash
ls -lh backups/
```

### Restore a backup:
```bash
cd "/Users/mac/Documents/Terminal/Claude/Projects/Time Keeping"

# 1. Backup current database first (safety!)
cp timetracking.db timetracking-current.db

# 2. Restore from backup
cp backups/timetracking-2025-10-31.db timetracking.db

# 3. Test it
tt st
```

### Undo restore (if needed):
```bash
cp timetracking-current.db timetracking.db
```

---

## Check Backup Log

If you set up cron automation, check the log:
```bash
tail -20 backups/backup.log
```

---

## Manual Backup Before Major Changes

**Before renaming categories, importing large data sets, etc:**
```bash
./backup.sh
```

You'll see confirmation:
```
✓ Database backed up: backups/timetracking-2025-10-31.db
  Size: 84K
  Entries: 279
```

---

## Backup to External Drive (Optional)

**For extra safety, copy backups folder to external drive:**
```bash
# Example: Copy to USB drive
cp -r backups /Volumes/MyUSB/time-tracker-backups/

# Or iCloud Drive
cp -r backups ~/Library/Mobile\ Documents/com~apple~CloudDocs/time-tracker-backups/
```

**Set up automatic sync:**
```bash
# Add to crontab (runs after weekly backup)
5 23 * * 0 cp -r "/Users/mac/Documents/Terminal/Claude/Projects/Time Keeping/backups" ~/Library/Mobile\ Documents/com~apple~CloudDocs/
```

---

## Troubleshooting

### "Permission denied"
```bash
chmod +x backup.sh
```

### "timetracking.db not found"
Make sure you're in the project directory:
```bash
cd "/Users/mac/Documents/Terminal/Claude/Projects/Time Keeping"
./backup.sh
```

### Check if cron is running
```bash
# View system log
log show --predicate 'eventMessage contains "cron"' --last 1h
```

---

## Files

- **Backup script:** `backup.sh`
- **Backups folder:** `backups/`
- **Main database:** `timetracking.db`
- **Backup log:** `backups/backup.log` (if using cron)

---

## Quick Reference

| Command | What It Does |
|---------|--------------|
| `./backup.sh` | Create backup now |
| `ls -lh backups/` | List all backups |
| `crontab -e` | Edit cron schedule |
| `crontab -l` | View cron schedule |
| `tail backups/backup.log` | Check backup log |

---

**Remember:** Backups are your safety net. Run `./backup.sh` before making major changes!
