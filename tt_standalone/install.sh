#!/bin/bash
#
# Time Tracker Installation Script
# Checks for existing installations before installing
#
# Features:
# - Smart dependency checking
# - Safe to run multiple times
# - Clear status messages
#
# Usage: ./install.sh

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
else
    OS="unknown"
fi

echo -e "${BLUE}==================================${NC}"
echo -e "${BLUE}Time Tracker Installation${NC}"
echo -e "${BLUE}==================================${NC}"
echo -e "OS: $OS\n"

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
            pip3 install "$package"
        fi
    done
}

# Check if npm package installed globally
npm_installed_global() {
    npm list -g "$1" &>/dev/null
}

# Check if npm package installed locally
npm_installed_local() {
    npm list "$1" &>/dev/null
}

# ============================================
# 1. Check Package Managers
# ============================================

echo -e "${BLUE}[1] Checking Package Managers${NC}"

if [[ "$OS" == "macos" ]]; then
    if ! command_exists brew; then
        echo -e "${YELLOW}Installing Homebrew...${NC}"
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    else
        echo -e "${GREEN}✓${NC} Homebrew installed"
    fi
fi

# ============================================
# 2. Check System Dependencies
# ============================================

echo -e "\n${BLUE}[2] Checking System Dependencies${NC}"

# Python
if ! command_exists python3; then
    echo -e "${YELLOW}Installing Python 3...${NC}"
    if [[ "$OS" == "macos" ]]; then
        brew_install_if_missing python@3.11
    elif [[ "$OS" == "linux" ]]; then
        sudo apt-get update && sudo apt-get install -y python3 python3-pip
    fi
else
    echo -e "${GREEN}✓${NC} Python 3 installed ($(python3 --version))"
fi

# Node.js
if ! command_exists node; then
    echo -e "${YELLOW}Installing Node.js...${NC}"
    if [[ "$OS" == "macos" ]]; then
        brew_install_if_missing node
    elif [[ "$OS" == "linux" ]]; then
        curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
        sudo apt-get install -y nodejs
    fi
else
    echo -e "${GREEN}✓${NC} Node.js installed ($(node --version))"
fi

# Git
if ! command_exists git; then
    echo -e "${YELLOW}Installing Git...${NC}"
    if [[ "$OS" == "macos" ]]; then
        brew_install_if_missing git
    elif [[ "$OS" == "linux" ]]; then
        sudo apt-get install -y git
    fi
else
    echo -e "${GREEN}✓${NC} Git installed ($(git --version))"
fi

# ============================================
# 3. Check Python Packages
# ============================================

echo -e "\n${BLUE}[3] Checking Python Packages${NC}"

# Watchdog (for file watching)
pip_install_if_missing watchdog

# Optional: Check for user-mentioned packages (informational only)
if pip_installed vosk; then
    echo -e "${GREEN}✓${NC} Vosk already installed (no action needed)"
fi

if pip_installed openai-whisper; then
    echo -e "${GREEN}✓${NC} Whisper already installed (no action needed)"
fi

# ============================================
# 4. Check Node.js Dependencies
# ============================================

echo -e "\n${BLUE}[4] Checking Node.js Dependencies${NC}"

if [ -f "package.json" ]; then
    if [ -d "node_modules" ]; then
        echo -e "${GREEN}✓${NC} Node modules already installed"
        echo -e "${YELLOW}Running npm install to verify...${NC}"
        npm install --silent
    else
        echo -e "${YELLOW}Installing Node.js dependencies...${NC}"
        npm install
    fi
else
    echo -e "${RED}Error: package.json not found${NC}"
    exit 1
fi

# Check critical packages
if npm_installed_local better-sqlite3; then
    echo -e "${GREEN}✓${NC} better-sqlite3 installed"
else
    echo -e "${RED}Error: better-sqlite3 not installed${NC}"
    exit 1
fi

# ============================================
# 5. Check Database
# ============================================

echo -e "\n${BLUE}[5] Checking Database${NC}"

if [ -f "timetracking.db" ]; then
    echo -e "${GREEN}✓${NC} Database exists ($(du -h timetracking.db | cut -f1))"

    # Verify database integrity
    if command_exists sqlite3; then
        if sqlite3 timetracking.db "SELECT COUNT(*) FROM time_entries;" &>/dev/null; then
            ENTRY_COUNT=$(sqlite3 timetracking.db "SELECT COUNT(*) FROM time_entries;")
            echo -e "${GREEN}✓${NC} Database verified ($ENTRY_COUNT entries)"
        else
            echo -e "${RED}Warning: Database exists but may be corrupted${NC}"
        fi
    fi
else
    echo -e "${YELLOW}Warning: Database not found${NC}"
    echo -e "  Database will be created on first run of ./tt"
fi

# ============================================
# 6. Check Scripts Permissions
# ============================================

echo -e "\n${BLUE}[6] Checking Script Permissions${NC}"

SCRIPTS=(
    "tt"
    "tt_local"
    "tt_local_shortcuts"
    "append_to_markdown.sh"
    "backup.sh"
    "watch_markdown.py"
    "sync"
    "push-now"
    "quick-commit"
)

for script in "${SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        if [ -x "$script" ]; then
            echo -e "${GREEN}✓${NC} $script is executable"
        else
            echo -e "${YELLOW}Making $script executable...${NC}"
            chmod +x "$script"
        fi
    else
        echo -e "${YELLOW}Warning: $script not found${NC}"
    fi
done

# ============================================
# 7. Check Directories
# ============================================

echo -e "\n${BLUE}[7] Checking Directories${NC}"

DIRS=(
    "time_logs"
    "backups"
    "obsidian_templates"
)

for dir in "${DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✓${NC} Directory exists: $dir"
    else
        echo -e "${YELLOW}Creating directory: $dir${NC}"
        mkdir -p "$dir"
    fi
done

# ============================================
# 8. Optional: Create Virtual Environment
# ============================================

echo -e "\n${BLUE}[8] Python Virtual Environment (Optional)${NC}"

if [ -d "venv" ]; then
    echo -e "${GREEN}✓${NC} Virtual environment exists"
else
    read -p "Create Python virtual environment? [y/N] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Creating virtual environment...${NC}"
        python3 -m venv venv
        echo -e "${GREEN}✓${NC} Virtual environment created"
        echo -e "${BLUE}Activate with: source venv/bin/activate${NC}"

        # Install packages in venv
        source venv/bin/activate
        pip install --upgrade pip
        pip_install_if_missing watchdog
        deactivate
    fi
fi

# ============================================
# Installation Complete
# ============================================

echo -e "\n${BLUE}==================================${NC}"
echo -e "${GREEN}✓ Installation Complete!${NC}"
echo -e "${BLUE}==================================${NC}"

echo -e "\n${BLUE}Quick Start:${NC}"
echo -e "  ${GREEN}./tt${NC}              Show weekly progress"
echo -e "  ${GREEN}./tt s${NC}            Start timer"
echo -e "  ${GREEN}./tt e${NC}            End timer"
echo -e "  ${GREEN}./tt --help${NC}       Show all commands"

echo -e "\n${BLUE}Markdown Watcher:${NC}"
echo -e "  ${GREEN}python3 watch_markdown.py${NC}    Start file watcher"

echo -e "\n${BLUE}Git Shortcuts:${NC}"
echo -e "  ${GREEN}./sync${NC}            Pull latest changes"
echo -e "  ${GREEN}./push-now${NC}        Push to remote"
echo -e "  ${GREEN}./quick-commit \"msg\"${NC}  Add, commit, and push"

echo -e "\n${BLUE}Next Steps:${NC}"
echo -e "  1. Read ${GREEN}README.md${NC} for full documentation"
echo -e "  2. Read ${GREEN}SETUP_TERMINAL.md${NC} for terminal setup"
echo -e "  3. Read ${GREEN}obsidian_templates/SHORTCUTS_OBSIDIAN_SETUP.md${NC} for mobile setup"
echo -e "  4. Run ${GREEN}./tt${NC} to test the CLI"

echo ""
