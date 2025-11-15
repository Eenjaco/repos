#!/bin/bash
#
# Time Tracker Aliases for .zshrc
# Copy these lines to your ~/.zshrc file
#
# Usage:
#   cat ALIASES_ZSHRC.sh >> ~/.zshrc
#   source ~/.zshrc

cat << 'EOF'

# ═══════════════════════════════════════════════════════════
# Time Tracker Aliases
# ═══════════════════════════════════════════════════════════
export TT_HOME="/Users/mac/Documents/Applications/tt_standalone"

# Main tt command - works from anywhere
tt() {
    (cd "$TT_HOME" && source venv/bin/activate && ./tt "$@")
}

# Quick shortcuts
alias ttb='(cd "$TT_HOME" && source venv/bin/activate && ./tt s)'
alias tte='(cd "$TT_HOME" && source venv/bin/activate && ./tt e)'
alias ttcd='cd "$TT_HOME"'
alias ttwatch='(cd "$TT_HOME" && source venv/bin/activate && python3 watch_obsidian_timer.py)'
alias ttsync='(cd "$TT_HOME" && ./sync)'
alias ttarchive='(cd "$TT_HOME" && ./weekly_archive.sh)'

# Git shortcuts (when in tt directory)
alias ttpush='(cd "$TT_HOME" && ./push-now)'
alias ttcommit='(cd "$TT_HOME" && ./quick-commit)'

EOF
