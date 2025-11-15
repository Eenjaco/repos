# Script Standards and Git Shortcuts

## Installation Scripts - ALWAYS Include Smart Checking

Every installation script MUST check before installing to avoid:

❌ Long reinstalls of existing packages
❌ Warning spam from brew/apt
❌ Wasted time and bandwidth
❌ Breaking existing installations

## Required Functions

Include these functions in ALL installation scripts:

```bash
# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if brew package installed (macOS)
brew_installed() {
    if [[ "$OS" == "macos" ]]; then
        brew list "$1" &>/dev/null
    else
        return 1
    fi
}

# Install brew package only if missing
brew_install_if_missing() {
    for package in "$@"; do
        if brew_installed "$package"; then
            echo -e "${GREEN}✓${NC} Already installed: $package"
        else
            echo -e "${YELLOW}Installing $package...${NC}"
            brew install "$package"
        fi
    done
}

# Check if pip package installed
pip_installed() {
    python3 -m pip show "$1" &>/dev/null
}

# Install pip package only if missing
pip_install_if_missing() {
    for package in "$@"; do
        if pip_installed "$package"; then
            echo -e "${GREEN}✓${NC} Already installed: $package"
        else
            echo -e "${YELLOW}Installing $package...${NC}"
            pip install "$package"
        fi
    done
}

# Check if directory exists
dir_exists() {
    [[ -d "$1" ]]
}
```

## Usage Examples

### Installing System Packages

```bash
# ❌ BAD - Always reinstalls
brew install python node ffmpeg

# ✅ GOOD - Checks first
brew_install_if_missing python node ffmpeg
```

### Installing Python Packages

```bash
# ❌ BAD - Always reinstalls
pip install numpy pandas librosa

# ✅ GOOD - Checks first
pip_install_if_missing numpy pandas librosa
```

### Installing to Directories

```bash
# ❌ BAD - Doesn't check
curl -o ~/tools/sometool.zip https://example.com/tool.zip

# ✅ GOOD - Checks first
if [[ -d "$HOME/tools/sometool" ]]; then
    echo "✓ Already installed: sometool"
else
    echo "Installing sometool..."
    curl -o ~/tools/sometool.zip https://example.com/tool.zip
    unzip ~/tools/sometool.zip
fi
```

## Benefits

Scripts with smart checking:

✅ Safe to run multiple times
✅ Much faster on subsequent runs
✅ Clear status output
✅ No reinstall warnings
✅ Idempotent (same result every time)

## Example Output

**Without checking:**
```
Warning: python@3.11 is already installed and up-to-date.
Warning: node 25.2.0 is already installed and up-to-date.
Warning: ffmpeg 8.0_2 is already installed and up-to-date.
==> Downloading python@3.11...
```

**With checking:**
```
✓ Already installed: python@3.11
✓ Already installed: node
✓ Already installed: ffmpeg
Installing new-package...
✓ Installed: new-package
```

## Color Standards

Use consistent colors for status messages:

```bash
RED='\033[0;31m'      # Errors, critical warnings
GREEN='\033[0;32m'    # Success, already installed
YELLOW='\033[1;33m'   # Installing, warnings
BLUE='\033[0;34m'     # Section headers, info
NC='\033[0m'          # No Color (reset)
```

## Script Headers

All scripts should have clear headers:

```bash
#!/bin/bash
#
# Script Name
# Brief description of what it does
#
# Features:
# - Smart dependency checking
# - Safe to run multiple times
# - Clear status messages
#
# Usage: ./script_name.sh [options]
```

## Error Handling

```bash
set -e  # Exit on error (unless handled)

# For non-critical commands
command_that_might_fail || true

# For critical checks
if ! critical_check; then
    echo -e "${RED}Error: Critical requirement not met${NC}"
    exit 1
fi
```

**Remember:** Every installation script should be idempotent - running it multiple times should give the same result without breaking anything!

---

## Git Shortcuts for Development

Quick commands to make git operations easier!

### Simple Scripts

**./sync**
Pull latest changes from current branch
```bash
./sync
```

**./push-now**
Push current branch to remote
```bash
./push-now
```

**./quick-commit**
Add all changes, commit, and push in one command
```bash
# With message as argument
./quick-commit "Add new feature"

# Or run without argument to be prompted for message
./quick-commit
```

### Git Aliases (Optional Setup)

To make branch operations even easier, add these aliases to your git config:

```bash
# Set up aliases (run these once)
git config alias.sync '!git fetch origin $(git branch --show-current) && git pull origin $(git branch --show-current)'
git config alias.pushnow '!git push -u origin $(git branch --show-current)'
git config alias.qc '!f() { git add . && git commit -m "$1" && git push -u origin $(git branch --show-current); }; f'
```

Then you can use:
```bash
git sync       # Instead of ./sync
git pushnow    # Instead of ./push-now
git qc "msg"   # Instead of ./quick-commit "msg"
```

### About Long Branch Names

Branch names like `claude/add-gui-layer-011CV5SgRJgCFHwu7JhDMD59` are long but required:

- Must start with `claude/`
- Must end with session ID for security
- Cannot be shortened without breaking push permissions

**Good news:** With these scripts, you rarely need to type it!

### Quick Reference

| Command | What it does |
|---------|-------------|
| `./sync` | Pull latest changes |
| `./push-now` | Push your commits |
| `./quick-commit "msg"` | Add all + commit + push |
| `git status` | See what changed |
| `git log --oneline -5` | See recent commits |
