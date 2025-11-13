# Strudel Sheet Music Converter - Quick Start

## What is this?

Transform **sheet music PDFs** and **audio recordings** into playable **Strudel code** for live coding.

Two workflows:
- 📄 **PDF → Strudel**: Scan sheet music, get code
- 🎵 **Audio → Strudel**: Analyze songs, extract patterns

## Installation

```bash
# Navigate to project
cd strudel_sheetmusic

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# For audio analysis
pip install -r requirements_audio.txt
```

## Try It Now!

### 1. Tuning Systems (Works immediately!)

```bash
# Show Werkmeister I temperament
python cli.py show-tuning werkmeister1

# Compare all tunings for a specific note
python cli.py compare-tunings C#4

# Show MIDI pitch bend values
python cli.py show-tuning werkmeister1 --show-bend
```

**Example output:**
```
Werkmeister I(III) (base=440.0Hz)
Base frequency: 440.0 Hz (A4)

Frequency Table (Octave 4):
----------------------------------------
  C4:  261.63 Hz  ( 0.0 cents)
 C#4:  277.18 Hz  (-10.0 cents)
  D4:  293.66 Hz  (-8.0 cents)
...
```

### 2. Audio Analysis (Requires librosa)

```bash
# Basic analysis: BPM, key, beat detection
python cli.py analyze-audio song.mp3

# Full analysis with chords and melody
python cli.py analyze-audio song.mp3 --detect-chords --extract-melody --show-beats
```

**Example output:**
```
📁 File: song.mp3
⏱️  Duration: 180.45s
🎵 BPM: 120.3
🎹 Key: C major
🥁 Beats detected: 361

🎸 Detecting chords...
Found 24 chord changes:
    0.00s:     Cmaj (0.82)
    8.12s:      Am7 (0.75)
   16.24s:     Fmaj (0.78)
   24.36s:     G7 (0.81)
...
```

### 3. Run All Examples

```bash
python examples/quickstart.py
```

This demonstrates:
- Tuning system calculations
- Frequency tables
- Pitch bend values
- Project architecture

## What's Working Right Now?

✅ **Tuning Systems**
- Werkmeister I, II, III temperaments
- Equal temperament
- Frequency calculations
- MIDI pitch bend generation
- Full test suite

✅ **Audio Analysis**
- BPM detection
- Key detection
- Beat tracking
- Chord progression detection
- Pitch detection framework
- Melody extraction (requires basic-pitch)

✅ **CLI Tools**
- Tuning comparison
- Audio analysis
- PDF to images (requires poppler)

## What's Coming Next?

🚧 **In Development:**
- OMR (Optical Music Recognition) for PDFs
- MusicXML to MIDI conversion
- Strudel code generation
- Web interface

## Common Commands

```bash
# Audio: Analyze a song
python cli.py analyze-audio recording.mp3 --detect-chords

# Tuning: Compare systems
python cli.py compare-tunings F#5

# PDF: Convert to images (when you have PDFs)
python cli.py pdf-to-images sheet.pdf -o output/

# Help
python cli.py --help
python cli.py analyze-audio --help
```

## Project Structure

```
strudel_sheetmusic/
├── cli.py              ← Start here! Command-line interface
├── examples/           ← Demo scripts
│   └── quickstart.py
├── src/
│   ├── audio/         ← Audio analysis (NEW!)
│   ├── tuning/        ← Werkmeister temperaments (WORKING!)
│   ├── omr/           ← PDF processing (TODO)
│   ├── midi/          ← MIDI conversion (TODO)
│   └── strudel/       ← Code generation (TODO)
├── samples/
│   ├── audio/         ← Put MP3/WAV files here
│   └── organ/         ← Put PDF sheet music here
├── docs/
│   ├── AUDIO_ANALYSIS.md  ← Audio feature docs
│   ├── ARCHITECTURE.md    ← Technical details
│   └── PROJECT_PITCH.md   ← Full vision
└── config/            ← Tuning and instrument configs
```

## Example Workflows

### Workflow 1: Analyze a Song

```bash
# 1. Have an MP3 file
ls song.mp3

# 2. Analyze it
python cli.py analyze-audio song.mp3 --detect-chords --extract-melody

# 3. Results show: BPM, key, chords, melody
# 4. (Coming soon) Generate Strudel code automatically
```

### Workflow 2: Compare Tunings

```bash
# See how different temperaments affect a note
python cli.py compare-tunings C4

# Output shows frequency differences between:
# - Equal Temperament
# - Werkmeister I, II, III
```

### Workflow 3: Process Sheet Music

```bash
# 1. Have a PDF of sheet music
# 2. Convert to images
python cli.py pdf-to-images bach_fugue.pdf -o output/

# 3. (Coming soon) Run OMR to extract notes
# 4. (Coming soon) Generate Strudel code
```

## Troubleshooting

### "librosa not found"
```bash
pip install -r requirements_audio.txt
```

### "poppler not found" (for PDFs)
```bash
# Ubuntu/Debian
sudo apt-get install poppler-utils

# macOS
brew install poppler
```

### "No module named 'src'"
```bash
# Make sure you're in the strudel_sheetmusic directory
pwd  # Should end with strudel_sheetmusic
```

## Learn More

- **docs/AUDIO_ANALYSIS.md** - Detailed audio feature docs
- **docs/ARCHITECTURE.md** - Technical architecture
- **docs/PROJECT_PITCH.md** - Full project vision
- **docs/GETTING_STARTED.md** - Development guide

## What Makes This Special?

1. **Dual Input**: Both PDFs and audio files
2. **Historical Tunings**: Authentic Werkmeister temperaments for baroque music
3. **Live Coding Bridge**: Connect traditional music to Strudel
4. **Open Source**: Free to use and modify

## Next Steps

1. **Try the demos** - Run `python examples/quickstart.py`
2. **Analyze audio** - Try `analyze-audio` with your MP3s
3. **Add samples** - Place sheet music in `samples/organ/`
4. **Read docs** - Check out `docs/` for details
5. **Star the repo** - Help others discover it!

---

## Quick Tips

- Start with audio analysis if you have MP3s
- Use organ music PDFs for best OMR results (when implemented)
- Werkmeister I is best all-around baroque tuning
- librosa installation can take a few minutes (be patient!)

**Have fun bridging traditional and electronic music! 🎵**
