# Session Template - GitHub Workflow

**Date:** YYYY-MM-DD
**Start Time:** HH:MM
**Project(s):** repo-name(s)

---

## ⚠️ IMPORTANT: Session Notes Location

**Session notes should ONLY be saved in development folders, NEVER in repositories.**

**Correct location:**
```
/Projects/my_project/SESSION-2025-11-12.md  ✅
```

**WRONG location:**
```
/Projects/repos/my-project/SESSION-*.md  ❌ (will be committed to git!)
```

**Why:** Session notes contain personal information, work-in-progress details, and debugging notes that should not be shared publicly in git repositories.

---

## 🎯 Session Goal

[ONE specific goal for this session]

**Success Criteria:**
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] [Measurable outcome 3]

---

## 📂 Repositories Worked On

### [repo-name]

**Branch:** `main` or `feature/branch-name`

**Starting State:**
```bash
# Output of: git status
```

---

## ✅ Work Completed

### Code Changes
- [ ] File/feature worked on
- [ ] Tests added/updated
- [ ] Documentation updated

### Commits Made

```
commit-hash: type: brief message
commit-hash: type: brief message
```

**Total commits:** X

---

## 🧪 Testing Done

### In Development Folder
**Location:** `/Projects/my_project/`
- [ ] Tested with personal data/files
- [ ] Happy path works
- [ ] Edge cases handled
- [ ] Error handling verified

### In Repository Folder
**Location:** `/Projects/repos/my-project/`
- [ ] Copied production files to repo
- [ ] Tested in clean environment
- [ ] All dependencies work
- [ ] Scripts executable

**Test commands run:**
```bash
# In development folder (with personal data)
./script test/my-personal-file.mp3

# In repo folder (clean test)
./script sample-file.mp3
```

**Results:** ✅ All passed / ⚠️ Issues found

---

## 🔄 Development ↔ Repository Sync

### Files Copied to Repo
```bash
# Example:
cp transcribe /Users/mac/Documents/Local\ Vault/Projects/repos/mp3-txt/
cp transcribe_vosk_stream.py /Users/mac/Documents/Local\ Vault/Projects/repos/mp3-txt/
cp README.md /Users/mac/Documents/Local\ Vault/Projects/repos/mp3-txt/
```

- [ ] Source code copied
- [ ] Documentation updated
- [ ] Configuration files (if needed)
- [ ] Requirements/dependencies file updated

### Repository Cleanliness Check

**Before committing, verify:**
- [ ] No personal data in repo folder
- [ ] No test files with real user data (test/, test_output/)
- [ ] No output directories with personal content (transcriptions/, output/)
- [ ] No virtual environments (venv/, node_modules/)
- [ ] No session notes (SESSION-*.md)
- [ ] No planning docs with personal info
- [ ] .gitignore properly excludes personal files
- [ ] README has generic examples only
- [ ] No API keys or credentials

**Think:** "Could someone clone this repo and use it without seeing my personal data?"

---

## 💡 Learned

### Technical Insights
- [What you learned about the code/tool/language]

### Problems Solved
- **Problem:** [Description]
  **Solution:** [How you solved it]

### Decisions Made
- **Decision:** [What you decided]
  **Rationale:** [Why]

---

## 📝 Git Activity

### Commits
```bash
# git log output
abc1234: feat: add batch processing
def5678: docs: update README
```

### Pushed to GitHub?
- [ ] Yes, pushed X commits to repo-name
- [ ] No, still local (reason: ___)

### Branches
- Working on: `main` / `feature/___`
- Merged: none / `feature/___` → `main`
- Deleted: none / `feature/___`

---

## 🐛 Issues Found

### Bugs
- [ ] [Bug description] - Fixed / Filed as issue

### Known Issues
- [ ] [Issue description] - TODO / Documented

---

## 📋 Next Session

### Immediate Next Steps
1. [Most important next task]
2. [Second priority]
3. [Third priority]

### Blockers
- [Anything blocking progress]

### Questions to Research
- [Questions that came up]

---

## ⏱️ Time Tracking

**Duration:** [X hours/minutes]
**Focus areas:**
- [ ] Coding: ___
- [ ] Testing: ___
- [ ] Debugging: ___
- [ ] Documentation: ___
- [ ] Learning/Research: ___

---

## 🔄 Sync Status

### Development ↔ Repository
- [ ] Changes copied from `Projects/[Project]/` to `repos/[repo]/`
- [ ] Repository cleanliness verified (no personal data)
- [ ] Tested in repo folder
- [ ] Committed to git

### Local ↔ GitHub
- [ ] All commits pushed
- [ ] Remote is up to date
- [ ] No personal data committed (double-checked)

---

## 📸 Session Snapshot

**Development Folder State:**
```bash
# In /Projects/my_project/
ls -la
# Shows: source code, test/, output/, venv/, session notes
```

**Repository Folder State:**
```bash
# In /Projects/repos/my-project/
git status
git diff --stat
```

**Current repo files:**
```bash
# Output of: ls -la
# Should show: source code, docs, .gitignore, NO personal data
```

---

## 💭 Reflections

### What Went Well
- [What worked smoothly]

### What Was Frustrating
- [What slowed you down]

### What to Improve
- [Process improvements for next time]

---

## 🔗 Related Sessions

- Previous: SESSION-YYYY-MM-DD.md
- Related: SESSION-YYYY-MM-DD.md (other project)

---

## 📋 Pre-Commit Checklist

**Use this before every commit:**

**Repository Cleanliness:**
- [ ] No personal audio/video files in repo
- [ ] No personal PDFs or documents in repo
- [ ] No test files with real user data
- [ ] No output directories with personal content
- [ ] No virtual environments (venv/, node_modules/)
- [ ] No session notes or planning docs
- [ ] No API keys or credentials
- [ ] .gitignore properly configured
- [ ] README has generic examples only

**Code Quality:**
- [ ] Tests passing
- [ ] Scripts executable (chmod +x)
- [ ] No hardcoded paths
- [ ] All file paths relative
- [ ] Comments explain "why" not "what"

**Documentation:**
- [ ] README updated
- [ ] Usage examples current
- [ ] Dependencies listed
- [ ] Installation instructions clear

---

## 📦 Archive Note

**Template Updated:** 2025-11-12
**Previous version:** Archived to `/Archive/github-workflow-2025-11-12/`

**Major changes:**
- Added "Session Notes Location" warning
- Added two-folder system sections
- Added "Repository Cleanliness Check"
- Separated testing into development vs repository
- Added "Pre-Commit Checklist"
- Emphasized keeping personal data out of repos

---

**End Time:** HH:MM
**Status:** Complete ✅ / In Progress ⏳ / Blocked 🚫

---

## 🔗 Related Docs

- `GITHUB-WORKFLOW.md` - Complete workflow with two-folder system
- `REPO-NAMING.md` - Naming conventions for repos and files
- `SETUP.md` - Initial GitHub setup guide
