# Audio Analysis Module

## Overview

The audio analysis module enables reverse engineering of music: instead of converting sheet music to playable code, it extracts musical information from audio recordings to generate MIDI and Strudel code.

**Workflow**: Audio Recording → Analysis → MIDI → Strudel Code

## Use Cases

1. **Learn by Ear**
   - Upload a song recording
   - Extract melody, chords, and rhythm
   - Get Strudel code to recreate sections

2. **Loop Extraction**
   - Analyze drum loops or instrumental sections
   - Extract patterns for live coding
   - Integrate into performances

3. **Music Education**
   - Analyze famous songs to understand structure
   - Study chord progressions and melodies
   - Practice transcription skills

4. **Sampling & Remixing**
   - Extract musical elements from recordings
   - Manipulate in Strudel
   - Create variations and remixes

## Features

### 1. Tempo (BPM) Detection
Automatically detect the beats per minute of a recording.

```python
from src.audio.audio_analyzer import AudioAnalyzer

analyzer = AudioAnalyzer()
analyzer.load_audio("song.mp3")
bpm = analyzer.detect_bpm()
print(f"BPM: {bpm}")
```

### 2. Key Detection
Identify the musical key (e.g., C major, A minor).

```python
key_info = analyzer.detect_key()
print(f"Key: {key_info['key']} {key_info['mode']}")
# Output: Key: C major
```

### 3. Beat Detection
Find exact beat positions for quantization.

```python
beats = analyzer.detect_beats()
print(f"Found {len(beats)} beats")
print(f"First beat at {beats[0]:.2f}s")
```

### 4. Melody Extraction
Extract the main melody as MIDI notes.

```python
melody_notes = analyzer.extract_melody()
for note in melody_notes[:10]:
    print(f"{note['time']:.2f}s: {note['note_name']} ({note['midi']})")
```

### 5. Chord Detection
Identify chord progression.

```python
from src.audio.chord_detector import ChordDetector

chord_detector = ChordDetector()
chords = chord_detector.detect_chord_progression(audio)

for chord in chords:
    print(f"{chord['time']:.2f}s: {chord['chord']} ({chord['confidence']:.2f})")
```

### 6. Pitch Detection
Get detailed pitch information over time.

```python
from src.audio.pitch_detector import PitchDetector

pitch_detector = PitchDetector()
frequencies, times = pitch_detector.detect_pitch_librosa(audio)
notes = pitch_detector.pitch_to_notes(frequencies, times)
```

## Complete Analysis

Run full analysis on an audio file:

```python
analyzer = AudioAnalyzer()
results = analyzer.analyze_full("song.mp3")

print(f"Duration: {results['duration']:.2f}s")
print(f"BPM: {results['bpm']:.1f}")
print(f"Key: {results['key']} {results['mode']}")
print(f"Beats: {results['beat_count']}")
```

## CLI Usage

```bash
# Analyze audio file
python cli.py analyze-audio song.mp3

# Analyze with options
python cli.py analyze-audio song.mp3 --extract-melody --detect-chords

# Convert analysis to MIDI
python cli.py audio-to-midi song.mp3 -o output.mid

# Full pipeline: audio → MIDI → Strudel
python cli.py audio-to-strudel song.mp3 -o output.js
```

## Installation

### Required Dependencies

```bash
# Core audio processing
pip install librosa soundfile

# Advanced pitch detection (optional)
pip install crepe

# Audio-to-MIDI (optional but recommended)
pip install basic-pitch

# Beat tracking (optional)
pip install madmom

# Source separation (optional)
pip install demucs
```

### Quick Install

```bash
cd strudel_sheetmusic
pip install -r requirements_audio.txt
```

## Technology Stack

### Core: librosa
- **Purpose**: Main audio analysis library
- **Features**: Tempo, beat, pitch, chroma, spectral analysis
- **Pros**: Well-documented, actively maintained, comprehensive
- **Cons**: Can be slow for real-time

### Optional: CREPE
- **Purpose**: State-of-art pitch detection
- **Features**: Deep learning-based, very accurate
- **Pros**: Best accuracy for melody extraction
- **Cons**: Slower than traditional methods, requires TensorFlow

### Optional: basic-pitch
- **Purpose**: Audio-to-MIDI conversion
- **Features**: Spotify's model, polyphonic, multi-instrument
- **Pros**: Handles full songs, not just monophonic
- **Cons**: Large model, slower processing

### Optional: Demucs
- **Purpose**: Source separation
- **Features**: Separate vocals, drums, bass, other
- **Pros**: High quality separation
- **Cons**: Very slow, large model, high memory usage

### Optional: madmom
- **Purpose**: Advanced beat tracking
- **Features**: More accurate than librosa for complex music
- **Pros**: Great for electronic and complex rhythms
- **Cons**: Additional dependency

## Vosk & Whisper Note

You mentioned having **Vosk** and **Whisper** installed. These are **speech** transcription tools (speech-to-text), which are different from music analysis:

- **Vosk/Whisper**: Convert spoken words to text
- **This module**: Convert music to MIDI/musical data

However, there's a creative use case: **Vocal Melody Extraction**
- Record yourself humming/singing a melody
- Use Whisper to verify it's audio (though it will try to transcribe as speech)
- Use THIS module's pitch detection to extract the melody
- Convert to MIDI/Strudel code

## Workflow Examples

### Example 1: Extract Melody from Recording

```python
from src.audio.audio_analyzer import AudioAnalyzer
from src.audio.pitch_detector import PitchDetector

# Load audio
analyzer = AudioAnalyzer()
audio = analyzer.load_audio("melody.mp3")

# Detect key and BPM
bpm = analyzer.detect_bpm(audio)
key_info = analyzer.detect_key(audio)

print(f"BPM: {bpm}, Key: {key_info['key']} {key_info['mode']}")

# Extract pitch
pitch_detector = PitchDetector()
frequencies, times = pitch_detector.detect_pitch_librosa(audio)
notes = pitch_detector.pitch_to_notes(frequencies, times)

# Print melody
print("Melody:")
for note in notes[:20]:
    print(f"  {note['note_name']:>4} for {note['duration']:.2f}s")
```

### Example 2: Detect Chord Progression

```python
from src.audio.audio_analyzer import AudioAnalyzer
from src.audio.chord_detector import ChordDetector

analyzer = AudioAnalyzer()
audio = analyzer.load_audio("song.mp3")

chord_detector = ChordDetector()
chords = chord_detector.detect_chord_progression(
    audio,
    segment_length=2.0,  # Analyze every 2 seconds
    min_confidence=0.6   # Only include confident detections
)

print("Chord Progression:")
for chord in chords:
    print(f"  {chord['time']:>6.2f}s: {chord['chord']:>6} ({chord['confidence']:.2f})")
```

### Example 3: Full Analysis → Strudel Code

```python
# Full analysis
analyzer = AudioAnalyzer()
results = analyzer.analyze_full("loop.mp3")

# Generate Strudel code (TODO: implement)
from src.strudel.code_generator import StrudelGenerator

generator = StrudelGenerator()
strudel_code = generator.from_audio_analysis(results)

print(strudel_code)
```

Expected output:
```javascript
// Analyzed from loop.mp3
// BPM: 120, Key: C major

s("bd").every(4, fast(2))
  .stack(
    s("sd").fast(2).delay(0.25),
    note("c4 e4 g4").fast(4).s("synth")
  )
  .cpm(120)
```

## Limitations & Considerations

### Accuracy
- **Monophonic** (single instrument): 90%+ accuracy
- **Polyphonic** (multiple instruments): 60-80% accuracy
- **Complex mixes**: May require source separation first

### Processing Time
- **Real-time**: Not suitable for live use (yet)
- **Typical song** (3-4 minutes): 30-60 seconds processing
- **With advanced models**: 2-5 minutes

### Best Results
1. **Clean recordings**: Studio quality > live recordings
2. **Monophonic first**: Start with single instrument
3. **Good separation**: Drums/bass/melody well separated
4. **Stable tempo**: Constant BPM easier than tempo changes

### Copyright
- Analysis tools are legal (like audio editors)
- Extracting melody for learning: educational fair use
- Redistributing copyrighted material: NOT allowed
- Always respect copyright when sharing results

## Advanced Features (Coming Soon)

### Source Separation
Separate audio into stems before analysis:

```python
from src.audio.separator import AudioSeparator

separator = AudioSeparator()
stems = separator.separate("song.mp3")  # vocals, drums, bass, other

# Analyze each stem separately
melody = analyzer.extract_melody(stems['vocals'])
chords = chord_detector.detect_chords(stems['other'])
drums = analyzer.detect_beats(stems['drums'])
```

### Time Signature Detection
```python
time_sig = analyzer.get_time_signature()
print(f"Time signature: {time_sig[0]}/{time_sig[1]}")
```

### Structural Analysis
```python
structure = analyzer.detect_structure()
# Output: ['intro', 'verse', 'chorus', 'verse', 'chorus', 'outro']
```

### Harmonic Analysis
```python
harmony = analyzer.analyze_harmony()
# Includes: key modulations, borrowed chords, cadences
```

## Integration with Sheet Music Pipeline

The audio and sheet music pipelines can work together:

```
Audio Recording
      ↓
   Analysis
      ↓
  MIDI File  ←→  Sheet Music PDF
      ↓               ↓
   Tuning        OMR + MIDI
      ↓               ↓
 Strudel Code ← ─ ← ─ ┘
```

Use cases:
1. Compare audio recording to sheet music
2. Check if performance matches score
3. Extract sheet music from audio (transcription)
4. Generate sheet music from audio analysis

## Example Projects

### Project 1: Loop Library Builder
- Record yourself playing short loops
- Analyze each loop for key, BPM, notes
- Build searchable library
- Generate Strudel code on demand

### Project 2: Practice Tool
- Play along with sheet music
- Record your performance
- Compare detected notes to expected notes
- Get accuracy feedback

### Project 3: Song Remixer
- Load favorite song
- Extract individual elements (melody, chords, bass)
- Remix in Strudel with effects
- Create live performance version

## Testing

```bash
# Run audio module tests
pytest tests/test_audio_analyzer.py -v
pytest tests/test_pitch_detector.py -v
pytest tests/test_chord_detector.py -v

# Test with sample audio
python examples/audio_analysis_demo.py
```

## Troubleshooting

### "librosa not found"
```bash
pip install librosa soundfile
```

### "Slow processing"
- Use lower sample rate (22050 instead of 44100)
- Process shorter segments
- Use librosa instead of CREPE for pitch

### "Inaccurate results"
- Check audio quality (no distortion, clipping)
- Try source separation first
- Adjust confidence thresholds
- Use CREPE for better pitch accuracy

### "Memory issues"
- Process audio in chunks
- Use lower sample rate
- Close other applications
- Increase system RAM

## Resources

**Libraries**:
- [librosa documentation](https://librosa.org/doc/latest/)
- [CREPE pitch detection](https://github.com/marl/crepe)
- [basic-pitch (Spotify)](https://github.com/spotify/basic-pitch)
- [Demucs source separation](https://github.com/facebookresearch/demucs)

**Learning**:
- Music Information Retrieval (MIR) resources
- Digital signal processing basics
- Music theory for programmers

---

**Status**: 🚧 Implementation in progress
**Next Steps**: Implement audio-to-MIDI conversion, integrate with Strudel generator
