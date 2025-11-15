# Terminal Setup Guide

Complete guide for setting up the Time Tracker in a new terminal session.

## Table of Contents

1. [First Time Setup](#first-time-setup)
2. [Daily Workflow](#daily-workflow)
3. [Virtual Environment Setup](#virtual-environment-setup)
4. [Git Branch Setup](#git-branch-setup)
5. [Background Services](#background-services)
6. [Troubleshooting](#troubleshooting)

---

## First Time Setup

### Option 1: Quick Install (Recommended)

```bash
# Clone or navigate to the repo
cd /Users/mac/Documents/Applications/tt_standalone

# Run installation script (checks existing dependencies)
./install.sh

# Test the CLI
./tt
```

The install script will:
- ✅ Check for Python, Node.js, Git
- ✅ Install watchdog (if missing)
- ✅ Verify npm packages
- ✅ Check database
- ✅ Set executable permissions
- ✅ Offer to create virtual environment

### Option 2: Manual Setup

```bash
# Navigate to repo
cd /Users/mac/Documents/Applications/tt_standalone

# Install Node.js dependencies
npm install

# Install Python dependencies
pip3 install watchdog

# Make scripts executable
chmod +x tt tt_local tt_local_shortcuts watch_markdown.py
chmod +x sync push-now quick-commit install.sh

# Test
./tt
```

---

## Daily Workflow

### Opening a New Terminal

```bash
# Navigate to repo
cd /Users/mac/Documents/Applications/tt_standalone

# If using virtual environment (optional)
source venv/bin/activate

# Check status
./tt

# Start working!
```

### Quick Commands

```bash
# Time tracking
./tt              # Show weekly progress
./tt s            # Start timer
./tt e            # End timer
./tt t            # Today's entries

# Git operations
./sync            # Pull latest changes
git status        # Check what changed
./quick-commit "message"  # Add, commit, push

# File watcher
python3 watch_markdown.py  # Auto-sync markdown → SQLite
```

---

## Virtual Environment Setup

### Why Use a Virtual Environment?

- ✅ Isolates Python packages from system
- ✅ Prevents version conflicts
- ✅ Clean uninstall (just delete `venv/`)
- ❌ Adds extra step (activation) each session

### Create Virtual Environment

```bash
# In project directory
cd /Users/mac/Documents/Applications/tt_standalone

# Create venv
python3 -m venv venv

# Activate
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install watchdog

# Test
python3 watch_markdown.py
```

### Using the Virtual Environment

**Every new terminal session:**

```bash
cd /Users/mac/Documents/Applications/tt_standalone
source venv/bin/activate   # Notice (venv) prefix in prompt
```

**When done:**

```bash
deactivate  # Exit virtual environment
```

### Auto-Activate (Optional)

Add to `~/.zshrc` or `~/.bash_profile`:

```bash
# Auto-activate tt_standalone venv when cd'ing into directory
cd() {
  builtin cd "$@"
  if [[ -f "$(pwd)/venv/bin/activate" ]]; then
    source venv/bin/activate
  fi
}
```

**Or use direnv:**

```bash
# Install direnv
brew install direnv

# Add to ~/.zshrc
eval "$(direnv hook zsh)"

# In project directory, create .envrc
echo "source venv/bin/activate" > .envrc
direnv allow .

# Now auto-activates when entering directory!
```

---

## Git Branch Setup

### Check Current Branch

```bash
git branch --show-current
```

### Create and Switch to Development Branch

```bash
# Create new branch
git checkout -b feature/obsidian-integration

# Or switch to existing branch
git checkout main
```

### Track Remote Branch

```bash
# If branch exists on remote
git fetch origin
git checkout -b feature/watchdog origin/feature/watchdog

# Or create and push new branch
git checkout -b feature/new-feature
git push -u origin feature/new-feature
```

### Branch Workflow

```bash
# Start working on feature
git checkout -b feature/my-feature

# Make changes
./tt s  # work...
./tt e

# Commit and push
./quick-commit "Add watchdog auto-sync"

# When feature is done, merge to main
git checkout main
git merge feature/my-feature
git push
```

---

## Background Services

### Running Watchdog in Background

**Option 1: Terminal in Background**

```bash
# Start in background
python3 watch_markdown.py &

# Check if running
ps aux | grep watch_markdown

# Stop
pkill -f watch_markdown
```

**Option 2: tmux/screen (Persistent)**

```bash
# Install tmux
brew install tmux

# Start tmux session
tmux new -s watcher

# Run watcher
python3 watch_markdown.py

# Detach: Ctrl+B, then D
# Reattach later: tmux attach -t watcher
```

**Option 3: launchd (Auto-start on Mac)**

Create `~/Library/LaunchAgents/com.timetracker.watcher.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.timetracker.watcher</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/Users/mac/Documents/Applications/tt_standalone/watch_markdown.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/tt_watcher.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/tt_watcher_error.log</string>
</dict>
</plist>
```

Load service:

```bash
launchctl load ~/Library/LaunchAgents/com.timetracker.watcher.plist

# Check status
launchctl list | grep timetracker

# Stop service
launchctl unload ~/Library/LaunchAgents/com.timetracker.watcher.plist
```

---

## Shell Aliases (Optional)

Add to `~/.zshrc` or `~/.bash_profile`:

```bash
# Time Tracker aliases
alias tt='cd /Users/mac/Documents/Applications/tt_standalone && ./tt'
alias tts='cd /Users/mac/Documents/Applications/tt_standalone && ./tt s'
alias tte='cd /Users/mac/Documents/Applications/tt_standalone && ./tt e'
alias ttwatch='cd /Users/mac/Documents/Applications/tt_standalone && python3 watch_markdown.py'
alias ttcd='cd /Users/mac/Documents/Applications/tt_standalone'

# Git shortcuts (when in tt directory)
alias ttsync='./sync'
alias ttpush='./push-now'
alias ttcommit='./quick-commit'
```

Reload shell:

```bash
source ~/.zshrc  # or source ~/.bash_profile
```

Now from anywhere:

```bash
tt      # Show progress
tts     # Start timer
tte     # End timer
ttcd    # Go to project directory
```

---

## Full Session Examples

### Example 1: Fresh Terminal, Start Working

```bash
# Open terminal
cd /Users/mac/Documents/Applications/tt_standalone
source venv/bin/activate  # If using venv

# Check status
./tt

# Start timer
./tt s
# Select: Sermon → Writing

# [Work for 2 hours...]

# Stop timer
./tt e

# Check progress
./tt
```

### Example 2: New Terminal, Resume Active Timer

```bash
cd /Users/mac/Documents/Applications/tt_standalone

# CLI automatically detects active timer
./tt
# Output shows: "⏱️ Active timer: Sermon/Writing (45m elapsed)"

# When done
./tt e
```

### Example 3: Set Up Watchdog on Startup

```bash
# Terminal 1: Development
cd /Users/mac/Documents/Applications/tt_standalone
./tt s
# Work...

# Terminal 2: Watcher (background)
cd /Users/mac/Documents/Applications/tt_standalone
python3 watch_markdown.py &

# Now Obsidian changes auto-sync!
```

### Example 4: Work on Feature Branch

```bash
cd /Users/mac/Documents/Applications/tt_standalone

# Create feature branch
git checkout -b feature/improve-analytics

# Make changes to tt script...

# Test
./tt

# Commit
./quick-commit "Improve weekly analytics display"

# Merge when ready
git checkout main
git merge feature/improve-analytics
git push
```

---

## Troubleshooting

### "command not found: ./tt"

```bash
# Make executable
chmod +x tt

# Or run via node
node tt
```

### "Module 'better-sqlite3' not found"

```bash
# Reinstall dependencies
npm install
```

### "watchdog not installed"

```bash
# Install globally
pip3 install watchdog

# Or in venv
source venv/bin/activate
pip install watchdog
```

### Database locked error

```bash
# Check for other processes
lsof timetracking.db

# Kill if needed
pkill -f "node.*tt"
```

### Watchdog not detecting changes

```bash
# Check if running
ps aux | grep watch_markdown

# Check file permissions
ls -la time_logs/

# Manual test
echo "| 2025-11-14 | Test | test | 10:00 | 11:00 | 1h | test |" >> time_logs/test.md
```

### Virtual environment issues

```bash
# Recreate venv
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install watchdog
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Navigate to project | `cd /Users/mac/Documents/Applications/tt_standalone` |
| Activate venv | `source venv/bin/activate` |
| Install all deps | `./install.sh` |
| Show progress | `./tt` |
| Start timer | `./tt s` |
| Stop timer | `./tt e` |
| Pull changes | `./sync` |
| Commit & push | `./quick-commit "message"` |
| Start watcher | `python3 watch_markdown.py` |
| Check branch | `git branch --show-current` |
| Switch branch | `git checkout branch-name` |

---

## Recommended Terminal Setup

For the smoothest experience:

1. ✅ **Use aliases** (add to ~/.zshrc)
2. ✅ **Use tmux** for persistent watcher
3. ✅ **Use direnv** for auto venv activation
4. ✅ **Set up launchd** for auto-start watcher
5. ✅ **Keep separate terminal tabs**:
   - Tab 1: CLI work (`./tt`)
   - Tab 2: Watcher (`python3 watch_markdown.py`)
   - Tab 3: General dev

Happy time tracking! 🎉
