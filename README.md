# Personal Projects Repository

A collection of tools and applications for music, productivity, and document processing.

## Projects

### 🎵 Strudel Sheet Music Converter

**Location**: `strudel_sheetmusic/`

An intelligent application that transforms PDF sheet music into playable Strudel (TidalCycles) code, bridging traditional music notation with live coding.

**Features**:
- Optical Music Recognition (OMR) from PDF sheet music
- MIDI conversion and processing
- Historical tuning systems (Werkmeister temperaments)
- Strudel/TidalCycles code generation
- Specialized support for organ music
- Instrument mapping interface

**Status**: 🚧 Initial setup phase

[Read more →](strudel_sheetmusic/README.md)

---

### 📝 Convert to Markdown

**Location**: `convert_to_markdown/`

Tools for converting PDFs to markdown format, with OCR support and batch processing capabilities.

**Features**:
- PDF to markdown conversion
- OCR processing
- Batch conversion scripts
- Forever Notes integration
- Multiple conversion tools (mdcon, mdclean)

[Read more →](convert_to_markdown/README.md)

---

### 🎙️ MP3 to Text (Transcription)

**Location**: `mp3_txt/`

Audio transcription tools using Whisper and various processing backends.

**Features**:
- Whisper-based transcription
- Multiple transcription backends
- Markdown cleaning with llama3.2:1b
- Streaming transcription support
- Enhanced transcription options

[Read more →](mp3_txt/USAGE_GUIDE.md)

---

### ⏱️ Time Keeping

**Location**: `time_keeping/`

iOS Shortcuts-based time tracking system with visual indicators and backup functionality.

**Features**:
- iOS Shortcuts integration
- Color-coded time tracking
- Automated backups
- SQLite database
- Markdown reports

[Read more →](time_keeping/README.md)

---

### ☁️ Cloud Vault Mirror

**Location**: `cloud_vault_mirror/`

Tools for mirroring and syncing cloud vaults.

---

### 📚 Git Documentation

**Location**: `git_docs/`

Documentation and workflows for git operations and repository management.

**Features**:
- Session templates
- GitHub workflow guides
- Setup documentation
- Handoff procedures

---

### 🎨 Sanzo Wada

**Location**: `sanzo_wada/`

Color palette tools based on Sanzo Wada's color combinations.

---

## Quick Start

### Strudel Sheet Music Converter

```bash
cd strudel_sheetmusic

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Try the demo
python examples/quickstart.py

# Use CLI
python cli.py show-tuning werkmeister1
python cli.py compare-tunings C#4
```

### MP3 Transcription

```bash
cd mp3_txt

# Install requirements
pip install -r requirements.txt

# Transcribe audio
./transcribe input.mp3

# Clean transcript with AI
python mdclean_simple.py transcript.txt
```

### PDF to Markdown

```bash
cd convert_to_markdown

# Convert single PDF
./mdcon input.pdf output.md

# Batch convert
./mdcon_batch *.pdf
```

## Repository Structure

```
repos/
├── strudel_sheetmusic/    # NEW: Sheet music to Strudel converter
├── convert_to_markdown/   # PDF/OCR conversion tools
├── mp3_txt/               # Audio transcription
├── time_keeping/          # Time tracking
├── cloud_vault_mirror/    # Cloud sync tools
├── git_docs/              # Git workflows
├── sanzo_wada/            # Color palettes
└── mdcon/                 # Markdown conversion utilities
```

## Contributing

These are personal projects, but suggestions and improvements are welcome through issues or pull requests.

## License

Each project may have its own license. Check individual project directories for details.

## Recent Updates

- **2025-11-13**: Added Strudel Sheet Music Converter project with comprehensive documentation
- **2025-11-12**: Enhanced MP3 transcription with llama3.2:1b cleaning
- **Earlier**: Various tools and utilities for productivity and media processing

---

**Note**: This repository serves as a central collection of personal tools and experiments. Projects are at various stages of completion.
