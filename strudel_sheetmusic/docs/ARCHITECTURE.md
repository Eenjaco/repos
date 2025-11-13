# Technical Architecture

## System Overview

The Strudel Sheet Music Converter is a multi-stage pipeline that transforms PDF sheet music into executable Strudel code. Each stage is modular, allowing for independent development and testing.

## Component Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Web Interface                        │
│  (Upload, Configure, Preview, Download)                 │
└───────────────┬─────────────────────────────────────────┘
                │
                ↓
┌─────────────────────────────────────────────────────────┐
│                  API Layer (Flask/FastAPI)               │
│  - File handling                                         │
│  - Job queue management                                  │
│  - WebSocket for real-time updates                      │
└───────────────┬─────────────────────────────────────────┘
                │
                ↓
┌─────────────────────────────────────────────────────────┐
│              Pipeline Orchestrator                       │
│  - Manages workflow stages                              │
│  - Error handling and recovery                          │
│  - Progress tracking                                    │
└─────┬──────┬──────┬──────┬──────┬────────────────┬─────┘
      │      │      │      │      │                │
      ↓      ↓      ↓      ↓      ↓                ↓
   ┌────┐┌────┐┌────┐┌────┐┌────┐         ┌──────────┐
   │OMR ││MIDI││Map ││Tune││Code│         │  Cache   │
   └────┘└────┘└────┘└────┘└────┘         └──────────┘
```

## Stage 1: PDF Processing & OMR

### Input
- PDF file (sheet music)
- Optional: DPI setting, page range

### Processing
1. **PDF to Image Conversion**
   - Library: `pdf2image`
   - Output: High-res PNG (300+ DPI)
   - Per-page processing for memory efficiency

2. **Image Preprocessing**
   - Deskewing (rotation correction)
   - Noise reduction
   - Contrast enhancement
   - Staff line detection

3. **OMR (Optical Music Recognition)**
   - **Option A**: Audiveris (Java-based, mature)
   - **Option B**: Custom TensorFlow/PyTorch model
   - **Option C**: music21 + opencv for simple cases

### Output
- MusicXML file (standardized music notation format)
- Confidence scores per element
- Bounding boxes for manual correction

### Key Modules

```python
# src/omr/pdf_processor.py
class PDFProcessor:
    def convert_to_images(pdf_path: str) -> List[Image]
    def preprocess_image(image: Image) -> Image

# src/omr/omr_engine.py
class OMREngine:
    def recognize(image: Image) -> MusicXML
    def get_confidence_scores() -> Dict

# src/omr/staff_detector.py
class StaffDetector:
    def detect_staves(image: Image) -> List[Staff]
    def separate_systems(image: Image) -> List[System]
```

## Stage 2: MIDI Conversion

### Input
- MusicXML file from OMR stage
- User configuration (tempo, dynamics)

### Processing
1. **MusicXML Parsing**
   - Library: `music21`
   - Extract notes, rhythms, dynamics, articulations
   - Preserve staff/voice structure

2. **MIDI Generation**
   - Library: `mido`
   - Convert pitch/duration to MIDI events
   - Map dynamics to velocity
   - Create tracks per staff/instrument

3. **Validation**
   - Check timing accuracy
   - Verify pitch ranges
   - Detect anomalies

### Output
- Standard MIDI file (.mid)
- JSON representation for further processing
- Timing/track metadata

### Key Modules

```python
# src/midi/musicxml_parser.py
class MusicXMLParser:
    def parse(musicxml: str) -> Score
    def extract_metadata() -> Dict

# src/midi/midi_converter.py
class MIDIConverter:
    def score_to_midi(score: Score) -> MIDIFile
    def add_track(notes: List[Note], track_num: int)

# src/midi/validator.py
class MIDIValidator:
    def validate(midi: MIDIFile) -> ValidationReport
    def detect_errors(midi: MIDIFile) -> List[Error]
```

## Stage 3: Instrument Mapping

### Input
- MIDI file with multiple tracks
- Score image (for visual reference)
- User's instrument preferences

### Processing
1. **Track Identification**
   - Analyze pitch ranges
   - Detect instrument characteristics
   - Suggest mappings

2. **User Interaction**
   - Visual score display
   - Clickable staff selection
   - Instrument dropdown per track
   - Preview individual tracks

3. **Mapping Configuration**
   - Store track → instrument associations
   - Define sound sample paths
   - Set per-instrument parameters

### Output
- Mapping configuration JSON
- Modified MIDI with instrument assignments
- Sample library references

### Key Modules

```python
# src/mapping/track_analyzer.py
class TrackAnalyzer:
    def analyze_range(track: Track) -> Range
    def suggest_instrument(track: Track) -> Instrument

# src/mapping/mapper_ui.py
class MapperInterface:
    def display_score(image: Image, tracks: List[Track])
    def select_region(staff_num: int) -> Track
    def assign_instrument(track: Track, instrument: Instrument)

# src/mapping/config_manager.py
class MappingConfig:
    def save(config: Dict, path: str)
    def load(path: str) -> Dict
    def validate(config: Dict) -> bool
```

## Stage 4: Tuning System Application

### Input
- MIDI file with note data
- Selected tuning system (Werkmeister I-VI, Equal, Custom)
- Base frequency (e.g., A4 = 440Hz)

### Processing
1. **Tuning Calculation**
   - Load tuning definition
   - Calculate frequency for each note
   - Determine MIDI pitch bend values

2. **MIDI Modification**
   - Insert pitch bend events before each note
   - Adjust per-channel if needed
   - Preserve timing accuracy

3. **Validation**
   - Verify pitch bend range (-8192 to +8191)
   - Check for channel limitations
   - Test audio output

### Output
- Retuned MIDI file
- Frequency table for reference
- Tuning visualization data

### Key Modules

```python
# src/tuning/temperament.py
class Temperament:
    def calculate_frequency(note: Note) -> float
    def get_pitch_bend(note: Note) -> int

# src/tuning/werkmeister.py
class WerkmeisterI(Temperament):
    # Werkmeister I (III) - "correct temperament"

class WerkmeisterII(Temperament):
    # Werkmeister II

# ... (through Werkmeister VI)

# src/tuning/tuning_applicator.py
class TuningApplicator:
    def apply_tuning(midi: MIDIFile, temperament: Temperament) -> MIDIFile
    def insert_pitch_bends(track: Track, bends: List[PitchBend])
```

## Stage 5: Strudel Code Generation

### Input
- Retuned MIDI file
- Mapping configuration
- Strudel generation settings

### Processing
1. **Pattern Analysis**
   - Identify repeated patterns
   - Detect rhythmic motifs
   - Find chord progressions

2. **Code Generation**
   - Convert notes to Strudel syntax
   - Use mini-notation where appropriate
   - Add effects from articulations
   - Structure as functions/patterns

3. **Optimization**
   - Simplify redundant patterns
   - Use Strudel's pattern transformations
   - Add comments for clarity

### Output
- Strudel JavaScript code
- Multiple format options (compact, readable, modular)
- Playback instructions

### Key Modules

```python
# src/strudel/pattern_analyzer.py
class PatternAnalyzer:
    def find_patterns(notes: List[Note]) -> List[Pattern]
    def identify_motifs(notes: List[Note]) -> List[Motif]

# src/strudel/code_generator.py
class StrudelGenerator:
    def generate(midi: MIDIFile, mapping: MappingConfig) -> str
    def notes_to_pattern(notes: List[Note]) -> str
    def add_effects(pattern: str, articulations: List) -> str

# src/strudel/optimizer.py
class CodeOptimizer:
    def simplify(code: str) -> str
    def extract_functions(code: str) -> str
```

## Data Models

### Score Representation

```python
@dataclass
class Note:
    pitch: int          # MIDI number (0-127)
    duration: float     # In quarter notes
    onset: float        # Time position
    velocity: int       # Dynamics (0-127)
    staff: int          # Staff number
    voice: int          # Voice within staff
    articulation: str   # staccato, legato, etc.

@dataclass
class Staff:
    number: int
    clef: str          # treble, bass, alto, etc.
    key_signature: str
    time_signature: tuple[int, int]
    notes: List[Note]

@dataclass
class Score:
    title: str
    composer: str
    staves: List[Staff]
    tempo: int
    metadata: Dict
```

### Configuration Models

```python
@dataclass
class InstrumentMapping:
    track_id: int
    staff_number: int
    instrument_name: str
    sample_path: str
    volume: float
    effects: List[Effect]

@dataclass
class TuningConfig:
    temperament: str    # "werkmeister_iii", "equal", etc.
    base_frequency: float  # A4 frequency
    reference_note: str    # "A4"

@dataclass
class GenerationConfig:
    output_format: str  # "compact", "readable", "modular"
    include_comments: bool
    use_mini_notation: bool
    pattern_detection: bool
```

## API Endpoints

```python
# REST API
POST   /api/upload              # Upload PDF
GET    /api/jobs/{id}           # Job status
GET    /api/jobs/{id}/preview   # Preview score
POST   /api/jobs/{id}/configure # Set mapping/tuning
GET    /api/jobs/{id}/generate  # Generate Strudel code
GET    /api/jobs/{id}/download  # Download outputs

# WebSocket
/ws/job/{id}                    # Real-time progress updates
```

## Data Flow Example

```
1. User uploads "bach_bwv578.pdf"
   ↓
2. PDF → Images (6 pages)
   ↓
3. OMR processes each page → musicxml_parts
   ↓
4. Combine parts → full_score.musicxml
   ↓
5. MusicXML → MIDI (3 tracks: Manual I, Manual II, Pedal)
   ↓
6. User maps: Manual I → "organ_great", Manual II → "organ_swell", Pedal → "organ_pedal"
   ↓
7. Apply Werkmeister III tuning → retuned_midi
   ↓
8. Generate Strudel code:
   ```javascript
   const manualI = s("organ_great").note("c4 d4 e4 f4")
   const manualII = s("organ_swell").note("e3 f3 g3 a3")
   const pedal = s("organ_pedal").note("c2 . . .")
   stack(manualI, manualII, pedal)
   ```
```

## Technology Stack

### Backend
- **Python 3.9+**: Core processing
- **FastAPI**: REST API and WebSocket
- **Celery**: Async job processing
- **Redis**: Job queue and caching
- **PostgreSQL**: Metadata storage (optional)

### Libraries
- **pdf2image**: PDF conversion
- **Pillow**: Image processing
- **Audiveris**: OMR engine
- **music21**: Music theory and MusicXML
- **mido**: MIDI processing
- **numpy**: Numerical computations
- **opencv-python**: Computer vision

### Frontend
- **React** or **Vue**: UI framework
- **PDF.js**: PDF rendering
- **Tone.js**: Audio preview
- **Monaco Editor**: Code editing

### Deployment
- **Docker**: Containerization
- **Docker Compose**: Development environment
- **Nginx**: Reverse proxy
- **Let's Encrypt**: SSL certificates

## Performance Considerations

### Processing Time Targets
- Simple melody (1 page): < 10 seconds
- Complex organ piece (4 pages): < 60 seconds
- Large score (20+ pages): < 5 minutes

### Optimization Strategies
- Parallel page processing
- Cached OMR results
- Incremental processing
- GPU acceleration for OMR
- Streaming output for large files

### Scalability
- Horizontal scaling via job queue
- Separate OMR workers
- CDN for sample libraries
- Database sharding if needed

## Error Handling

### OMR Errors
- Low confidence warnings
- Manual correction interface
- Retry with different parameters
- Fallback to simpler recognition

### Conversion Errors
- Invalid MusicXML handling
- MIDI range violations
- Timing inconsistencies
- User notification with details

### Generation Errors
- Unsupported notation graceful degradation
- Syntax validation before output
- Alternative generation strategies

## Testing Strategy

### Unit Tests
- Each module independently
- Mock external dependencies
- Edge cases and error conditions

### Integration Tests
- Full pipeline with sample files
- Various complexity levels
- Different music styles

### End-to-End Tests
- Real user workflows
- Performance benchmarks
- Browser compatibility

### Test Data
- Public domain scores
- Synthetic test cases
- Known-good reference outputs

## Security Considerations

- File upload validation (size, type)
- Sandboxed OMR processing
- Rate limiting on API
- Input sanitization
- No code execution from user input
- Secure sample library access

## Monitoring and Logging

- Processing time per stage
- Success/failure rates
- OMR confidence scores
- User feedback collection
- Error tracking (Sentry)
- Analytics (job types, popular features)

## Future Enhancements

- Real-time collaboration
- Mobile app (camera → sheet music)
- Browser-based OMR (TensorFlow.js)
- Cloud sample library
- Community score sharing
- API for third-party integrations
- Plugin system for custom instruments
