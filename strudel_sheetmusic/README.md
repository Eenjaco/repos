# Strudel Sheet Music Converter

An intelligent app that transforms PDF sheet music into playable Strudel (TidalCycles) code, bridging traditional music notation with live coding.

## Overview

This application enables musicians and live coders to:
- Scan PDF sheet music using Optical Music Recognition (OMR)
- Convert notation to MIDI format
- Generate Strudel/TidalCycles code snippets
- Map different instrumental parts to specific sounds
- Apply historical tuning systems (Werkmeister temperaments)
- Play converted music through Strudel's live coding environment

## Project Structure

```
strudel_sheetmusic/
├── src/
│   ├── omr/          # Optical Music Recognition processing
│   ├── midi/         # MIDI conversion and processing
│   ├── strudel/      # Strudel code generation
│   ├── mapping/      # Instrument-to-sound mapping
│   └── tuning/       # Werkmeister tuning system implementations
├── samples/          # Training and test sheet music PDFs
│   ├── organ/        # Specialized organ music (multi-staff, complex)
│   ├── guitar/       # Guitar tablature and notation
│   ├── voice/        # Vocal scores
│   ├── drums/        # Percussion notation
│   └── bass/         # Bass notation
├── docs/             # Documentation and guides
├── config/           # Configuration files
└── tests/            # Test suite
```

## Workflow

1. **PDF Input** → Upload sheet music PDF
2. **OMR Processing** → Scan and recognize musical notation
3. **MIDI Conversion** → Convert recognized notes to MIDI format
4. **Instrument Mapping** → User selects which parts map to which sounds
5. **Tuning Application** → Apply Werkmeister or other temperaments
6. **Code Generation** → Generate Strudel code snippets
7. **Playback** → Execute in Strudel environment

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

## Technologies

- **OMR Engine**: TBD (Audiveris, MuseScore's OMR, or custom solution)
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

(To be completed as implementation progresses)

### Prerequisites
- Python 3.8+
- Node.js (for Strudel integration)
- Strudel environment

### Installation
```bash
# Instructions coming soon
```

### Usage
```bash
# Instructions coming soon
```

## Contributing

This is an experimental project. Documentation and contribution guidelines will evolve as the project develops.

## License

TBD

## Notes

- Organ music provides excellent training data due to its complexity
- Werkmeister temperaments are historically important for baroque organ music
- Strudel's pattern-based syntax aligns well with musical phrase structures
- The challenge lies in translating traditional notation's expressiveness to code

## Future Possibilities

- Real-time sheet music following during live coding
- Collaborative annotation of sheet music for better OMR training
- Integration with other live coding environments (SuperCollider, Sonic Pi)
- Mobile app for quick scanning and conversion
- Cloud-based processing for complex scores
