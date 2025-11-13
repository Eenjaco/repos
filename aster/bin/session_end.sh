#!/usr/bin/env bash
# Session end script with AI-generated commit message
# Works in any terminal, no Claude Code needed

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}📊 Session End${NC}"
echo ""

# Navigate to git root
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Not in a git repository"
    exit 1
fi

cd $(git rev-parse --show-toplevel)

# Check if there are changes
if [[ -z $(git status -s) ]]; then
    echo -e "${GREEN}✅ No changes to commit${NC}"
    echo ""
    git log --oneline -5
    exit 0
fi

echo -e "${YELLOW}📝 Analyzing changes...${NC}"
echo ""

# Get git status and diff
GIT_STATUS=$(git status --short)
GIT_DIFF=$(git diff --stat)
GIT_DIFF_FULL=$(git diff)

# Show what changed
echo "Changes detected:"
echo "$GIT_STATUS"
echo ""

# Generate commit message with Ollama
echo -e "${YELLOW}🤖 Generating commit message with llama3.2:1b...${NC}"

PROMPT="You are a git commit message generator. Based on these changes, write a concise commit message (1 line summary + optional bullet points).

Git status:
$GIT_STATUS

Git diff stat:
$GIT_DIFF

Rules:
- First line: imperative mood, <50 chars (e.g., 'Add feature' not 'Added feature')
- Be specific about what changed
- If multiple changes, add bullet points
- No fluff or unnecessary words

Example format:
Add audio transcription pipeline

- Implement Vosk integration
- Add chunking for large files
- Create parallel processing

Now generate a commit message:"

COMMIT_MSG=$(echo "$PROMPT" | ollama run llama3.2:1b 2>/dev/null | head -20)

echo ""
echo -e "${GREEN}Generated commit message:${NC}"
echo "---"
echo "$COMMIT_MSG"
echo "---"
echo ""

# Ask for confirmation
read -p "Use this message? [Y/n/e(dit)] " -n 1 -r
echo
if [[ $REPLY =~ ^[Nn]$ ]]; then
    echo "Commit cancelled"
    exit 1
elif [[ $REPLY =~ ^[Ee]$ ]]; then
    # Open editor for manual edit
    echo "$COMMIT_MSG" > /tmp/commit_msg.txt
    ${EDITOR:-nano} /tmp/commit_msg.txt
    COMMIT_MSG=$(cat /tmp/commit_msg.txt)
    rm /tmp/commit_msg.txt
fi

# Stage all changes
git add -A

# Commit with generated message
git commit -m "$COMMIT_MSG"

echo ""
echo -e "${GREEN}✅ Committed${NC}"
echo ""

# Push to remote
read -p "Push to remote? [Y/n] " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    BRANCH=$(git branch --show-current)
    git push -u origin "$BRANCH"
    echo ""
    echo -e "${GREEN}✅ Pushed to origin/$BRANCH${NC}"
fi

echo ""
echo -e "${BLUE}📋 Recent commits:${NC}"
git log --oneline -5

echo ""
echo -e "${GREEN}✨ Session closed!${NC}"
