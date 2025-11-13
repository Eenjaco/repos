# Applications - Development Workspace

**Purpose:** Central location for all development projects, documentation, and tutorials.

## Directory Structure

```
Applications/
├── README.md                    # This file
├── repos/                       # Production-ready code for GitHub
│   ├── mdcon/                   # PDF/DOCX to Markdown converter
│   ├── mp3_txt/                 # Audio transcription tool
│   └── sanzo_wada/              # Color palette tools
├── Convert to markdown/         # mdcon development & testing
├── file_renaming/               # Audio file renaming utilities
├── local_llm/                   # Local LLM documentation & experiments
├── mp3_txt/                     # Transcription development & testing
├── ssh/                         # SSH configuration & documentation
├── Time Keeping/                # Time tracking tools
├── GITHUB-WORKFLOW.md           # Git workflow documentation
├── REPO-NAMING.md               # Repository naming conventions
├── SESSION-TEMPLATE.md          # Session notes template
└── SETUP.md                     # Repository setup guide
```

## Philosophy

### Development vs Production

**Development folders** (Convert to markdown/, mp3_txt/, etc.):
- Work in progress, experiments, personal testing
- Can contain personal data, test files, session notes
- Virtual environments, output directories
- NOT tracked in git

**Production repositories** (repos/mdcon/, repos/mp3_txt/, etc.):
- Clean, distributable code only
- NO personal data, NO test files with real data
- Tracked in git, ready for GitHub
- When project is production-ready → move source to repos/ → push to GitHub

### Integration with Knowledge Base

- `/Users/mac/Documents/Local Vault/` = Obsidian knowledge base (only .md files)
- `/Users/mac/Documents/Applications/` = Development workspace
- Keep Local Vault clean - development work happens here in Applications/

### Scripts Location

- Executable scripts: `~/bin/` (in PATH for easy access)
- Script source/development: In respective project folders here
- When script is ready: Copy to ~/bin/ and make executable

## Common Tasks

### Starting New Project

1. Create development folder: `Applications/my_project/`
2. Work, experiment, test with personal data
3. When ready for production:
   - Create clean repo: `Applications/repos/my-project/`
   - Copy only production code (no personal data)
   - Initialize git, push to GitHub
   - Continue development in `Applications/my_project/`

### Moving Scripts to PATH

```bash
# Copy script to ~/bin
cp /path/to/script ~/bin/script-name
chmod +x ~/bin/script-name

# Now accessible from anywhere
script-name
```

### Updating Production Repository

```bash
# Make changes in development folder
cd Applications/my_project/
# Test changes...

# Copy clean code to repository
cp src/* repos/my-project/src/
cd repos/my-project/

# Commit and push
git add .
git commit -m "feat: add new feature"
git push
```

## Inventory & Audits

See `SYSTEM-INVENTORY.md` for complete inventory of installed applications and tools.

Regular audits help track what's installed and identify cleanup opportunities.

---

**Created:** 2025-11-12
**Last Updated:** 2025-11-12

## Documentation

Key documentation files are in `docs/`:
- **SYSTEM-INVENTORY.md** - Complete inventory of all installed apps and tools
- **MIGRATION-DEPENDENCIES-2025-11-12.md** - Guide for fixing post-migration issues
- **RESTRUCTURING-COMPLETE-2025-11-12.md** - Migration completion summary

## Scripts

Utility scripts are in `scripts/` (also copied to ~/bin for easy access):
- **audit-gui-apps.sh** - Scan /Applications for GUI apps
- **audit-cli-apps.sh** - Scan system for CLI tools

Run these periodically to keep SYSTEM-INVENTORY.md up to date.

