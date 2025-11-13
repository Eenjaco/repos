# Strudel Sheet Music Converter

An intelligent app that transforms both PDF sheet music and audio recordings into playable Strudel (TidalCycles) code, bridging traditional music notation and recorded audio with live coding.

## Overview

This application enables musicians and live coders to:
- **From Sheet Music**: Scan PDF sheet music using Optical Music Recognition (OMR)
- **From Audio**: Analyze audio recordings to extract musical features (NEW!)
- Convert notation or audio to MIDI format
- Generate Strudel/TidalCycles code snippets
- Map different instrumental parts to specific sounds
- Apply historical tuning systems (Werkmeister temperaments)
- Play converted music through Strudel's live coding environment

## Project Structure

```
strudel_sheetmusic/
├── src/
│   ├── omr/          # Optical Music Recognition processing
│   ├── audio/        # Audio analysis (BPM, key, chords, melody) [NEW!]
│   ├── midi/         # MIDI conversion and processing
│   ├── strudel/      # Strudel code generation
│   ├── mapping/      # Instrument-to-sound mapping
│   └── tuning/       # Werkmeister tuning system implementations
├── samples/          # Training and test data
│   ├── audio/        # Audio recordings for analysis [NEW!]
│   ├── organ/        # Organ sheet music (multi-staff, complex)
│   ├── guitar/       # Guitar tablature and notation
│   ├── voice/        # Vocal scores
│   ├── drums/        # Percussion notation
│   └── bass/         # Bass notation
├── docs/             # Documentation and guides
├── config/           # Configuration files
└── tests/            # Test suite
```

## Workflows

### Sheet Music → Strudel (PDF Input)
1. **PDF Input** → Upload sheet music PDF
2. **OMR Processing** → Scan and recognize musical notation
3. **MIDI Conversion** → Convert recognized notes to MIDI format
4. **Instrument Mapping** → User selects which parts map to which sounds
5. **Tuning Application** → Apply Werkmeister or other temperaments
6. **Code Generation** → Generate Strudel code snippets
7. **Playback** → Execute in Strudel environment

### Audio → Strudel (Recording Input) [NEW!]
1. **Audio Input** → Upload audio recording (MP3, WAV, etc.)
2. **Audio Analysis** → Extract BPM, key, chords, melody
3. **MIDI Conversion** → Convert detected notes to MIDI
4. **Tuning Application** → Apply temperaments (optional)
5. **Code Generation** → Generate Strudel code snippets
6. **Playback** → Execute in Strudel environment

## Key Features

### Optical Music Recognition (OMR)
- PDF scanning and image processing
- Staff line detection and removal
- Note head, stem, and beam recognition
- Clef, key signature, and time signature detection
- Rest and articulation marking recognition
- Multi-staff system handling (essential for organ music)

### MIDI Conversion
- Accurate timing and duration conversion
- Polyphonic note handling
- Dynamics and expression mapping
- Multi-track support for different instruments

### Strudel Code Generation
- Pattern-based code generation
- Note sequence to Strudel pattern syntax
- Rhythm and timing translation
- Effect and articulation mapping

### Instrument Mapping Interface
- Visual score display with selectable regions
- Assign staff lines/tracks to instruments
- Customizable sound library integration
- Preview individual instrument parts

### Tuning Systems (Werkmeister)
- Historical temperament implementations
- Werkmeister I-VI temperaments
- Equal temperament baseline
- Custom tuning definition support
- Per-instrument tuning configuration

### Audio Analysis [NEW!]
- **BPM Detection** - Automatic tempo detection from recordings
- **Key Detection** - Musical key identification (e.g., C major, A minor)
- **Chord Detection** - Chord progression analysis over time
- **Melody Extraction** - Main melody converted to MIDI notes
- **Beat Tracking** - Precise beat position detection
- **Pitch Detection** - Frequency-to-MIDI conversion for monophonic audio

## Technologies

- **OMR Engine**: TBD (Audiveris, MuseScore's OMR, or custom solution)
- **Audio Analysis**: `librosa` (core), `CREPE` (pitch), `basic-pitch` (audio-to-MIDI)
- **MIDI Processing**: Python `mido` or similar
- **PDF Processing**: `pdf2image`, `Pillow` for image manipulation
- **Strudel**: Integration with Strudel REPL/API
- **Frontend**: TBD (web-based interface recommended)

## Training Data

The `samples/organ/` directory is ideal for initial training because:
- Multiple staves (typically 3: right hand, left hand, pedals)
- Complex polyphonic notation
- Rich harmonic content
- Diverse rhythmic patterns
- Clear notation standards

## Development Phases

### Phase 1: Foundation
- [ ] Set up development environment
- [ ] Research and select OMR library
- [ ] Implement basic PDF to image conversion
- [ ] Create simple note recognition proof-of-concept

### Phase 2: Core Pipeline
- [ ] Build complete OMR processing pipeline
- [ ] Implement MIDI conversion
- [ ] Create basic Strudel code generator
- [ ] Develop simple command-line interface

### Phase 3: Advanced Features
- [ ] Build instrument mapping interface
- [ ] Implement Werkmeister tuning systems
- [ ] Add multi-instrument support
- [ ] Create web-based UI

### Phase 4: Refinement
- [ ] Training on organ music samples
- [ ] Accuracy improvements
- [ ] Performance optimization
- [ ] Documentation and examples

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js (for Strudel integration - optional)
- Strudel environment (for playback)

### Installation
```bash
# Clone and navigate to project
cd strudel_sheetmusic

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install core dependencies
pip install -r requirements.txt

# Install audio analysis dependencies (optional)
pip install -r requirements_audio.txt
```

### Usage
```bash
# Tuning system demos (working now!)
python cli.py show-tuning werkmeister1
python cli.py compare-tunings C#4

# Audio analysis (NEW! - requires librosa)
python cli.py analyze-audio song.mp3
python cli.py analyze-audio song.mp3 --detect-chords --extract-melody --show-beats

# PDF processing
python cli.py pdf-to-images sheet_music.pdf -o output/

# Run all examples
python examples/quickstart.py
```

## Contributing

This is an experimental project. Documentation and contribution guidelines will evolve as the project develops.

## License

TBD

## Use Cases

### 1. Learn Songs by Ear
- Upload an MP3 of your favorite song
- Extract melody, chords, and rhythm automatically
- Get Strudel code to recreate and modify sections
- Perfect for musicians learning by ear

### 2. Sheet Music to Live Coding
- Upload PDF of classical sheet music (Bach, Beethoven, etc.)
- Get playable Strudel code with authentic historical tunings
- Remix classical pieces with modern electronic elements
- Ideal for organ music with Werkmeister temperaments

### 3. Music Education
- Analyze songs to understand chord progressions
- Study melody construction and harmony
- Interactive demonstrations of music theory concepts
- Compare different tuning systems side-by-side

### 4. Live Performance Tool
- Prepare classical or recorded material for live coding sets
- Quick transcription of melodic ideas
- Build a library of patterns from various sources
- Integrate traditional and electronic music seamlessly

## Notes

- Organ music provides excellent training data due to its complexity
- Werkmeister temperaments are historically important for baroque organ music
- Strudel's pattern-based syntax aligns well with musical phrase structures
- Audio analysis enables "learning by ear" workflows
- Both PDF and audio inputs lead to the same MIDI → Strudel pipeline

## Future Possibilities

- Real-time sheet music following during live coding
- Collaborative annotation of sheet music for better OMR training
- Integration with other live coding environments (SuperCollider, Sonic Pi)
- Mobile app for quick scanning and conversion
- Cloud-based processing for complex scores
- Source separation (vocals, drums, bass, other) before analysis
- Real-time audio analysis for live performance
- Browser-based audio analysis using TensorFlow.js
- Collaborative pattern sharing and remixing community
