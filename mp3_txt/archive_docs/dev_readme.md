# mp3_txt - Development Folder

**Location:** `/Users/mac/Documents/Local Vault/Projects/mp3_txt/`

This is the **development and testing folder** with personal data, test files, and work-in-progress materials.

---

## 📂 Folder Structure

### Development Folder (this folder)
**Purpose:** Testing, development, personal transcriptions

**Contents:**
- `test/` - Test audio files (personal)
- `test_output/` - Test transcription outputs
- `transcriptions/` - Working transcription outputs
- `venv/` - Python virtual environment
- Personal planning docs and session summaries
- All the scripts and tools for development

**Do NOT commit to git** - Contains personal information

---

### Public Repository
**Location:** `/Users/mac/Documents/Local Vault/Projects/repos/mp3_txt/`

**Purpose:** Clean, distributable version for public use

**Contents:**
```
repos/mp3_txt/
├── .git/                          # Git repository
├── .gitignore                     # Git ignore rules
├── README.md                      # User guide
├── PROJECT-OVERVIEW.md            # Technical specs
├── ADVANCED.md                    # Advanced features
├── requirements.txt               # Python dependencies
├── transcribe                     # Main CLI
├── transcribe_vosk_stream.py      # Core engine
└── test_debug.py                  # Debug tool
```

**This is the public-facing repository** - No personal data, ready to share

---

## 🔄 Workflow

### Development
1. Work in this folder (`/Projects/mp3_txt/`)
2. Test with personal audio files
3. Create transcriptions in `transcriptions/`
4. Keep session notes and summaries here

### Publishing Updates
1. Make changes to code in this folder
2. Test thoroughly with personal files
3. Copy updated files to `/Projects/repos/mp3_txt/`
4. Commit to git repository there
5. Push to remote (GitHub, GitLab, etc.)

### Syncing Files
```bash
# Copy updated files to repos (when ready to publish)
cp transcribe /Users/mac/Documents/Local\ Vault/Projects/repos/mp3_txt/
cp transcribe_vosk_stream.py /Users/mac/Documents/Local\ Vault/Projects/repos/mp3_txt/
cp README.md /Users/mac/Documents/Local\ Vault/Projects/repos/mp3_txt/
cp ADVANCED.md /Users/mac/Documents/Local\ Vault/Projects/repos/mp3_txt/

# Then commit in repos folder
cd /Users/mac/Documents/Local\ Vault/Projects/repos/mp3_txt/
git add .
git commit -m "update: description of changes"
```

---

## 📝 Files in This Folder

### Production Files (sync to repos)
- `transcribe` - Main CLI
- `transcribe_vosk_stream.py` - Core engine
- `test_debug.py` - Debug tool
- `requirements.txt` - Dependencies
- `README.md` - User documentation
- `PROJECT-OVERVIEW.md` - Technical specs
- `ADVANCED.md` - Advanced features
- `.gitignore` - Git ignore rules

### Development Only (keep private)
- `test/` - Personal test audio
- `test_output/` - Test outputs
- `transcriptions/` - Working transcriptions
- `venv/` - Virtual environment
- `SESSION-SUMMARY-2025-11-12.md` - Session notes
- `DEV-README.md` - This file
- Any personal audio files
- Any personal transcripts

### Old Planning Docs (archived in repos)
- `batch_whispersync_transcriber_project_overview.md`
- `mp3_txt_ project_overview.md`
- `vosk_lightweight_bulk_processor_project_overview.md`

These were used during planning but superseded by `PROJECT-OVERVIEW.md`. Kept here for reference but not in public repo.

---

## 🚀 Usage (Development)

```bash
# Activate virtual environment
cd "/Users/mac/Documents/Local Vault/Projects/mp3_txt"
source venv/bin/activate

# Run transcribe CLI
./transcribe

# Or directly with Python
python3 transcribe_vosk_stream.py single test/audio.mp3 --outdir transcriptions

# Test with debug script
python3 test_debug.py
```

---

## 📦 Repository Status

**Development folder:** Not a git repository (personal data)
**Repos folder:** ✅ Clean git repository ready for distribution

**Current commit:**
```bash
cd /Users/mac/Documents/Local\ Vault/Projects/repos/mp3_txt/
git log --oneline
# d82f67e (HEAD -> main) feat: initial commit - audio transcription tool
```

---

## 🔐 Privacy

**Keep private:**
- Test audio files (sermons, audiobooks, personal recordings)
- Transcription outputs (personal content)
- Session summaries (work notes)
- Virtual environment (large, personal setup)

**Safe to share (in repos/):**
- Source code
- Documentation
- Configuration files
- Requirements list

---

**Created:** 2025-11-12
**Purpose:** Development workspace with personal data
**Public repo:** /Projects/repos/mp3_txt/
