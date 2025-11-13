# mp3_txt - Audio Transcription Project

**Created:** 2025-11-11
**Status:** Ready to implement
**Approach:** Vosk-based lightweight CPU transcription
**Success Probability:** 92%
**Complexity:** Low-Medium (2.5/5)

---

## 🎯 Project Goal

Create a command-line tool to batch transcribe MP3/audio files to text using Vosk speech recognition, optimized for MacBook hardware (8GB RAM, i5 CPU).

**Use Case:** Convert audio recordings (lectures, sermons, interviews, voice notes) to markdown text files for integration with Zettelkasten knowledge management system.

---

## ✅ Feasibility Assessment

### Success Probability: 92%

**Why this will succeed:**
- ✅ Complete working code examples already exist (in vosk_lightweight doc)
- ✅ Perfect hardware match (CPU-only, no GPU required)
- ✅ Straightforward dependencies (Python + ffmpeg)
- ✅ Small model size (~40MB for English)
- ✅ Proven technology (Vosk used in production worldwide)
- ✅ Active community and documentation

**Low risks:**
- ⚠️ Accuracy depends on audio quality (but acceptable for personal use)
- ⚠️ Slower than GPU solutions (but acceptable for batch processing)

**Timeline:** 1-2 weeks for full implementation
- Week 1: Basic CLI with single-file transcription
- Week 2: Batch processing, refinements, integration

---

## 🛠️ Technical Approach

### Chosen Solution: Vosk Lightweight Processor

**Why Vosk over alternatives:**
- ✅ Runs entirely on CPU (no GPU needed)
- ✅ Offline processing (no API costs, no internet required)
- ✅ Small model sizes (40MB-1.8GB depending on accuracy needs)
- ✅ Fast enough for personal use (10min audio → ~2-3min processing)
- ✅ Python-native integration
- ⚠️ Whisper would be slower and more resource-intensive on this hardware

---

## 📦 Dependencies

### System Requirements
- **OS:** macOS (Sonoma) ✅
- **Python:** 3.10+ (check: `python3 --version`)
- **RAM:** 8GB ✅
- **CPU:** Intel i5 ✅
- **Disk:** ~500MB (model + dependencies)

### Required Software

#### 1. ffmpeg (Audio Processing)
```bash
# Install via Homebrew
brew install ffmpeg

# Verify installation
ffmpeg -version
```

#### 2. Python Packages
```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install vosk
pip install soundfile
pip install typer[all]
pip install rich
```

#### 3. Vosk Language Model
```bash
# Download small English model (~40MB) - Good for getting started
curl -LO https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip

# Extract to standard location
unzip vosk-model-small-en-us-0.15.zip -d ~/.cache/
mv ~/.cache/vosk-model-small-en-us-0.15 ~/.cache/vosk-model-small-en-us-0.15

# For better accuracy (optional, ~1.8GB):
# curl -LO https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip
```
Full list of models here:

https://alphacephei.com/vosk/models 

---

## 🏗️ Implementation Plan

### Phase 1: Basic Single-File Transcription (Days 1-3)
**Goal:** Get basic transcription working for one file

**Features:**
- Convert MP3 → WAV → Transcribe → TXT/MD
- Command: `transcribe`
- Progress indicator with Rich
- Basic error handling

**Core Script:** `transcribe_vosk.py` (example already exists in documentation)

---

### Phase 2: Batch Processing (Days 4-7)
**Goal:** Process multiple files efficiently

**Features:**
- Folder input: `transcribe ./audio_folder/`
- Parallel processing (2-3 workers)
- Progress bars for each file
- Skip already-transcribed files
- Summary report

**Enhancements:**
- Recursive folder scanning
- Glob pattern support (`transcribe *.mp3`)
- Output naming options

---

### Phase 3: Knowledge Management Integration (Days 8-14)
**Goal:** Connect to Zettelkasten workflow

**Features:**
- Output format: Markdown with metadata
- Auto-create wikilinks for speakers/topics
- Integration with Resources/Notes/literature/
- Template customization

**Example Output:**
```markdown
# Transcription: sermon_2025_11_10.mp3

**Date:** 2025-11-10
**Duration:** 32:45
**Source:** [[Church/Sermons]]

## Transcript

[Transcribed content here...]

## Keywords
- [[Faith]]
- [[Grace]]
- [[Romans 8]]

---
#audio #transcript #sermon
```

---

## 💻 Core Implementation

### Basic Architecture
```
mp3_txt/
├── transcribe_vosk.py      # Main CLI script
├── requirements.txt        # Python dependencies
├── setup.sh               # Automated setup script
├── README.md              # Usage instructions
└── tests/                 # Test audio files
    └── sample.mp3
```

### Key Functions (from vosk documentation)

**1. Audio Conversion (MP3 → WAV)**
```python
def convert_to_wav(input_path: Path, output_path: Path) -> bool:
    """Convert MP3 to 16kHz mono WAV using ffmpeg"""
    cmd = [
        "ffmpeg", "-i", str(input_path),
        "-ar", "16000",  # 16kHz sample rate
        "-ac", "1",      # Mono
        "-y",            # Overwrite
        str(output_path)
    ]
    # Execute with subprocess
```

**2. Vosk Transcription (Streaming)**
```python
def transcribe_wav(model: Model, wav_path: Path) -> str:
    """Transcribe WAV file using Vosk streaming"""
    rec = KaldiRecognizer(model, 16000)
    rec.SetWords(True)

    with sf.SoundFile(wav_path) as audio:
        while True:
            data = audio.read(4000, dtype='int16')
            if len(data) == 0:
                break
            rec.AcceptWaveform(data.tobytes())

    return json.loads(rec.FinalResult())["text"]
```

**3. Batch Processing**
```python
def batch_transcribe(folder: Path, workers: int = 2):
    """Process all audio files in folder with multiprocessing"""
    audio_files = list(folder.glob("*.mp3"))

    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(transcribe_file, f) for f in audio_files]
        for future in as_completed(futures):
            result = future.result()
            # Handle result
```

---

## 🔧 Setup Instructions

### Quick Start (Automated)

We'll create a `setup.sh` script that handles everything:

```bash
# Run setup script
./setup.sh

# Verify installation
python3 transcribe_vosk.py --help
```

### Manual Setup

**Step 1: Install System Dependencies**
```bash
# Install ffmpeg
brew install ffmpeg
```

**Step 2: Create Python Environment**
```bash
cd /Users/mac/Documents/Local\ Vault/Projects/mp3_txt

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install packages
pip install vosk soundfile typer[all] rich
```

**Step 3: Download Vosk Model 0.15✱
```bash
# Create cache directory
mkdir -p ~/.cache

# Download and extract model
curl -LO https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip -d ~/.cache/
rm vosk-model-small-en-us-0.15.zip
```

**Step 3: Download Vosk Model 0.22✱
```bash
  # Create cache directory if needed
  mkdir -p ~/.cache

  # Download large model (~1.8GB - this will take a few minutes)
  cd ~/.cache
  curl -LO https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip

  # Extract (this may take a minute)
  unzip vosk-model-en-us-0.22.zip

  # Cleanup
  rm vosk-model-en-us-0.22.zip

  # Verify it exists
  ls -la ~/.cache/vosk-model-en-us-0.22

  Performance expectations with larger model on your 8GB Mac:
  - Accuracy: ~92% (much better for accents, unclear audio, background noise)
  - Speed: 10min audio → 4-6min processing time
  - RAM usage: ~1.5GB per worker
  - Recommendation: Use --concurrency 1 for batch processing to avoid RAM exhaustion

  Once the download completes, you can test it the same way:

  cd "/Users/mac/Documents/Local Vault/Projects/mp3_txt"
  source venv/bin/activate

  # Test with single file
  python3 transcribe_vosk_stream.py single /path/to/audio.mp3 --outdir ./test_output

  # Or batch process with 1 worker (recommended for 8GB RAM)
  ./transcribe.sh batch /path/to/audio_folder ./output 1

  The larger model will give you significantly better transcription quality,
  especially for sermons, lectures, or any audio with multiple speakers or technical
  terms.
```

---

## 📊 Performance Expectations

### Hardware: 8GB RAM, Intel i5 (CPU-only)

**Small Model (vosk-model-small-en-us-0.15):**
- Size: ~40MB
- Accuracy: ~85% (good for clear speech)
- Speed: 10min audio → 2-3min processing
- RAM usage: ~500MB per worker

**Large Model (vosk-model-en-us-0.22):**
- Size: ~1.8GB
- Accuracy: ~92% (better for accents/noise)
- Speed: 10min audio → 4-6min processing
- RAM usage: ~1.5GB per worker

**Recommended:**
- Start with small model for testing
- Upgrade to large model if accuracy is insufficient
- Use 2-3 parallel workers max (avoid RAM exhaustion)

---

## 🔗 Integration with Knowledge Management

### Workflow: Audio → Transcript → Zettelkasten

**Step 1: Batch Transcribe**
```bash
# Transcribe all sermons
transcribe ~/Downloads/sermons/*.mp3 --output ~/Documents/Local\ Vault/Inbox/
```

**Step 2: Process Weekly (Manual Review)**
```
Inbox/
├── sermon_2025_11_03.md
├── sermon_2025_11_10.md
└── lecture_audio.md
```

**Step 3: Extract Ideas → Literature Notes**
- Read transcripts in Inbox/
- Extract key ideas
- Create literature notes in Resources/Notes/literature/
- Link to permanent notes (zettels)

**Step 4: Archive Original**
```bash
# Move processed transcripts
mv Inbox/sermon_*.md Archive/transcripts/2025/
```

---

## 📁 File Naming Convention

**Input files:** (any format)
```
sermon_2025_11_10.mp3
interview_john_doe_2025_11_11.mp3
voice_note_20251111_143022.mp3
```

**Output files:** (markdown)
```
sermon_2025_11_10.md
interview_john_doe_2025_11_11.md
voice_note_20251111_143022.md
```

**Naming pattern:** `{description}_{YYYY_MM_DD}.md`
- Lowercase with underscores
- ISO date format
- Descriptive prefix

---

## ✨ Future Enhancements (Optional)

### Phase 4: Advanced Features (Post-MVP)
- Speaker diarization (who said what)
- Timestamp markers every N minutes
- Auto-punctuation improvements
- Custom vocabulary (names, technical terms)
- GUI wrapper (if needed)

### Integration Ideas
- Obsidian plugin for in-app transcription
- Hotkey to transcribe voice notes
- Auto-tag based on content analysis
- Summary generation (using Claude API)

---

## 🐛 Troubleshooting

### "ffmpeg not found"
```bash
brew install ffmpeg
# Verify: ffmpeg -version
```

### "No module named 'vosk'"
```bash
# Ensure virtual environment is activated
source venv/bin/activate
pip install vosk
```

### "Model not found"
```bash
# Check model path
ls ~/.cache/vosk-model-small-en-us-0.15/

# Re-download if missing
curl -LO https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip -d ~/.cache/
```

### "Out of memory" during batch processing
```bash
# Reduce parallel workers
transcribe folder/ --workers 1
```

### Low accuracy
1. Try large model (vosk-model-en-us-0.22)
2. Ensure audio quality is good (clear speech, minimal background noise)
3. Convert to 16kHz mono WAV before transcription
4. Consider manual review for critical content

---

## 📚 Resources

**Vosk Documentation:**
- Official site: https://alphacephei.com/vosk/
- Models: https://alphacephei.com/vosk/models
- Python API: https://github.com/alphacep/vosk-api/tree/master/python

**Related Project Docs:**
- vosk_lightweight_bulk_processor_project_overview.md (complete code examples)
- batch_whispersync_transcriber_project_overview.md (alternative approach)
- mp3_txt_ project_overview.md (general overview)

**Knowledge Management Integration:**
- KNOWLEDGE-MANAGEMENT-FRAMEWORK.md (capture → process workflow)
- VAULT-STRUCTURE-FRAMEWORK.md (where files go)

---

## 🎯 Success Criteria

**MVP (Week 1):**
- ✅ Transcribe single MP3 file to text
- ✅ Output as .txt or .md
- ✅ Basic error handling
- ✅ Progress indicator

**Full Implementation (Week 2):**
- ✅ Batch process folder of files
- ✅ Parallel processing (2-3 workers)
- ✅ Markdown output with metadata
- ✅ Skip already-processed files
- ✅ Summary report
- ✅ Integration with Inbox workflow

---

## 📝 Next Steps

1. ✅ Review this PROJECT-OVERVIEW.md
2. ⏳ Run setup.sh to install dependencies
3. ⏳ Test with single audio file
4. ⏳ Implement basic CLI (transcribe_vosk.py)
5. ⏳ Test batch processing
6. ⏳ Refine output format for Zettelkasten
7. ⏳ Document usage in README.md

---

**Project Status:** Ready to begin implementation
**Estimated Completion:** 2025-11-25 (2 weeks)
**Primary Reference:** vosk_lightweight_bulk_processor_project_overview.md

#project #audio #transcription #vosk #knowledge-management
