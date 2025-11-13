#!/usr/bin/env bash
# Session start script with AI-generated summary
# Works in any terminal, no Claude Code needed

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Session Start${NC}"
echo ""

# Navigate to git root
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Not in a git repository"
    exit 1
fi

cd $(git rev-parse --show-toplevel)

# Get repo info
REPO_NAME=$(basename $(pwd))
BRANCH=$(git branch --show-current)

echo -e "${CYAN}📁 Repository: ${REPO_NAME}${NC}"
echo -e "${CYAN}🌿 Branch: ${BRANCH}${NC}"
echo ""

# Check if up to date with remote
echo -e "${YELLOW}📡 Checking remote...${NC}"
git fetch --quiet 2>/dev/null || true

if git status | grep -q "Your branch is behind"; then
    echo -e "${YELLOW}⚠️  Your branch is behind remote${NC}"
    read -p "Pull latest changes? [Y/n] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        git pull
        echo ""
    fi
fi

# Get recent commits
RECENT_COMMITS=$(git log --oneline -10)

# Get recent commit messages for context
COMMIT_SUMMARY=$(git log --pretty=format:"%s" -10)

echo -e "${BLUE}📝 Recent Activity${NC}"
echo ""
echo "$RECENT_COMMITS"
echo ""

# Generate session briefing with Ollama
echo -e "${YELLOW}🤖 Generating session briefing with llama3.2:1b...${NC}"

PROMPT="You are a code session assistant. Summarize recent work and suggest next steps.

Repository: $REPO_NAME
Branch: $BRANCH

Recent commits:
$COMMIT_SUMMARY

Task:
1. Summarize what was accomplished recently (2-3 bullet points)
2. Suggest 2-3 logical next steps
3. Keep it concise and actionable

Format:
## Recent Work
- Point 1
- Point 2

## Suggested Next Steps
1. First priority
2. Second priority

Now generate the briefing:"

BRIEFING=$(echo "$PROMPT" | ollama run llama3.2:1b 2>/dev/null | head -25)

echo ""
echo -e "${GREEN}${BRIEFING}${NC}"
echo ""

# Check for uncommitted changes
if [[ -n $(git status -s) ]]; then
    echo -e "${YELLOW}⚠️  Uncommitted changes:${NC}"
    git status --short
    echo ""
fi

# Check for SESSION_NOTES.md
if [[ -f SESSION_NOTES.md ]]; then
    echo -e "${CYAN}📋 Session notes found (SESSION_NOTES.md)${NC}"
    if grep -q "Pending Ideas" SESSION_NOTES.md 2>/dev/null; then
        echo ""
        echo -e "${YELLOW}⏳ Pending from last session:${NC}"
        sed -n '/## ⏳ Pending Ideas/,/^## /p' SESSION_NOTES.md | grep "^###" | sed 's/^### /  • /'
        echo ""
    fi
fi

echo -e "${GREEN}✨ Ready to work!${NC}"
