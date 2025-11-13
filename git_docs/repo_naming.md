# Repository Naming Conventions

**Last Updated:** 2025-11-12
**Status:** Active
**Purpose:** Naming standards for GitHub repositories and files within them

---

## 🎯 Quick Rules

### GitHub Repository Names
- **Format:** `lowercase-with-hyphens`
- **Examples:** `mdcon`, `sanzo-wada`, `time-tracker`, `mp3-txt`
- **Keep short:** 2-3 words max
- **Descriptive:** What does it do?

### Development Folder Names
- **Format:** `Project Name` or `project_name` (flexible)
- **Examples:** `Convert to markdown`, `mp3_txt`, `Time Keeping`
- **Location:** `/Projects/project_name/`
- **Purpose:** Development workspace with personal data

### Files Within Repos
Follow standard conventions:

| Type | Format | Example |
|------|--------|---------|
| Documentation | `UPPERCASE.md` | `README.md`, `CHANGELOG.md` |
| Scripts | `lowercase-hyphens` | `mdcon`, `backup-db` |
| Config | `lowercase.ext` | `config.json`, `settings.yaml` |
| Source code | Language convention | `main.py`, `index.js` |

---

## 📁 Two-Folder System

### Pattern: Development + Repository

Every project has TWO locations:

```
Projects/
├── my_project/                    # Development folder (NOT git)
│   ├── Source code (working)
│   ├── test/                      # Personal test files
│   ├── output/                    # Personal outputs
│   ├── venv/                      # Virtual environment
│   ├── SESSION-*.md               # Session notes
│   └── Planning docs
│
└── repos/
    └── my-project/                # Repository (git tracked)
        ├── Source code (clean)
        ├── README.md
        ├── .gitignore
        └── Generic examples only
```

### Naming Pattern

| Location | Name Format | Example |
|----------|-------------|---------|
| Development | Flexible | `mp3_txt` or `Convert to markdown` |
| Repository | `lowercase-hyphens` | `mp3-txt` or `mdcon` |

**Why different?**
- Development folders are for YOU (flexible naming)
- Repository folders are for PUBLIC (standard naming)
- Separator helps avoid confusion

---

## 📦 Repository Names

### Good Names

✅ `mdcon` - Clear abbreviation (markdown converter)
✅ `sanzo-wada` - Project name
✅ `time-tracker` - Descriptive function
✅ `pdf-tools` - Clear category
✅ `mp3-txt` - Clear purpose (MP3 to text)

### Avoid

❌ `my-tool` - Too generic
❌ `Project1` - Unclear
❌ `md_converter` - Use hyphens, not underscores
❌ `MDConverter` - No CamelCase
❌ `mp3_txt` - Underscores (use hyphens for repos)

---

## 🚫 Files to NEVER Commit

### Personal Data
```
# Audio/video files
*.mp3
*.wav
*.m4a
*.mp4

# PDFs with personal content
*.pdf

# Output directories
transcriptions/
output/
results/
```

### Development Artifacts
```
# Virtual environments
venv/
env/
node_modules/

# Python cache
__pycache__/
*.pyc
*.pyo

# Session work
SESSION-*.md
NOTES-*.md
TODO-*.md

# Test data
test/
test_output/
my_tests/
```

### Large/Temporary Files
```
# OS files
.DS_Store
Thumbs.db
._*

# Editor files
.vscode/
.idea/
*.swp
*.swo

# Backups
*.bak
*.tmp
*~
```

---

## 📄 Standard Repo Structure

### Minimal Repository (Clean, Public)
```
repo-name/
├── README.md                # Required: What, why, how
├── LICENSE                  # Optional but recommended
├── .gitignore              # Required: Excludes personal data
├── requirements.txt         # Dependencies (Python)
├── package.json            # Dependencies (Node.js)
├── script-name             # Main executable
└── src/                    # Source code (if applicable)
```

### Development Folder (Private, Personal)
```
my_project/
├── All the above files (working copies)
├── test/                   # Personal test files
├── output/                 # Personal outputs
├── venv/                   # Virtual environment
├── SESSION-2025-11-12.md   # Session notes
├── DEV-README.md           # Development notes
└── Planning docs
```

---

## 📋 Required Files

### README.md

Must include:
- Project title and one-line description
- Installation instructions
- Basic usage examples
- Requirements/dependencies

**Template:**
```markdown
# Project Name

One-line description of what it does.

## Installation

\`\`\`bash
# Steps to install
\`\`\`

## Usage

\`\`\`bash
# Basic usage
\`\`\`

## Requirements

- bash 3.2+
- pandoc (for PDF conversion)
```

### .gitignore

**CRITICAL:** Must exclude all personal data.

**Minimum for all projects:**
```
# macOS
.DS_Store
._*

# Temp files
*.tmp
*.swp
*.bak

# Editor
.vscode/
.idea/

# Session work
SESSION-*.md
NOTES-*.md
```

**Project-specific additions:**

**Python projects:**
```
# Virtual environment
venv/
env/

# Python cache
__pycache__/
*.pyc
```

**Audio/transcription projects:**
```
# Personal audio
test/
test_output/
transcriptions/
*.mp3
*.wav
*.m4a

# Output
output/
results/
```

**PDF processing projects:**
```
# Personal PDFs
test/
test_pdfs/
*.pdf

# Output
output/
converted/
```

---

## 🎨 Examples from Our Repos

### mdcon Repository

**Development folder:**
```
Projects/Convert to markdown/
├── mdcon (working)
├── mdclean (working)
├── test/                    # Personal PDFs
├── output/                  # Personal conversions
├── SESSION-*.md             # Session notes
└── Planning docs
```

**Repository (clean, public):**
```
repos/mdcon/
├── .git/
├── .gitignore              # Excludes test/, output/, *.pdf
├── README.md
├── Makefile
├── mdcon                   # Main converter
├── mdclean                 # Cleaner
└── mdclean-v2              # Advanced cleaner
```

**Why it works:**
- Related tools grouped together
- Clear, descriptive names
- NO personal PDFs in repo
- Test files stay in development folder

### mp3_txt Repository

**Development folder:**
```
Projects/mp3_txt/
├── transcribe (working)
├── transcribe_vosk_stream.py (working)
├── test/                    # Personal audio files (sermons, audiobooks)
├── transcriptions/          # Personal transcription outputs
├── venv/                    # Virtual environment
├── SESSION-2025-11-12.md    # Session notes
└── DEV-README.md            # Development notes
```

**Repository (clean, public):**
```
repos/mp3-txt/
├── .git/
├── .gitignore              # Excludes test/, transcriptions/, *.mp3
├── README.md               # User guide
├── PROJECT-OVERVIEW.md     # Technical specs
├── ADVANCED.md             # Advanced features
├── requirements.txt
├── transcribe              # CLI
└── transcribe_vosk_stream.py  # Core engine
```

**Why it works:**
- Zero personal data in repo
- Anyone can clone and use immediately
- Test files and outputs stay private
- Clean, distributable code only

### sanzo_wada Repository

**Repository structure:**
```
sanzo_wada/
├── README.md
├── .gitignore
├── Makefile
├── sanzo_import.py         # Import colors
├── show_combinations.py    # Show combos
└── sanzo_wada.json         # Data file
```

**Why it works:**
- Python naming for .py files
- Clear purpose for each file
- Data file included (not personal)
- Ready to share

---

## 💡 Naming Tips

### For Repos

1. **Think of npm/pip:** Would this make sense as a package name?
2. **Check GitHub:** Is the name already taken?
3. **Future-proof:** Generic enough to grow, specific enough to understand
4. **Avoid versions:** Don't name `tool-v2`, just `tool`
5. **Use hyphens:** `my-tool` not `my_tool` or `MyTool`

### For Development Folders

1. **Flexible naming:** Use whatever makes sense to you
2. **Consistency:** Pick a pattern and stick to it
3. **Clear purpose:** You should know what it is at a glance
4. **Examples:**
   - `Convert to markdown` (descriptive)
   - `mp3_txt` (matches project concept)
   - `Time Keeping` (multi-word, clear)

### For Files

1. **Action verbs for scripts:** `backup-db`, `analyze-log`, `convert-file`
2. **Nouns for data:** `config.json`, `colors.json`, `cache.db`
3. **Standard names:** `README.md`, `LICENSE`, `Makefile`
4. **No spaces:** Use hyphens or underscores, not spaces

### For Commits

1. **Present tense:** "add feature" not "added feature"
2. **Imperative mood:** "fix bug" not "fixes bug"
3. **Lowercase first word:** "add" not "Add"
4. **No period at end:** "add feature" not "add feature."

---

## 📝 Commit Messages

### Format

```
type: brief description

Optional longer description.
```

### Types

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `style:` - Formatting
- `refactor:` - Code restructure
- `test:` - Tests
- `chore:` - Maintenance

### Examples

```
feat: add batch processing mode
fix: handle filenames with spaces
docs: update installation guide
refactor: extract parsing logic to function
chore: update dependencies
```

---

## 🏷️ Tags and Releases

### Version Tags

Use semantic versioning: `v1.0.0`

```bash
git tag -a v1.0.0 -m "First release"
git push origin v1.0.0
```

### When to Tag

- Major releases (v1.0.0, v2.0.0)
- Stable milestones
- Before breaking changes

---

## 🗂️ Branch Naming

### Main Branches

- `main` - Production-ready code
- `develop` - Integration branch (optional for small projects)

### Feature Branches

**Format:** `feature/short-description`

```
feature/add-table-support
feature/batch-mode
fix/space-in-filenames
docs/update-readme
```

### Branch Lifecycle

```bash
# Create
git checkout -b feature/new-thing

# Work, commit
git add .
git commit -m "feat: add new thing"

# Merge when done
git checkout main
git merge feature/new-thing

# Delete
git branch -d feature/new-thing
```

---

## 🚨 Common Mistakes

### ❌ Inconsistent Naming

**Bad:**
```
my-repo/
├── backupDB.sh        # CamelCase
├── convert_file       # snake_case
└── analyze-log        # kebab-case
```

**Good:**
```
my-repo/
├── backup-db          # All kebab-case
├── convert-file
└── analyze-log
```

### ❌ Unclear Names

**Bad:**
- `script.sh` - Which script?
- `utils` - Utilities for what?
- `tmp` - Temporary what?

**Good:**
- `backup-database.sh` - Clear purpose
- `string-utils.py` - Specific utilities
- `temp-conversion-output.txt` - What and why

### ❌ Version in Name

**Bad:**
- `tool-v2`
- `converter-2024`
- `script-new`

**Good:**
- `tool` (use git tags for versions)
- `converter` (date in commits/tags)
- `script` (old versions in git history)

### ❌ Personal Data in Repos

**Bad:**
```
repos/my-tool/
├── test/sermon-2025-11-10.mp3      # Personal audio
├── transcriptions/my_notes.md      # Personal output
├── SESSION-2025-11-12.md           # Session notes
└── venv/                           # Virtual environment
```

**Good:**
```
repos/my-tool/
├── .gitignore                      # Excludes test/, transcriptions/, venv/
├── README.md
├── requirements.txt
└── tool                            # Clean source only
```

**Development folder can have:**
```
Projects/my_tool/
├── test/sermon-2025-11-10.mp3      # ✅ Personal files here
├── transcriptions/my_notes.md      # ✅ Personal outputs here
├── SESSION-2025-11-12.md           # ✅ Session notes here
└── venv/                           # ✅ Venv here
```

---

## 📦 Multi-Project Repositories

**Avoid:** Don't create mono-repos unless necessary.

**Prefer:** Individual repos per project.

**Exception:** Related utilities can share a repo:
```
my-tools/
├── README.md
├── tool-one
├── tool-two
└── tool-three
```

---

## 📚 Quick Reference

```bash
# Good repo names
mdcon
sanzo-wada
time-tracker
backup-tools
mp3-txt

# Good file names
README.md
mdcon
backup-db.sh
config.json
utils.py

# Good commit messages
feat: add batch processing
fix: handle edge case in parser
docs: update installation steps
refactor: extract validation logic

# Good branch names
feature/add-ocr-support
fix/filename-spacing-bug
docs/update-readme
```

---

## 🔐 Repository Cleanliness Checklist

Before committing to repos/:

- [ ] No personal audio/video files
- [ ] No personal PDFs or documents
- [ ] No test files with real user data
- [ ] No output directories with personal content
- [ ] No virtual environments (venv/, node_modules/)
- [ ] No session notes or planning docs
- [ ] No API keys or credentials
- [ ] .gitignore properly configured
- [ ] README has generic examples only
- [ ] All file paths are relative
- [ ] File sizes reasonable (<1MB for code files)

**Think:** "Could a stranger clone this and use it without seeing my personal data?"

---

## 🔗 Related Docs

- `GITHUB-WORKFLOW.md` - Complete workflow with two-folder system
- `SESSION-TEMPLATE.md` - Daily session notes template (for development folders)
- `SETUP.md` - Initial GitHub setup guide

---

## 📋 Archive Note

**Previous version archived:** 2025-11-12
**Location:** `/Archive/github-workflow-2025-11-12/REPO-NAMING.md`
**Reason:** Added two-folder system and repository cleanliness policy

**Major changes:**
- Added two-folder system documentation
- Added "Files to NEVER Commit" section
- Added mp3_txt example showing separation
- Added repository cleanliness checklist
- Expanded .gitignore examples with personal data exclusions

---

**Remember:**
- Repository names use `lowercase-hyphens`
- Development folders are flexible
- Repos are PUBLIC and CLEAN
- Development folders are PRIVATE and can have personal data
- Keep them separate!

**Next Review:** 2025-12-12
