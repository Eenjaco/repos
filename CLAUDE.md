# CLAUDE.md - AI Assistant Guide

This document provides comprehensive guidance for AI assistants working with this repository.

## Repository Overview

**Purpose:** Personal productivity and knowledge management toolkit - a monorepo containing complementary tools for document conversion, audio transcription, and time tracking, all designed to integrate with an Obsidian-based markdown knowledge base.

**Philosophy:**
- Unix philosophy: Do one thing well, compose tools together
- Local-first approach with cloud fallbacks
- Clean separation between development and production code
- Obsidian-friendly markdown output
- Cross-platform compatibility (macOS/Linux)

**Repository Statistics:**
- **Projects:** 7 directories (3 active, 4 placeholders)
- **Languages:** Bash (~60%), Python (~35%), Node.js (~5%)
- **Lines of Code:** ~2,132 (excluding node_modules)
- **Documentation:** 30+ markdown files

---

## Project Structure

```
/home/user/repos/
├── convert_to_markdown/    # Universal document to markdown converter
├── mp3_txt/                # Audio transcription with AI cleaning
├── time_keeping/           # Time tracking system (terminal + iOS)
├── git_docs/               # Repository documentation and workflows
├── cloud_vault_mirror/     # [Placeholder] Cloud sync
├── sanzo_wada/            # [Placeholder] Color palettes
├── mdcon/                 # [Placeholder] Future mdcon module
└── .gitignore             # Excludes audio, models, secrets, cache
```

---

## Active Projects

### 1. `convert_to_markdown/` - Document Converter (203 KB)

**Purpose:** Convert PDF, DOCX, EPUB, and HTML to clean markdown.

**Key Scripts:**
- `mdcon` (bash, 21KB) - Main universal converter with interactive menu
- `mdclean` (bash, 22KB) - Post-processing cleanup script
- `mdcon_batch` - Batch processing wrapper
- Legacy: `pdf_to_md.sh`, `forever_notes_ocr.sh`

**Technologies:**
- Pandoc (universal document conversion)
- Ghostscript + Tesseract (OCR for scanned PDFs)
- pdftotext (text extraction)
- ImageMagick (image processing)

**Workflow:**
1. Input file → Type detection (scanned vs text PDF)
2. Scanned → OCR pipeline | Text → Direct extraction
3. Pandoc conversion → `filename-raw.md`
4. Optional: `mdclean` → `filename.md`
5. Output ready for Obsidian vault

**Entry Point:**
```bash
cd convert_to_markdown
./mdcon  # Interactive menu
```

**Documentation:**
- `README.md` - Quick start
- `PROJECT_OVERVIEW.md` - Architecture
- `DESIGN.md` - Technical decisions
- `QUICKSTART.md` - 3-minute reference
- `FOREVER_NOTES_INTEGRATION.md` - Obsidian integration

**Code Location:** `convert_to_markdown/mdcon:1-500` (main script)

---

### 2. `mp3_txt/` - Audio Transcription (160 KB)

**Purpose:** Transcribe audio files with dual-engine support and AI-powered cleaning.

**Key Scripts:**
- `transcribe` (bash) - Interactive CLI wrapper
- `transcribe_enhanced.py` (python, typer CLI) - Dual-engine transcription
- `transcribe_vosk_stream.py` - Vosk engine (fast, English-only)
- `mdclean_claude.py` - Claude API cleaning (RECOMMENDED)
- `mdclean_simple.py` - Ollama local LLM cleaning
- `mdclean.py` - Full pipeline with Unstructured

**Technologies:**
- Vosk (Kaldi-based, 85-92% accuracy, 40MB-1.8GB models)
- OpenAI Whisper via faster-whisper (95-98% accuracy, multilingual including Afrikaans)
- FFmpeg (audio processing)
- Ollama (local LLMs: llama3.2:1b works on 8GB RAM)
- Claude API (highest quality cleaning)
- Typer + Rich (CLI framework)

**Dependencies:**
```bash
pip install vosk soundfile typer[all] rich
# From requirements.txt in mp3_txt/
```

**Workflow:**
1. Audio file (MP3, M4A, WAV, FLAC)
2. Choose engine: Vosk (fast) or Whisper (accurate)
3. Transcription → `filename.md` with optional timestamps
4. Optional: AI cleaning (Ollama local or Claude API)
5. Output to Obsidian inbox

**Entry Point:**
```bash
cd mp3_txt
./transcribe  # Interactive menu
# Or direct:
python3 transcribe_enhanced.py single file.mp3 --engine whisper
python3 mdclean_claude.py input.md output.md
```

**Performance:**
- Vosk small: 2-3min for 10min audio (40MB model)
- Vosk large: 4-6min for 10min audio (1.8GB model)
- Whisper: ~5min for 10min audio (multilingual)

**Documentation:**
- `README.md` - Quick start with examples
- `ADVANCED.md` - 20+ model options
- `USAGE_GUIDE.md` - Detailed instructions
- `TEST_RESULTS.md` - Model comparisons

**Code Locations:**
- `mp3_txt/transcribe_enhanced.py:1-300` (main transcription)
- `mp3_txt/mdclean_claude.py:1-150` (Claude cleaning)

---

### 3. `time_keeping/` - Time Tracking (371 KB)

**Purpose:** Simple terminal and iOS-based time tracking integrated with Obsidian.

**Key Scripts:**
- `tt` (node.js, v3.0, 49KB) - Main CLI with SQLite database
- `tt_local` (bash) - Simple markdown-based tracking
- `tt_local_shortcuts` - Non-interactive for iOS Shortcuts
- `backup.sh` - Database backup utility

**Technologies:**
- Node.js with better-sqlite3
- Google Sheets API integration
- SQLite database (90KB `timetracking.db`)
- iOS Shortcuts (Apple automation)
- Markdown output (ISO week format)

**Dependencies:**
```json
{
  "googleapis": "^105.0.0",
  "better-sqlite3": "^11.0.0"
}
```

**Workflow:**
1. Start timer: `./tt_local s` or iOS Shortcut
2. Enter task title and subtitle
3. Work session
4. Stop timer: `./tt_local e`
5. Entry saved to `2025-W##.md` (ISO week number)

**Data Files:**
- `timetracking.db` - SQLite database
- `2025-W##.md` - Weekly markdown files
- `.active-timer.json` - Current timer state
- `time_logs/` - Raw logs

**Entry Point:**
```bash
cd time_keeping
./tt          # Main Node.js version
./tt_local s  # Start bash version
./tt_local e  # End bash version
```

**Documentation:**
- `README.md` - Overview
- `SHORTCUTS_SETUP.md` - iOS setup guide
- `DESIGN.md` - Architecture and schema
- `tt_update.md` - Technical design
- `color_guide.md` - Customization

**Code Locations:**
- `time_keeping/tt:1-1500` (main Node.js app)
- `time_keeping/tt_local:1-200` (bash version)

---

### 4. `git_docs/` - Repository Documentation (78 KB)

**Purpose:** Guidelines for managing GitHub repositories and development workflows.

**Key Files:**
- `README.md` - Applications workspace structure
- `SETUP.md` - Two-folder system (dev vs production)
- `HANDOFF.md` - Session handoff notes
- `github_workflow.md` - Repo management
- `repo_naming.md` - Naming conventions
- `session_template.md` - Session notes template
- `session_summary` (bash) - Generate summaries

**Core Concepts:**
- **Two-folder system:** `/Projects/` (dev) vs `/Projects/repos/` (production)
- **Cleanliness:** No personal data in public repos
- **Integration:** Obsidian vault + development tools
- **Workflow:** Clean code copied from dev to repos when ready

---

## Development Workflows

### Document Conversion Workflow

```bash
# Interactive mode
cd convert_to_markdown
./mdcon

# Batch processing
./mdcon_batch /path/to/documents/

# Pipeline: PDF → Raw MD → Cleaned MD
./mdcon input.pdf           # Creates input-raw.md
./mdclean input.pdf raw.md  # Creates input.md
```

### Audio Transcription Workflow

```bash
# Interactive
cd mp3_txt
./transcribe

# Direct usage
python3 transcribe_enhanced.py single audio.mp3 --engine whisper --timestamps

# Cleaning options
python3 mdclean_claude.py transcript.md cleaned.md  # Recommended
python3 mdclean_simple.py transcript.md cleaned.md --model llama3.2:1b
```

### Time Tracking Workflow

```bash
# Terminal
cd time_keeping
./tt_local s  # Start
# Work...
./tt_local e  # End

# iOS Shortcuts
# Use SSH to execute ./tt_local_shortcuts s/e
```

---

## Git Workflow & Conventions

### Branch Naming

**CRITICAL:** All development branches MUST follow this pattern:
```
claude/claude-md-{random-string}-{session-id}
```

**Example:** `claude/claude-md-mhyhp7exeimx5s5g-01BHKx3ZdgpsTSW2rtStqP7A`

**Why:** Push operations will fail with 403 if branch doesn't start with `claude/` and end with matching session ID.

### Git Operations

**Pushing:**
```bash
git push -u origin <branch-name>
# Retry on network failure: up to 4 times with exponential backoff (2s, 4s, 8s, 16s)
```

**Fetching:**
```bash
git fetch origin <branch-name>
# Same retry logic for network failures
```

**Committing:**
- Clear, descriptive commit messages
- Commit when features/fixes are complete
- Follow repository's commit style (see git log)

### Current Git State

```bash
# Check status
git status

# Current branch: claude/claude-md-mhyhp7exeimx5s5g-01BHKx3ZdgpsTSW2rtStqP7A
# Main branch: (not specified - ask user if needed for PRs)
# Recent commits:
#   5556d88 Update README: Add Whisper transcription and llama3.2:1b cleaning
#   c96cb3c Initial commit: mp3_txt, convert_to_markdown, time_keeping, cloud_vault_mirror
```

---

## Key Technologies & Dependencies

### System Requirements

- **OS:** macOS or Linux (Bash scripts are Unix-compatible)
- **Python:** 3.10+ (for audio transcription)
- **Node.js:** 14+ (for time tracking)
- **Memory:** 8GB+ RAM (for local LLM models)
- **Storage:** 40MB-2.3GB (depending on audio models)

### External Tools

**Document Processing:**
- `pandoc` - Universal document converter
- `ghostscript` - PDF manipulation
- `tesseract` - OCR engine
- `pdftotext` - Text extraction
- `imagemagick` - Image processing

**Audio Processing:**
- `ffmpeg` - Audio conversion and streaming
- Vosk models (download separately, 40MB-2.3GB)
- Whisper models (auto-downloaded by faster-whisper)

**AI/LLM:**
- Ollama (local LLM server) with llama3.2:1b (700MB)
- Claude API (requires API key in environment)

### Python Dependencies

From `mp3_txt/requirements.txt`:
```
vosk>=0.3.44
soundfile>=0.13.1
typer[all]>=0.20.0
rich>=14.2.0
faster-whisper  # Not in requirements.txt yet
anthropic       # For Claude API
```

### Node.js Dependencies

From `time_keeping/package.json`:
```json
{
  "googleapis": "^105.0.0",
  "better-sqlite3": "^11.0.0"
}
```

---

## File Organization

### What's Tracked in Git

**Included:**
- All source code (.sh, .py, .js)
- Documentation (.md files)
- Configuration files (package.json, requirements.txt)
- Helper scripts and templates

**Excluded (see `.gitignore`):**
- Python cache (`__pycache__/`, `*.pyc`)
- Virtual environments (`venv/`, `env/`)
- Audio files (`*.mp3`, `*.wav`, `*.m4a`, `*.flac`)
- Model files (`*.onnx`, `*.pt`, `*.bin`, `models/`)
- API keys (`.env`, `*.key`, `secrets.json`)
- Temporary files (`tmp/`, `test_output/`, `*.log`)
- IDE files (`.vscode/`, `.idea/`)
- Node modules (`node_modules/` - restored via npm install)

### Output Locations

**Document Conversion:**
- `filename-raw.md` - Initial conversion output
- `filename.md` - Cleaned output
- `conversion.log` - Detailed conversion log

**Audio Transcription:**
- `filename.md` - Transcription output
- Frontmatter includes source file reference

**Time Tracking:**
- `2025-W##.md` - Weekly markdown files (ISO week format)
- `timetracking.db` - SQLite database
- `.active-timer.json` - Current timer state

---

## AI Assistant Best Practices

### When Working in This Repository

1. **Check documentation first:** Each project has comprehensive README and design docs
2. **Use existing patterns:** Follow Unix philosophy and modular design
3. **Maintain compatibility:** Keep macOS/Linux compatibility for bash scripts
4. **Test thoroughly:** Especially for PDF/audio processing pipelines
5. **Document changes:** Update relevant markdown files
6. **Follow git conventions:** Use proper branch naming (`claude/...`)

### Common Tasks

**Adding a new feature to mdcon:**
1. Read `convert_to_markdown/PROJECT_OVERVIEW.md`
2. Review `convert_to_markdown/DESIGN.md` for patterns
3. Edit `convert_to_markdown/mdcon` (main script)
4. Test with various input types
5. Update documentation in `README.md`

**Adding a new transcription model:**
1. Read `mp3_txt/ADVANCED.md` for model options
2. Edit `mp3_txt/transcribe_enhanced.py`
3. Add model to CLI options
4. Test accuracy and performance
5. Update `TEST_RESULTS.md` with benchmarks

**Modifying time tracking:**
1. Review `time_keeping/DESIGN.md` for schema
2. Check if change affects both `tt` and `tt_local`
3. Update database schema if needed
4. Test iOS Shortcuts integration
5. Update `SHORTCUTS_SETUP.md` if workflow changes

### Code Quality Standards

**Bash Scripts:**
- Use `#!/usr/bin/env bash` shebang
- Add error handling (`set -e` or explicit checks)
- Include usage/help functions
- Comment complex sections
- Quote variables to prevent word splitting
- Use meaningful variable names

**Python Scripts:**
- Follow PEP 8 style guidelines
- Use type hints where helpful
- Include docstrings for functions
- Use Typer for CLI interfaces
- Add Rich for progress bars/formatting
- Handle errors gracefully

**Node.js Scripts:**
- Use modern JavaScript (ES6+)
- Handle async operations properly
- Validate user input
- Include error messages
- Follow existing code style

### Security Considerations

**Never commit:**
- API keys or secrets
- Personal data or logs
- Audio files with private content
- Database files with personal time tracking

**Check before pushing:**
- `.env` files excluded
- No hardcoded credentials
- `.gitignore` properly configured
- Personal file paths removed

---

## Documentation Index

### By Project

**convert_to_markdown/**
- `README.md` - User guide with workflows
- `PROJECT_OVERVIEW.md` - Architecture and future plans
- `DESIGN.md` - Technical design decisions
- `QUICKSTART.md` - 3-minute quick reference
- `FOREVER_NOTES_INTEGRATION.md` - Obsidian integration
- `INDEX.md` - File navigation

**mp3_txt/**
- `README.md` - Quick start with examples
- `ADVANCED.md` - 20+ language models
- `USAGE_GUIDE.md` - Detailed instructions
- `TEST_RESULTS.md` - Model comparisons
- `PROJECT-OVERVIEW.md` - Feature documentation

**time_keeping/**
- `README.md` - Overview and quick start
- `SHORTCUTS_SETUP.md` - iOS Shortcuts guide
- `DESIGN.md` - Architecture and schema
- `tt_update.md` - Technical design notes
- `project_structure.md` - Directory layout
- `color_guide.md` - Customization options

**git_docs/**
- `SETUP.md` - Repository setup
- `HANDOFF.md` - Session handoff notes
- `github_workflow.md` - Repo management
- `repo_naming.md` - Naming conventions

---

## Quick Reference

### Entry Points

```bash
# Document conversion
cd convert_to_markdown && ./mdcon

# Audio transcription
cd mp3_txt && ./transcribe

# Time tracking (Node.js version)
cd time_keeping && ./tt

# Time tracking (Bash version)
cd time_keeping && ./tt_local s/e
```

### Common Commands

```bash
# Batch convert all PDFs in a directory
cd convert_to_markdown
./mdcon_batch /path/to/pdfs/

# Transcribe with Whisper and clean with Claude
cd mp3_txt
python3 transcribe_enhanced.py single audio.mp3 --engine whisper
python3 mdclean_claude.py audio.md audio-cleaned.md

# Check time tracking status
cd time_keeping
./tt_local status

# Backup time tracking data
cd time_keeping
./backup.sh
```

### File Locations

| Purpose | Path |
|---------|------|
| Main document converter | `convert_to_markdown/mdcon` |
| Document cleaner | `convert_to_markdown/mdclean` |
| Transcription CLI | `mp3_txt/transcribe` |
| Transcription engine | `mp3_txt/transcribe_enhanced.py` |
| Claude cleaning | `mp3_txt/mdclean_claude.py` |
| Time tracking (Node) | `time_keeping/tt` |
| Time tracking (Bash) | `time_keeping/tt_local` |
| Time tracking DB | `time_keeping/timetracking.db` |

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│      Personal Productivity & Knowledge Management       │
│              Toolkit (Monorepo)                         │
└─────────────────────────────────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │  Document    │ │    Audio     │ │     Time     │
    │ Conversion   │ │Transcription │ │   Tracking   │
    │              │ │              │ │              │
    │   mdcon      │ │ transcribe   │ │   tt/local   │
    │   mdclean    │ │ Vosk/Whisper │ │   SQLite     │
    │   Pandoc     │ │ Ollama/Claude│ │   Markdown   │
    │   Tesseract  │ │              │ │   iOS        │
    └──────────────┘ └──────────────┘ └──────────────┘
          │                │                │
    [PDF/DOCX/EPUB]  [MP3/M4A/WAV]   [Terminal/iOS]
          │                │                │
          └────────────────┼────────────────┘
                           │
                ┌──────────▼──────────┐
                │   Obsidian Vault   │
                │  (Markdown Files)  │
                │                    │
                │  - Daily Notes     │
                │  - Transcripts     │
                │  - Time Logs       │
                │  - Wikilinks       │
                └────────────────────┘
```

---

## Recent Development History

**Latest Commit:** "Update README: Add Whisper transcription and llama3.2:1b cleaning"

**Recent Session (Nov 13, 2025):**
- ✅ Added Afrikaans support via Whisper
- ✅ Created dual-mode transcription (Vosk + Whisper)
- ✅ Built multiple mdclean versions (Ollama, Claude API)
- ✅ Tested local LLM models (llama3.2:1b recommended for 8GB RAM)
- ✅ Initialized git repository
- ✅ Created comprehensive documentation

**Known Issues/Notes:**
- Local Ollama models 0.5B and 3B don't work well on 8GB RAM
- Claude API recommended for best cleaning quality (~$0.01-0.10/transcript)
- llama3.2:1b (700MB) works on 8GB RAM but quality varies

---

## Future Placeholders

### `cloud_vault_mirror/`
**Status:** Empty directory
**Purpose:** Cloud vault synchronization (not yet implemented)

### `sanzo_wada/`
**Status:** Empty directory
**Purpose:** Color palette tools (not yet implemented)

### `mdcon/`
**Status:** Empty directory
**Purpose:** Future refactored mdcon module (currently in convert_to_markdown/)

---

## Support & Resources

**For AI Assistants:**
- Read project-specific documentation before making changes
- Follow existing code patterns and conventions
- Test thoroughly with real-world files
- Update documentation alongside code changes
- Maintain cross-platform compatibility

**For Users:**
- Each project has detailed README with quick start
- Check DESIGN.md files for architecture understanding
- See QUICKSTART.md files for rapid reference
- Refer to TEST_RESULTS.md for performance data

---

**Last Updated:** November 14, 2025
**Repository Version:** Initial release (2 commits)
**Maintainer:** Personal productivity toolkit
**License:** (Not specified - assumed personal use)
