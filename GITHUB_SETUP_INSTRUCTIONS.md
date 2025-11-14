# GitHub Setup Instructions for Standalone Repos

## After Restart - Link Repos to GitHub

### Step 1: Create GitHub Repos (Do This First!)

Go to GitHub and create two **NEW** repositories:

1. **Aster Repo:**
   - Name: `aster`
   - Description: "Document processing system with audio transcription"
   - **Important:** Do NOT initialize with README, .gitignore, or license
   - Keep it completely empty

2. **Strudel Repo:**
   - Name: `strudel`
   - Description: "Sheet music converter with audio analysis"
   - **Important:** Do NOT initialize with README, .gitignore, or license
   - Keep it completely empty

---

### Step 2: Link and Push Aster

Open a terminal and run:

```bash
# Navigate to aster standalone
cd ~/Documents/Applications/aster_standalone

# Verify it's a git repo
git status

# Add GitHub remote
git remote add origin https://github.com/Eenjaco/aster.git

# Push to GitHub
git push -u origin main

# Verify it worked
git remote -v
```

**Expected output:**
```
origin  https://github.com/Eenjaco/aster.git (fetch)
origin  https://github.com/Eenjaco/aster.git (push)
```

---

### Step 3: Link and Push Strudel

In the same terminal (or open a new one):

```bash
# Navigate to strudel standalone
cd ~/Documents/Applications/strudel_standalone

# Verify it's a git repo
git status

# Add GitHub remote
git remote add origin https://github.com/Eenjaco/strudel.git

# Push to GitHub
git push -u origin main

# Verify it worked
git remote -v
```

**Expected output:**
```
origin  https://github.com/Eenjaco/strudel.git (fetch)
origin  https://github.com/Eenjaco/strudel.git (push)
```

---

## Quick Reference: Your New Workflow

### Terminal 1 - Aster Work:
```bash
cd ~/Documents/Applications/aster_standalone
git status
# Make changes...
git add .
git commit -m "Your commit message"
git push
```

### Terminal 2 - Strudel Work:
```bash
cd ~/Documents/Applications/strudel_standalone
git status
# Make changes...
git add .
git commit -m "Your commit message"
git push
```

---

## Running Aster Training

When you're ready to resume training:

```bash
cd ~/Documents/Applications/aster_standalone
python3 process_training_data.py --resume
```

This will:
- Skip the 16 files already processed
- Skip the 9 audio files already done
- Process the remaining ~118 files

---

## Troubleshooting

### If "remote already exists":
```bash
git remote remove origin
git remote add origin https://github.com/Eenjaco/aster.git
```

### If push is rejected:
```bash
git push -u origin main --force-with-lease
```

### If you need to check what's in a repo:
```bash
git log --oneline
git status
ls -la
```

---

## Old Monorepo Location

The old monorepo still exists at:
```
~/Documents/Applications/repos/
```

You can keep it as a backup or delete it later. All your work is safely copied to the standalone repos.

---

## Summary

✅ **Aster standalone:** `/Users/mac/Documents/Applications/aster_standalone/`
✅ **Strudel standalone:** `/Users/mac/Documents/Applications/strudel_standalone/`
✅ **Simple branches:** Both use `main` (no more long convoluted names!)
✅ **Independent repos:** No more branch confusion
✅ **Training ready:** Run `process_training_data.py --resume` when ready

---

**Good luck!** 🚀
