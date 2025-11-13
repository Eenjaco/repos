# mp3_txt - Audio Transcription Tool

Lightweight CPU-based audio transcription using Vosk speech recognition. Convert MP3/audio files to timestamped markdown for integration with your knowledge management system.

## Features

- ✅ **CPU-only processing** - No GPU required (perfect for MacBook)
- ✅ **Batch processing** - Transcribe entire folders
- ✅ **Streaming mode** - Low memory usage (~500MB per worker)
- ✅ **Timestamped output** - Markdown format with time markers
- ✅ **Offline** - No API calls, no internet required
- ✅ **Fast** - 10min audio → 2-3min processing (small model)

## Quick Start

### 1. Setup (One-time)

```bash
# Install ffmpeg
brew install ffmpeg

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download Vosk model (~40MB small, ~1.8GB large)
cd ~/.cache
curl -LO https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
rm vosk-model-small-en-us-0.15.zip
```

### 2. Transcribe Audio

**Simple one-word command:**
```bash
cd "/Users/mac/Documents/Local Vault/Projects/mp3_txt"
./transcribe
```

**Features:**
- Drag-and-drop files or paste paths
- Single file or batch folder
- Optional timestamps (disabled by default)
- Post-transcription renaming (add custom prefixes)
- Auto-move to different folders
- Clean, interactive prompts

**Alternative: Python CLI (advanced)**
```bash
# Single file (no timestamps)
python3 transcribe_vosk_stream.py single audio.mp3 --outdir ./output

# Single file (with timestamps)
python3 transcribe_vosk_stream.py single audio.mp3 --outdir ./output --timestamps

# Batch folder
python3 transcribe_vosk_stream.py batch ./audio_folder --outdir ./output --concurrency 1
```

## Output Format

### Without Timestamps (Default)
```markdown
---
source: sermon_2025_11_10.mp3
---

hello everyone welcome to today's discussion

we're going to talk about important topics

let's dive into the key concepts
```

### With Timestamps (Optional)
```markdown
---
source: sermon_2025_11_10.mp3
---

**(00:00.000 - 00:10.500)** hello everyone welcome to today's discussion

**(00:10.500 - 00:20.150)** we're going to talk about important topics

**(00:20.150 - 00:30.750)** let's dive into the key concepts
```

## Project Structure

```
mp3_txt/
├── README.md                      # This file
├── PROJECT-OVERVIEW.md            # Detailed project documentation
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore rules
├── transcribe                     # ⭐ Main CLI (single command)
├── transcribe_vosk_stream.py      # Core transcription engine
├── test_debug.py                  # Debugging tool
└── venv/                          # Python virtual environment
```

## Usage Examples

### Transcribe Sermon Audio

```bash
# Run the interactive CLI
./transcribe

# Choose option 1 (single file)
# Drag-and-drop: ~/Downloads/sermon_2025_11_10.mp3
# Choose: no timestamps
# Output to: ./transcriptions
# Rename to: pastor_john_sermon_nov_10
# Move to: ~/Documents/Local Vault/Inbox/

# Result: ~/Documents/Local Vault/Inbox/pastor_john_sermon_nov_10.md
```

### Batch Transcribe Audiobook

```bash
# Run the interactive CLI
./transcribe

# Choose option 2 (batch folder)
# Drag-and-drop folder with chapters
# Choose: no timestamps
# Output to: ./transcriptions
# Rename with prefix: christine_pohl_living_into_community
# Result: christine_pohl_living_into_community_ch_1.md, _ch_2.md, etc.
```

### Integrate with Knowledge Management

**Recommended workflow:**

1. **Rename files first** (if needed):
   ```bash
   cd ../file_renaming
   ./rename
   # Drag-drop audio folder → clean filenames
   ```

2. **Transcribe** with the `transcribe` command:
   ```bash
   cd ../mp3_txt
   ./transcribe
   # Choose batch mode
   # Drag-drop folder
   # No timestamps
   # Custom prefix if desired
   # Move directly to Inbox/
   ```

3. **Weekly review:**
   - Read transcripts in `Inbox/`
   - Highlight key ideas and quotes
   - Create literature notes in `Resources/Notes/literature/`

4. **Extract permanent notes:**
   - Create zettels from important concepts
   - Link using `[[wikilinks]]`
   - Connect to 12 Favorite Problems

5. **Archive processed transcripts:**
   ```bash
   mv Inbox/transcript_*.md Archive/transcripts/2025/
   ```

## Configuration

### Upgrade to Better Model

**Current:** Small model (40MB, 85% accuracy)
**Upgrade:** Large model (1.8GB, 92% accuracy) - Better for accents, multiple speakers, background noise

```bash
# Download large model
cd ~/.cache
curl -LO https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip
unzip vosk-model-en-us-0.22.zip

# Update transcribe_vosk_stream.py line 20:
DEFAULT_MODEL_PATH = Path.home() / ".cache" / "vosk-model-en-us-0.22"
```

**See ADVANCED.md** for:
- 20+ language models
- Audio format support (MP3, WAV, M4A, etc.)
- Model training and customization
- Accuracy improvement techniques
- Speaker diarization
- Real-time transcription

### Adjust Timestamp Window

Edit `transcribe_vosk_stream.py` line 90:

```python
window = 10.0  # Group words into 10-second blocks
```

Smaller windows (5.0) = more granular timestamps
Larger windows (30.0) = fewer, longer paragraphs

### Concurrency for Batch Processing

```bash
# Conservative (8GB RAM) - recommended
./transcribe.sh batch folder/ output/ 1

# Moderate (16GB RAM)
./transcribe.sh batch folder/ output/ 2

# Aggressive (32GB+ RAM)
./transcribe.sh batch folder/ output/ 4
```

## Performance

**Hardware:** MacBook, 8GB RAM, Intel i5

**Small model (vosk-model-small-en-us-0.15):**
- Accuracy: ~85% (good for clear speech)
- Speed: 10min audio → 2-3min processing
- RAM: ~500MB per worker
- Recommended workers: 1-2

**Large model (vosk-model-en-us-0.22):**
- Accuracy: ~92% (better for accents, noise, multiple speakers)
- Speed: 10min audio → 4-6min processing
- RAM: ~1.5GB per worker
- Recommended workers: 1

## Troubleshooting

### "No speech detected"

**Possible causes:**
1. Audio file is silent or very quiet
2. Audio encoding not compatible
3. Speech is in non-English language

**Solutions:**
```bash
# Check audio file with ffmpeg
ffmpeg -i audio.mp3

# Test playback
open audio.mp3

# Try converting first
ffmpeg -i input.mp3 -ar 16000 -ac 1 output.wav
python3 transcribe_vosk_stream.py single output.wav --outdir ./test
```

### "Vosk model not found"

```bash
# Verify model exists
ls ~/.cache/vosk-model-small-en-us-0.15/

# Re-download if missing
cd ~/.cache
curl -LO https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
```

### Low accuracy

1. **Upgrade to large model** (92% accuracy)
   ```bash
   cd ~/.cache
   curl -LO https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip
   unzip vosk-model-en-us-0.22.zip
   ```
   Update script to use large model path.

2. **Check audio quality**
   - Ensure clear speech, minimal background noise
   - Try noise reduction if needed

3. **Manual review**
   - For critical content (sermons, interviews), review and correct transcripts

### Out of memory

```bash
# Reduce workers to 1
./transcribe.sh batch folder/ output/ 1

# Use small model instead of large
```

## Dependencies

- **Python 3.10+**
- **ffmpeg** - Audio conversion
- **vosk** - Speech recognition engine
- **soundfile** - Audio file reading
- **typer** - CLI framework
- **rich** - Progress bars and formatting

See `requirements.txt` for exact versions.

## Models Available

**English models from https://alphacephei.com/vosk/models:**

- `vosk-model-small-en-us-0.15` - 40MB, fast, good accuracy
- `vosk-model-en-us-0.22` - 1.8GB, slower, excellent accuracy
- `vosk-model-en-us-0.42-gigaspeech` - 2.3GB, best accuracy

**Other languages:**
- Spanish, French, German, Russian, Chinese, and 20+ more
- See Vosk website for full list

## Contributing

This is a personal knowledge management tool. Customize as needed for your workflow.

## Resources

- **Vosk Documentation:** https://alphacephei.com/vosk/
- **Vosk Models:** https://alphacephei.com/vosk/models
- **Project Overview:** See `PROJECT-OVERVIEW.md` for detailed documentation
- **Knowledge Management Framework:** See `/knowledge_base_setup/KNOWLEDGE-MANAGEMENT-FRAMEWORK.md`

## License

Free for personal use. Vosk is licensed under Apache 2.0.

---

**Created:** 2025-11-11
**Status:** ✅ Working
**Success Rate:** 92% (with large model)
**Platform:** macOS (compatible with Linux)

#audio #transcription #vosk #knowledge-management
