# 🎵 Personal Projects Repository

A collection of tools for music, productivity, and document processing.

> **📖 New to this repo?** Read [`.WORKSPACE_GUIDE.md`](.WORKSPACE_GUIDE.md) for how everything works!
> **🚀 Quick start?** Check [`QUICK_REF.md`](QUICK_REF.md) for common commands.

---

## 🎯 Active Projects

### 🎵 StrudelSheet (NEW!)
**Location**: `strudel_sheet/`

Transform PDF sheet music and audio recordings into playable Strudel (TidalCycles) code.

**Features**:
- 📄 PDF sheet music → Strudel code
- 🎵 Audio analysis (MP3, WAV, M4A - Voice Memos work!)
- 🎹 Historical tuning systems (Werkmeister)
- 🎙️ Record audio directly from CLI
- 🎸 BPM, key, chord & melody detection

**Quick start**:
```bash
cd strudel_sheet
source venv/bin/activate
python3 strudel_sheet  # Interactive menu!
```

**Or use commands directly**:
```bash
# Show tuning systems
python3 cli.py show-tuning werkmeister1

# Analyze audio (works with Apple Voice Memos!)
python3 cli.py analyze-audio recording.m4a --detect-chords

# Convert PDF sheet music
python3 cli.py pdf-to-images sheet.pdf -o output/
```

[Read more →](strudel_sheet/README.md) | [Quick Start](strudel_sheet/QUICKSTART.md)

---

### 🎙️ MP3 to Text (Transcription)
**Location**: `mp3_txt/`

Audio transcription using Whisper and Vosk with AI-powered cleanup.

**Features**:
- Whisper/Vosk transcription
- llama3.2:1b markdown cleaning
- Streaming support
- Multiple backends

**Quick start**:
```bash
cd mp3_txt
source venv/bin/activate
./transcribe audio.mp3
```

[Read more →](mp3_txt/USAGE_GUIDE.md)

---

### 📝 Markdown Converter
**Location**: `convert_to_markdown/`

Universal file converter (PDF, EPUB, DOCX → Markdown).

**Features**:
- OCR for scanned PDFs
- Batch processing
- Forever Notes integration
- Multiple conversion tools (mdcon, mdclean)

**Quick start**:
```bash
cd convert_to_markdown
./mdcon file.pdf output.md
```

[Read more →](convert_to_markdown/README.md)

---

### ⏱️ Time Keeping
**Location**: `time_keeping/`

iOS Shortcuts time tracking with SQLite backend.

**Features**:
- Color-coded tracking
- Automated backups
- Markdown reports
- iOS Shortcuts integration

[Read more →](time_keeping/README.md)

---

## 🚀 Quick Setup

### Clone This Repo
```bash
git clone https://github.com/Eenjaco/repos.git
cd repos
```

### Set Up StrudelSheet (Example)
```bash
cd strudel_sheet
python3.13 -m venv venv        # Use 3.13, NOT 3.14!
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements_audio.txt

# Test it
python3 cli.py show-tuning werkmeister1
```

### Create Aliases (Optional but Recommended)
```bash
# StrudelSheet shortcut
cd strudel_sheet
./setup_alias.sh
source ~/.zshrc

# Now just type anywhere:
ss  # Opens StrudelSheet menu!
```

---

## 📚 Documentation

- **[`.WORKSPACE_GUIDE.md`](.WORKSPACE_GUIDE.md)** - How we work together (READ THIS!)
- **[`QUICK_REF.md`](QUICK_REF.md)** - Quick reference card
- Individual project READMEs in each directory

---

## 🛠️ System Requirements

- **Python**: 3.13 preferred (**NOT 3.14** - breaks librosa/numba)
- **OS**: macOS (scripts tested on Mac, 8GB RAM)
- **Terminal**: zsh with oh-my-zsh
- **Tools**: ffmpeg, pandoc, poppler-utils

### Installing System Dependencies
```bash
# macOS (Homebrew)
brew install python@3.13 ffmpeg pandoc poppler

# Verify
python3.13 --version
ffmpeg -version
```

---

## 🎨 Design Philosophy

All projects follow these principles:

- ✅ **Simple commands** - One action, one command
- ✅ **Interactive menus** - Numbered options, clear choices
- ✅ **Drag & drop friendly** - Paste file paths directly
- ✅ **Consistent colors** - Green (#42), Grey (#240) palette
- ✅ **Clear feedback** - ✓ success, ✗ errors, helpful messages
- ✅ **Auto-detection** - Dependencies, file types, configs

---

## 📦 All Projects

```
repos/
├── strudel_sheet/         🎵 NEW! Music → Strudel converter
├── mp3_txt/               🎙️ Audio transcription
├── convert_to_markdown/   📝 Universal file converter
├── time_keeping/          ⏱️ Time tracking
├── cloud_vault_mirror/    ☁️ Cloud sync tools
├── git_docs/              📚 Git workflows
├── sanzo_wada/            🎨 Color palettes
└── mdcon/                 📄 Markdown utilities
```

---

## 🆕 Recent Updates

- **2025-11-14**: 🎉 Added **StrudelSheet** with full audio analysis
  - Works with Apple Voice Memos (M4A)!
  - Record audio directly in CLI
  - Interactive menu system
  - Werkmeister tuning systems working
- **2025-11-12**: Enhanced MP3 transcription with llama3.2:1b
- **Earlier**: Various productivity and media tools

---

## 💡 Pro Tips

### Working with Python
```bash
# Always use 3.13 (not 3.14!)
python3.13 -m venv venv
source venv/bin/activate

# Check version
python --version  # Should be 3.13.x

# If wrong version, recreate venv
deactivate && rm -rf venv
python3.13 -m venv venv && source venv/bin/activate
```

### Working with Audio
```bash
# StrudelSheet supports:
# - MP3, WAV, M4A (Voice Memos!), FLAC, OGG, AIFF

# Test with a Voice Memo:
python3 cli.py analyze-audio ~/Library/Audio/Voice\ Memos/Recording.m4a
```

### Project Navigation
```bash
# Quick jump to any project
cd ~/Documents/Applications/repos/strudel_sheet

# Or use aliases (after setup)
ss  # StrudelSheet
tt  # Time tracking (if set up)
```

---

## 🔗 Quick Links

**StrudelSheet**:
- [Quick Start Guide](strudel_sheet/QUICKSTART.md)
- [Audio Analysis Docs](strudel_sheet/docs/AUDIO_ANALYSIS.md)
- [Project Pitch](strudel_sheet/docs/PROJECT_PITCH.md)
- [Architecture](strudel_sheet/docs/ARCHITECTURE.md)

**Other Projects**:
- [Transcription Guide](mp3_txt/USAGE_GUIDE.md)
- [Workspace Guide](.WORKSPACE_GUIDE.md) ⭐

---

## 🎯 Common Workflows

### Analyze a Song
```bash
cd strudel_sheet && source venv/bin/activate
python3 cli.py analyze-audio ~/Music/song.mp3 --detect-chords
```

### Transcribe Audio
```bash
cd mp3_txt && source venv/bin/activate
./transcribe recording.mp3
```

### Convert PDF
```bash
cd convert_to_markdown
./mdcon document.pdf output.md
```

### Track Time
```bash
cd time_keeping
./backup.sh  # Backup database
```

---

**Happy coding! 🎵🎙️📝**

*For questions, troubleshooting, or collaboration tips, see [`.WORKSPACE_GUIDE.md`](.WORKSPACE_GUIDE.md)*
