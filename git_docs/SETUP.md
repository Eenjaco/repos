# GitHub Repository Setup Guide

**Last Updated:** 2025-11-12
**Status:** Active
**Purpose:** Complete guide for setting up new GitHub repositories with clean, production-ready code

---

## 🎯 Core Philosophy

**Every project has TWO locations:**
1. **Development Folder** - `/Projects/my_project/` (personal data, tests, work-in-progress)
2. **Repository Folder** - `/Projects/repos/my-project/` (clean, public, git-tracked)

**Repositories must be production-ready from day one. No personal data, ever.**

---

## 📁 Directory Structure

```
/Users/mac/Documents/Local Vault/
├── Projects/
│   ├── my_project/                # Development workspace (NOT git)
│   │   ├── Source code (working)
│   │   ├── test/                  # Personal test files
│   │   ├── output/                # Personal outputs
│   │   ├── venv/                  # Virtual environment
│   │   ├── SESSION-*.md           # Session notes
│   │   └── DEV-README.md          # Development notes
│   │
│   └── repos/                     # All git repositories (git tracked)
│       ├── my-project/            # ← Clean, public repository
│       │   ├── .git/
│       │   ├── .gitignore         # Excludes personal data
│       │   ├── README.md
│       │   └── Source code (clean)
│       ├── other-project/
│       ├── GITHUB-WORKFLOW.md     # Workflow guide
│       ├── REPO-NAMING.md         # Naming conventions
│       ├── SESSION-TEMPLATE.md    # Session notes template
│       └── SETUP.md               # This file
```

---

## 🚀 Creating a New Project

Follow these steps for **every new project**.

### Phase 1: Development

**1. Create Development Folder**

```bash
mkdir -p "/Users/mac/Documents/Local Vault/Projects/my_new_project"
cd "/Users/mac/Documents/Local Vault/Projects/my_new_project"
```

**2. Create Project Files**

For a Python project:
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install required-packages

# Create test folder
mkdir -p test
mkdir -p output

# Create main script
touch main_script.py
chmod +x main_script.py
```

For a Bash project:
```bash
# Create main script
touch my-script
chmod +x my-script

# Create test folder
mkdir -p test
mkdir -p test_output
```

**3. Create DEV-README.md**

```bash
cat > DEV-README.md <<'EOF'
# my_new_project - Development Folder

**Location:** `/Users/mac/Documents/Local Vault/Projects/my_new_project/`

This is the **development and testing folder** with personal data, test files, and work-in-progress materials.

## Development vs Repository

**Development folder (this folder):**
- Contains personal test files
- Contains output/results with personal data
- Has virtual environment
- Has session notes and planning docs
- NOT git tracked

**Repository folder:**
- Location: `/Projects/repos/my-new-project/`
- Contains only clean, distributable code
- No personal data
- Git tracked and pushed to GitHub

## Workflow

1. Work in this folder with personal test files
2. Test thoroughly
3. Copy only production files to repos/
4. Commit from repos/ folder
5. Keep personal data here, never in git

## Files to Copy to Repo

When ready to commit:
```bash
cp my-script /Users/mac/Documents/Local\ Vault/Projects/repos/my-new-project/
cp README.md /Users/mac/Documents/Local\ Vault/Projects/repos/my-new-project/
cp requirements.txt /Users/mac/Documents/Local\ Vault/Projects/repos/my-new-project/
```

**Created:** $(date +%Y-%m-%d)
EOF
```

**4. Develop and Test**

```bash
# Work on your project with personal test files
./my-script test/my-personal-file.mp3

# Iterate until it works perfectly
# Keep all session notes in SESSION-*.md files here
```

---

### Phase 2: Prepare Clean Repository

**5. Create Repository Folder**

```bash
mkdir -p "/Users/mac/Documents/Local Vault/Projects/repos/my-new-project"
cd "/Users/mac/Documents/Local Vault/Projects/repos/my-new-project"
```

**6. Copy ONLY Production Files**

**Copy source code:**
```bash
# From development folder to repository
cp "/Users/mac/Documents/Local Vault/Projects/my_new_project/my-script" .
cp "/Users/mac/Documents/Local Vault/Projects/my_new_project/main.py" .
```

**Create requirements.txt (Python projects):**
```bash
# Generate from virtual environment
cd "/Users/mac/Documents/Local Vault/Projects/my_new_project"
source venv/bin/activate
pip freeze > requirements.txt

# Copy to repo
cp requirements.txt "/Users/mac/Documents/Local Vault/Projects/repos/my-new-project/"
```

**7. Create .gitignore**

**CRITICAL:** This prevents personal data from being committed.

```bash
cat > .gitignore <<'EOF'
# Personal data - NEVER COMMIT
test/
test_output/
output/
transcriptions/
results/
*.mp3
*.wav
*.m4a
*.mp4
*.pdf

# Virtual environments
venv/
env/
node_modules/

# Python
__pycache__/
*.pyc
*.pyo
*.egg-info/

# Session work - NEVER COMMIT
SESSION-*.md
NOTES-*.md
TODO-*.md
DEV-README.md

# OS files
.DS_Store
Thumbs.db
._*

# Editor
.vscode/
.idea/
*.swp
*.swo

# Temp files
*.tmp
*.bak
*~
EOF
```

**Customize .gitignore for your project type:**
- Audio/video projects: Add `*.flac`, `*.ogg`, etc.
- PDF processing: Add `*.docx`, `*.epub`, etc.
- Data projects: Add `*.csv`, `*.db`, etc.

**8. Create README.md**

```bash
cat > README.md <<'EOF'
# My New Project

One-line description of what this project does.

## Installation

```bash
# Clone the repository
git clone https://github.com/username/my-new-project.git
cd my-new-project

# Install dependencies (Python)
pip install -r requirements.txt

# Or install dependencies (Node.js)
npm install
```

## Usage

```bash
# Basic usage
./my-script input-file.txt

# Batch mode
./my-script --batch /path/to/folder
```

## Features

- Feature 1
- Feature 2
- Feature 3

## Requirements

- bash 3.2+
- python 3.8+ (or other dependencies)
- ffmpeg (if applicable)

## Options

```
--help          Show help message
--version       Show version
--batch DIR     Process directory
```

## Examples

```bash
# Example 1
./my-script sample.txt

# Example 2
./my-script --batch examples/
```

## License

MIT (or your choice)
EOF
```

**9. Verify Repository Cleanliness**

**Run this checklist:**
```bash
cd "/Users/mac/Documents/Local Vault/Projects/repos/my-new-project"

# List all files
ls -la

# Check for personal data (should find NOTHING)
find . -name "*.mp3" -o -name "*.pdf" -o -name "SESSION-*"

# Verify .gitignore exists
cat .gitignore
```

**Checklist:**
- [ ] No test/ folder with personal files
- [ ] No output/ or transcriptions/ folders
- [ ] No venv/ or node_modules/
- [ ] No SESSION-*.md files
- [ ] No personal audio/video/PDF files
- [ ] .gitignore exists and excludes personal data
- [ ] README has generic examples only
- [ ] All scripts are executable (chmod +x)
- [ ] No hardcoded paths

---

### Phase 3: Initialize Git

**10. Initialize Git Repository**

```bash
cd "/Users/mac/Documents/Local Vault/Projects/repos/my-new-project"

# Initialize git
git init

# Add all files
git add .

# Verify what will be committed
git status

# VERIFY: No personal data in staging area
git diff --cached --name-only
```

**11. Create Initial Commit**

```bash
git commit -m "feat: initial commit - my new project

Description of what the project does and key features.

Features:
- Feature 1
- Feature 2
- Feature 3

Technical:
- Language/framework used
- Key dependencies
- Platform support

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Phase 4: Push to GitHub

**12. Create GitHub Repository**

**Method 1: Using GitHub CLI (recommended)**

```bash
# Create private repository and push
gh repo create my-new-project --private --source=. --remote=origin --push

```

**Method 2: Manual**

```bash
# 1. Create repo on GitHub: https://github.com/new
#    - Name: my-new-project
#    - Private: Yes
#    - Don't initialize with README (we have one)

# 2. Add remote and push
git remote add origin https://github.com/username/my-new-project.git
git branch -M main
git push -u origin main
```

**13. Verify on GitHub**

Open repository in browser:
```bash
gh repo view --web
```

**Verify:**
- [ ] Repository is private (or public if intended)
- [ ] README displays correctly
- [ ] No personal data visible
- [ ] No test/ folder visible
- [ ] No SESSION-*.md files visible
- [ ] .gitignore is working

---

## 🔄 Daily Workflow

### Working on the Project

**1. Develop in development folder:**
```bash
cd "/Users/mac/Documents/Local Vault/Projects/my_new_project"

# Edit code, test with personal files
./my-script test/my-personal-file.mp3

# Keep session notes
echo "## Session $(date +%Y-%m-%d)" >> SESSION-$(date +%Y-%m-%d).md
```

**2. When ready to commit:**
```bash
# Copy updated files to repo
cp my-script /Users/mac/Documents/Local\ Vault/Projects/repos/my-new-project/
cp main.py /Users/mac/Documents/Local\ Vault/Projects/repos/my-new-project/
cp README.md /Users/mac/Documents/Local\ Vault/Projects/repos/my-new-project/
```

**3. Test in repository folder:**
```bash
cd "/Users/mac/Documents/Local Vault/Projects/repos/my-new-project"

# Test with generic file (NOT personal data)
./my-script sample-file.txt

# Verify it works
```

**4. Verify cleanliness:**
```bash
# Check for personal data
git status
git diff

# Verify no personal files
find . -name "*.mp3" -o -name "SESSION-*" -o -name "test/"
```

**5. Commit and push:**
```bash
git add .
git commit -m "feat: add new feature

Description of what changed and why.

Tested with sample files."

git push
```

---

## 📋 Pre-Commit Checklist

**Use this EVERY TIME before committing:**

### Repository Cleanliness
- [ ] No personal audio/video files in repo
- [ ] No personal PDFs or documents
- [ ] No test files with real user data
- [ ] No output directories with personal content (transcriptions/, output/)
- [ ] No virtual environments (venv/, node_modules/)
- [ ] No session notes (SESSION-*.md)
- [ ] No planning docs with personal info
- [ ] No API keys or credentials
- [ ] .gitignore properly configured
- [ ] README has generic examples only

### Code Quality
- [ ] Scripts are executable (chmod +x)
- [ ] No hardcoded absolute paths
- [ ] All file paths are relative
- [ ] Code tested and working
- [ ] No debug print statements

### Documentation
- [ ] README is current
- [ ] Usage examples are accurate
- [ ] Dependencies listed
- [ ] Installation steps clear

**Think:** "Could a stranger clone this and use it without seeing my personal data?"

---

## 🗂️ Managing Multiple Projects

### Quick Status Check

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

### Check for Uncommitted Changes

```bash
cd "/Users/mac/Documents/Local Vault/Projects/repos"

for repo in */; do
    if [ -d "$repo/.git" ]; then
        cd "$repo"
        changes=$(git status --short | wc -l)
        if [ $changes -gt 0 ]; then
            echo "$repo has $changes uncommitted changes"
        fi
        cd ..
    fi
done
```

### Check for Unpushed Commits

```bash
cd "/Users/mac/Documents/Local Vault/Projects/repos"

for repo in */; do
    if [ -d "$repo/.git" ]; then
        cd "$repo"
        unpushed=$(git log --branches --not --remotes --oneline 2>/dev/null | wc -l)
        if [ $unpushed -gt 0 ]; then
            echo "$repo has $unpushed unpushed commits"
        fi
        cd ..
    fi
done
```

---

## 🎨 Example Projects

### Example 1: Python Audio Transcription Tool

**Development folder:**
```
Projects/mp3_txt/
├── transcribe (working)
├── transcribe_vosk_stream.py (working)
├── test/                    # Personal audio files
├── transcriptions/          # Personal outputs
├── venv/                    # Virtual environment
├── SESSION-2025-11-12.md    # Session notes
└── DEV-README.md
```

**Repository (clean):**
```
repos/mp3-txt/
├── .git/
├── .gitignore              # Excludes test/, transcriptions/, *.mp3
├── README.md
├── PROJECT-OVERVIEW.md
├── ADVANCED.md
├── requirements.txt
├── transcribe
└── transcribe_vosk_stream.py
```

**.gitignore for mp3-txt:**
```
# Personal audio
test/
test_output/
transcriptions/
*.mp3
*.wav
*.m4a

# Python
venv/
__pycache__/
*.pyc

# Session work
SESSION-*.md
DEV-README.md

# OS
.DS_Store
```

---

### Example 2: Bash PDF Converter

**Development folder:**
```
Projects/pdf_converter/
├── convert-pdf (working)
├── test/                    # Personal PDFs
├── output/                  # Personal conversions
├── SESSION-2025-11-12.md
└── DEV-README.md
```

**Repository (clean):**
```
repos/pdf-converter/
├── .git/
├── .gitignore              # Excludes test/, output/, *.pdf
├── README.md
├── convert-pdf
└── config-template.json
```

**.gitignore for pdf-converter:**
```
# Personal PDFs
test/
test_pdfs/
output/
converted/
*.pdf

# Session work
SESSION-*.md
DEV-README.md

# OS
.DS_Store
```

---

## 🚨 Common Mistakes to Avoid

### ❌ Initializing Git in Development Folder

**WRONG:**
```bash
cd /Projects/my_project/
git init  # ❌ This folder has personal data!
```

**CORRECT:**
```bash
cd /Projects/repos/my-project/
git init  # ✅ Only initialize git in clean repo
```

---

### ❌ Copying Everything to Repository

**WRONG:**
```bash
cp -r /Projects/my_project/* /Projects/repos/my-project/  # ❌ Copies personal data!
```

**CORRECT:**
```bash
# Copy ONLY production files
cp /Projects/my_project/script.py /Projects/repos/my-project/
cp /Projects/my_project/README.md /Projects/repos/my-project/
# NOT test/, venv/, SESSION-*, etc.
```

---

### ❌ Weak .gitignore

**WRONG:**
```
# Only basic excludes
.DS_Store
*.pyc
```

**CORRECT:**
```
# Personal data
test/
output/
*.mp3
*.pdf

# Virtual environments
venv/

# Session work
SESSION-*.md

# OS
.DS_Store

# Python
__pycache__/
*.pyc
```

---

### ❌ Committing Before Verifying

**WRONG:**
```bash
git add .
git commit -m "update"  # ❌ Didn't verify!
git push
```

**CORRECT:**
```bash
git add .
git status                    # ✅ Verify staging area
git diff --cached --name-only # ✅ Check files
# Verify no personal data
git commit -m "feat: detailed message"
git push
```

---

## 🔧 Troubleshooting

### "I accidentally committed personal data!"

**If not pushed yet:**
```bash
# Undo last commit, keep changes
git reset --soft HEAD~1

# Remove personal files
rm -rf test/ transcriptions/ venv/

# Verify .gitignore
cat .gitignore

# Re-commit without personal data
git add .
git commit -m "feat: clean commit"
```

**If already pushed:**
```bash
# Contact GitHub support to purge sensitive data
# Or use BFG Repo-Cleaner (advanced)

# Immediate: Delete the repo and recreate
gh repo delete username/repo-name --yes
# Then recreate cleanly
```

---

### "My .gitignore isn't working"

```bash
# Files already tracked? Remove from git
git rm --cached -r test/
git rm --cached venv/ -r

# Commit removal
git commit -m "chore: remove personal data from tracking"

# Verify .gitignore works now
echo "test file" > test/test.txt
git status  # Should NOT show test/test.txt
```

---

### "I want to check all repos for personal data"

```bash
cd "/Users/mac/Documents/Local Vault/Projects/repos"

for repo in */; do
    if [ -d "$repo/.git" ]; then
        echo "=== Checking $repo ==="
        cd "$repo"

        # Check for common personal data patterns
        find . -name "*.mp3" -o -name "*.pdf" -o -name "SESSION-*" -o -name "test" -o -name "venv"

        cd ..
    fi
done
```

---

## 📚 Quick Reference

### New Project Checklist

- [ ] Create development folder in `/Projects/`
- [ ] Create test files, session notes, venv there
- [ ] Develop and test until working
- [ ] Create repository folder in `/Projects/repos/`
- [ ] Copy ONLY production files to repo
- [ ] Create .gitignore (exclude personal data)
- [ ] Create README.md
- [ ] Verify no personal data
- [ ] Initialize git
- [ ] Create initial commit
- [ ] Push to GitHub
- [ ] Verify repository is clean

### Daily Workflow Checklist

- [ ] Work in development folder
- [ ] Test with personal files
- [ ] Copy updated files to repo
- [ ] Test in repo (clean environment)
- [ ] Verify no personal data
- [ ] Commit with clear message
- [ ] Push to GitHub

---

## 🔗 Related Docs

- `GITHUB-WORKFLOW.md` - Complete daily workflow
- `REPO-NAMING.md` - Naming conventions
- `SESSION-TEMPLATE.md` - Session notes template (for development folders)

---

## 📋 Archive Note

**Previous version archived:** 2025-11-12
**Location:** `/Archive/github-workflow-2025-11-12/SETUP.md`
**Reason:** Converted from specific mdcon/sanzo_wada setup to generic setup guide

**Major changes:**
- Converted to generic, repeatable setup process
- Added two-folder system from day one
- Added comprehensive .gitignore examples
- Added pre-commit checklist
- Added troubleshooting section
- Added example projects (mp3-txt, pdf-converter)
- Emphasized repository cleanliness throughout

---

**Remember:** Always create TWO folders (development + repository), keep personal data in development, commit only clean code to repository.

**Next Review:** 2025-12-12
