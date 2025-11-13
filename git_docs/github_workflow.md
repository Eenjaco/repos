# GitHub Workflow - Individual Repository Management

**Last Updated:** 2025-11-12
**Status:** Active
**Purpose:** Complete workflow for managing individual GitHub repositories

---

## 🎯 Core Principles

### 1. Repos are Production-Ready ONLY
**All repositories in `/Projects/repos/` must be clean, distributable, and contain NO personal data.**

This means:
- ✅ Source code, documentation, configuration
- ✅ Sample/demo files (generic, non-personal)
- ✅ Tests with synthetic data
- ❌ Personal audio files, PDFs, transcriptions
- ❌ Session notes, planning docs with personal info
- ❌ Test files with real user data
- ❌ Virtual environments (venv/, node_modules/)
- ❌ Output directories with personal content

**Think:** "Could someone clone this repo and use it immediately without seeing my personal data?"

### 2. Development Happens in Projects/
Work on projects in `/Projects/[project_name]/` with all your personal test files, then copy only production files to repos when ready to commit.

### 3. Two-Folder System

```
Projects/
├── my_project/                    # Development workspace (NOT git tracked)
│   ├── Source code (working copies)
│   ├── test/                      # Personal test files
│   ├── transcriptions/            # Personal outputs
│   ├── venv/                      # Virtual environment
│   ├── Session notes
│   └── Planning docs
│
└── repos/
    └── my-project/                # Public repository (git tracked)
        ├── Source code (clean)
        ├── README.md
        ├── .gitignore
        └── Sample data (generic only)
```

### 4. Clean Commit History
Meaningful commits with clear messages. Track all changes via git.

### 5. Regular Pushes
Push to GitHub at end of each work session (or major milestone).

---

## 📁 Directory Structure

```
/Users/mac/Documents/Local Vault/
├── Projects/
│   ├── mp3_txt/                     # Development: tests, personal transcripts
│   ├── file_renaming/               # Development: personal files to rename
│   └── repos/                       # Git repositories (clean, public)
│       ├── mp3_txt/                 # ← Clean git repo (no personal data)
│       ├── sanzo_wada/              # ← Clean git repo
│       ├── [new-project]/           # ← Future projects
│       ├── GITHUB-WORKFLOW.md       # This file
│       ├── REPO-NAMING.md           # Naming conventions
│       └── REPO-CLEAN-POLICY.md     # Cleanliness guidelines
```

---

## 🧹 Repository Cleanliness Policy

### What to INCLUDE in repos/

**Source Code:**
- Main scripts/executables
- Core libraries and modules
- Helper utilities
- Configuration templates (not filled with personal data)

**Documentation:**
- README.md (usage guide)
- PROJECT-OVERVIEW.md (technical specs)
- ADVANCED.md (optional advanced features)
- CODE_OF_CONDUCT.md, CONTRIBUTING.md (if open source)

**Configuration:**
- .gitignore (properly configured)
- requirements.txt / package.json / Gemfile
- Makefile / build scripts
- Sample config files (config.sample.json)

**Tests:**
- Test scripts
- Sample/synthetic test data
- Test fixtures (generic)

### What to EXCLUDE from repos/

**Personal Data:**
- Personal audio files, PDFs, documents
- Real transcriptions or outputs
- Session notes with personal info
- TODO lists with sensitive tasks

**Development Artifacts:**
- Virtual environments (venv/, env/, node_modules/)
- Python cache (__pycache__/, *.pyc)
- IDE files (.vscode/, .idea/, *.swp)
- OS files (.DS_Store, Thumbs.db)

**Output Directories:**
- transcriptions/
- test_output/
- output/
- build/ (unless distributing binaries)

**Large Files:**
- Downloaded models (vosk models, ML weights)
- Large datasets
- Binary dependencies

**Work-in-Progress:**
- Experimental branches not ready for public
- Draft documentation
- Planning documents

### Example: mp3_txt Repository

**Development folder** (`/Projects/mp3_txt/`):
```
mp3_txt/                           # NOT git tracked
├── transcribe                     # Working copy
├── transcribe_vosk_stream.py      # Working copy
├── test/                          # Personal audiobook files ❌
│   ├── chapter_001.mp3
│   └── chapter_002.mp3
├── transcriptions/                # Personal transcripts ❌
│   ├── sermon_nov_10.md
│   └── audiobook_ch1.md
├── venv/                          # Virtual environment ❌
├── SESSION-SUMMARY-2025-11-12.md  # Work notes ❌
└── Planning docs                  # Personal plans ❌
```

**Public repository** (`/Projects/repos/mp3_txt/`):
```
mp3_txt/                           # Git tracked
├── .git/                          # Git repository ✅
├── .gitignore                     # Excludes personal data ✅
├── README.md                      # User guide ✅
├── PROJECT-OVERVIEW.md            # Technical specs ✅
├── ADVANCED.md                    # Advanced features ✅
├── requirements.txt               # Dependencies ✅
├── transcribe                     # Main CLI ✅
├── transcribe_vosk_stream.py      # Core engine ✅
└── test_debug.py                  # Debug tool ✅
```

**Notice:**
- No test audio files
- No personal transcriptions
- No session notes
- No virtual environment
- No output directories
- Clean, ready to distribute

---

## 🔄 Daily Workflow

### Morning (5 minutes)

**1. Check Repository Status**
```bash
cd "/Users/mac/Documents/Local Vault/Projects/repos"

# Check all repos
for repo in */; do
    if [ -d "$repo/.git" ]; then
        echo "=== $repo ==="
        cd "$repo"
        git status --short
        cd ..
    fi
done
```

**2. Pull Latest Changes** (if collaborating or working from multiple machines)
```bash
cd my-project
git pull
```

**3. Set Session Goal**
Write down ONE primary goal for today.

---

### During Work Session

**Pattern: Develop → Test → Copy → Commit**

**1. Work in Development Folder**
```bash
# Do your work in the development project folder
cd "/Users/mac/Documents/Local Vault/Projects/mp3_txt"

# Edit, test with personal files
./transcribe
# Test with personal audio, create personal transcripts
```

**2. Verify with Personal Data**
```bash
# Test thoroughly with real use cases
./transcribe
# Drag-drop your personal audio files
# Verify transcriptions are accurate
```

**3. Copy ONLY Production Files to Repo**
```bash
# Copy only the source code, no personal data
cp transcribe "/Users/mac/Documents/Local Vault/Projects/repos/mp3_txt/"
cp transcribe_vosk_stream.py "/Users/mac/Documents/Local Vault/Projects/repos/mp3_txt/"
cp README.md "/Users/mac/Documents/Local Vault/Projects/repos/mp3_txt/"

# Do NOT copy:
# - test/ folder with personal audio
# - transcriptions/ with personal outputs
# - venv/ virtual environment
# - Session notes
```

**4. Test in Repo (Final Check)**
```bash
cd "/Users/mac/Documents/Local Vault/Projects/repos/mp3_txt"

# Quick sanity check (no personal data)
python3 transcribe_vosk_stream.py --help
```

**5. Verify Repo Cleanliness**
```bash
# Check for accidentally added personal files
git status

# Verify .gitignore is working
ls -la  # Should NOT see venv/, test/, transcriptions/
```

**6. Commit Changes**
```bash
git add transcribe transcribe_vosk_stream.py README.md
git commit -m "feat: add post-transcription renaming workflow

- Users can rename outputs with custom prefixes
- Auto-move files to different folders (e.g., Inbox)
- Improved UX with colored prompts

Tested with audiobook chapters and sermon audio.

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### End of Session (10-15 minutes)

**1. Review Changes**
```bash
cd "/Users/mac/Documents/Local Vault/Projects/repos/mp3_txt"

git status
git log --oneline -5  # Last 5 commits
```

**2. Double-Check for Personal Data**
```bash
# Look for common personal data patterns
git diff --cached | grep -i "personal\|private\|secret"

# Check file sizes (large files might be personal audio/PDFs)
git diff --cached --stat
```

**3. Push to GitHub**
```bash
git push origin main
```

**4. Update Session Notes** (in development folder, NOT repo)
```bash
# In /Projects/mp3_txt/, not /Projects/repos/mp3_txt/
echo "## Session 2025-11-12
✅ Added rename workflow
✅ Tested with personal audiobook
✅ Committed clean version to repo
" >> SESSION-NOTES.md
```

---

## 🚀 Creating a New Project/Repo

### Step 1: Develop in Projects/ (with personal data)

```bash
# Create development folder
mkdir "/Users/mac/Documents/Local Vault/Projects/my_new_tool"
cd "/Users/mac/Documents/Local Vault/Projects/my_new_tool"

# Develop with real use cases
# - Use personal test files
# - Create outputs with real data
# - Take session notes
# - Everything stays here, NOT in git

# ... write code, test extensively ...
```

### Step 2: Prepare Clean Version for Repo

**Create .gitignore in development folder** (as reference):
```bash
cat > .gitignore <<'EOF'
# Personal data
test/
test_output/
transcriptions/
personal_files/
*.mp3
*.pdf
*.wav

# Development
venv/
env/
__pycache__/
*.pyc
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Session notes
SESSION-*.md
NOTES.md
TODO.md
EOF
```

### Step 3: Create Clean Repo

```bash
# Create repo folder
mkdir "/Users/mac/Documents/Local Vault/Projects/repos/my-new-tool"
cd "/Users/mac/Documents/Local Vault/Projects/repos/my-new-tool"

# Copy ONLY production files (no personal data)
cp "../../../my_new_tool/main-script" .
cp "../../../my_new_tool/helper-script" .
cp "../../../my_new_tool/requirements.txt" .

# Copy .gitignore (for users who clone)
cp "../../../my_new_tool/.gitignore" .

# Create README (no personal examples)
cat > README.md <<'EOF'
# My New Tool

Description of what it does.

## Installation

\`\`\`bash
pip install -r requirements.txt
chmod +x main-script
\`\`\`

## Usage

\`\`\`bash
# Example with generic data
./main-script sample.txt
\`\`\`

## Requirements

- Python 3.10+
- Dependencies listed in requirements.txt
EOF
```

### Step 4: Initialize Git (Clean Repo)

```bash
# Initialize git in repos folder
git init

# Stage only production files
git add main-script helper-script requirements.txt .gitignore README.md

# Verify no personal data
git status  # Check what's staged
ls -la      # Verify no personal folders

# Create initial commit
git commit -m "feat: initial commit - my new tool

Description of what the tool does and key features.

Technical details:
- Language/framework
- Key dependencies
- Platform compatibility

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Step 5: Push to GitHub

```bash
# Create GitHub repo and push
gh repo create my-new-tool --private --source=. --remote=origin --push

# Or if repo already exists
git remote add origin git@github.com:username/my-new-tool.git
git push -u origin main
```

### Step 6: Create Development README

```bash
# Back in development folder, document the separation
cd "/Users/mac/Documents/Local Vault/Projects/my_new_tool"

cat > DEV-README.md <<'EOF'
# Development Folder

**This is NOT the git repository.**

## Structure

- `/Projects/my_new_tool/` - This folder (development, personal data)
- `/Projects/repos/my-new-tool/` - Public git repository (clean)

## Workflow

1. Work here with personal test files
2. Test thoroughly
3. Copy only production files to repos/
4. Commit from repos/ folder
5. Keep personal data here, never in git

## Syncing

\`\`\`bash
# After making changes, copy to repos
cp main-script /path/to/repos/my-new-tool/
cd /path/to/repos/my-new-tool/
git add main-script
git commit -m "update: description"
git push
\`\`\`
EOF
```

---

## 🔄 Syncing Development and Repo

### Active Development Pattern

**While actively developing:**
1. Work in `/Projects/[project_name]/`
2. Test with personal files
3. Take notes, create outputs
4. When feature complete, copy ONLY source to `repos/project/`
5. Verify cleanliness, commit, push

**Why:** Keeps repo clean, only commits working code, no personal data leaks.

### Quick Fixes Pattern

**For small fixes in existing features:**
1. Edit directly in `repos/project/` (if no personal data needed for testing)
2. Test with generic data or existing tests
3. Commit immediately
4. Optionally copy back to `/Projects/[project_name]/`

**Why:** Faster for small changes that don't need personal test data.

### Sync Script Example

```bash
#!/usr/bin/env bash
# sync-to-repo.sh
# Sync production files from development to repo

DEV_DIR="/Users/mac/Documents/Local Vault/Projects/my_tool"
REPO_DIR="/Users/mac/Documents/Local Vault/Projects/repos/my-tool"

# Copy only production files
cp "$DEV_DIR/main-script" "$REPO_DIR/"
cp "$DEV_DIR/helper" "$REPO_DIR/"
cp "$DEV_DIR/README.md" "$REPO_DIR/"
cp "$DEV_DIR/requirements.txt" "$REPO_DIR/"

echo "✅ Synced production files to repo"
echo "Next: cd $REPO_DIR && git status"
```

---

## 📋 Pre-Commit Checklist

Before every commit, verify:

- [ ] No personal data in staged files
- [ ] No test files with real user data
- [ ] No session notes or TODOs
- [ ] No virtual environments
- [ ] No output directories with personal content
- [ ] .gitignore properly configured
- [ ] README has generic examples only
- [ ] All file paths are relative, not absolute personal paths
- [ ] No API keys, passwords, or credentials
- [ ] File sizes reasonable (no large personal audio/PDF files)

**Quick check:**
```bash
# See what's staged
git diff --cached --stat

# Look for common personal data markers
git diff --cached | grep -i "personal\|/Users/mac\|secret\|password"

# Check for large files
git diff --cached --stat | awk '{if ($1 > 1000000) print $0}'
```

---

## 💡 Best Practices

### Commit Often (in repos/, not development)

- Small, focused commits
- Only working, tested code
- No personal data
- Clear messages

### Keep Development and Repo Separate

**Development folder:**
- Personal test files
- Real-world use cases
- Session notes
- Work-in-progress
- NOT git tracked

**Repo folder:**
- Production code only
- Generic examples
- Complete documentation
- Git tracked
- Ready to share

### Use .gitignore Aggressively

```
# Personal data patterns
test/
test_output/
transcriptions/
personal*/
*_personal.*

# Development
venv/
*.pyc
.vscode/

# OS
.DS_Store

# Session work
SESSION-*.md
TODO*.md
NOTES.md

# Output
output/
build/ (unless distributing)
```

### Test in Clean Repo Before Push

```bash
cd repos/my-project

# Can someone else clone and use this?
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
./my-script --help  # Should work without personal data
```

---

## 🚨 Troubleshooting

### "Accidentally Committed Personal Data"

**If not yet pushed:**
```bash
# Remove from last commit
git reset HEAD~1

# Remove the personal file
rm personal-file.txt

# Re-commit without it
git add .
git commit -m "..."
```

**If already pushed:**
```bash
# Remove file from git history (CAREFUL)
git filter-branch --tree-filter 'rm -f personal-file.txt' HEAD

# Force push (if repo is only yours)
git push --force

# Or contact GitHub support to purge sensitive data
```

### "Repo Contains venv/ or __pycache__/"

```bash
# Remove from tracking
git rm -r --cached venv __pycache__

# Add to .gitignore
echo "venv/" >> .gitignore
echo "__pycache__/" >> .gitignore

# Commit
git add .gitignore
git commit -m "chore: remove venv and cache from tracking"
```

### "Test Folder Was Committed with Personal Audio"

```bash
# Remove from git but keep in development folder
git rm -r --cached test/

# Add to .gitignore
echo "test/" >> .gitignore

# Commit removal
git add .gitignore
git commit -m "chore: remove personal test files"

# Force push to clean remote
git push --force  # Only if you own the repo
```

---

## 📚 Quick Reference

### Daily Commands

```bash
# Start session (development)
cd Projects/my_tool
# Work with personal files

# Sync to repo
cp script repos/my-tool/
cd repos/my-tool

# Verify clean
git status
ls -la  # No venv/, test/, personal folders

# Commit
git add script
git commit -m "type: message"
git push
```

### Pre-Commit Check

```bash
# What's staged?
git diff --cached --stat

# Any personal data?
git diff --cached | grep -i personal

# Large files?
git diff --cached --stat | awk '{if ($1 > 100000) print}'
```

### Repository Health Check

```bash
# Check all repos for cleanliness
for repo in repos/*/; do
    cd "$repo"
    echo "=== $(basename $repo) ==="

    # Check for common personal data folders
    ls | grep -E "test|personal|output|venv" || echo "  Clean ✅"

    # Check .gitignore exists
    [ -f .gitignore ] && echo "  .gitignore ✅" || echo "  Missing .gitignore ❌"

    cd -
done
```

---

## 🔗 Related Docs

- `REPO-NAMING.md` - Naming conventions for repos
- `REPO-CLEAN-POLICY.md` - Detailed cleanliness guidelines
- `SESSION-TEMPLATE.md` - Daily session notes template (for development folder, not repo)

---

## 📝 Archive

**Previous version:** `/Archive/github-workflow-2025-11-12/GITHUB-WORKFLOW.md`

**What changed (2025-11-12):**
- Added "Repos are Production-Ready ONLY" policy
- Added Repository Cleanliness Policy section
- Updated "Creating a New Project/Repo" with two-folder system
- Added pre-commit checklist
- Added examples from mp3_txt project
- Emphasized separation of development (personal data) from repos (clean, public)

---

**Remember:**

> **Repos = Public = No Personal Data**
>
> **Development = Private = All Personal Data**
>
> Always ask: "Could I share this repo right now without exposing personal information?"

**Next Review:** 2025-12-12
