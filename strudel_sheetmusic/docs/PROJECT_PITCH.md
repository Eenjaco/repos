# Strudel Sheet Music Converter - Project Pitch

## Executive Summary

**Vision**: Bridge the 500-year gap between traditional music notation and modern live coding by creating an intelligent system that transforms printed sheet music into executable Strudel code.

**Problem**: Musicians with classical training and vast libraries of sheet music cannot easily access their repertoire in live coding environments. Live coders cannot easily incorporate classical compositions without manual transcription.

**Solution**: An AI-powered application that scans PDF sheet music, understands musical notation through OMR (Optical Music Recognition), and generates playable Strudel/TidalCycles code with historical tuning accuracy.

## The Opportunity

### Target Audiences

1. **Classical Musicians Exploring Live Coding**
   - Want to bring their repertoire into modern environments
   - Interested in remixing and reinterpreting classical works
   - Need a bridge between their training and new technology

2. **Live Coders and Electronic Musicians**
   - Want access to classical composition techniques
   - Interested in historical performance practice
   - Need source material for algorithmic manipulation

3. **Music Educators**
   - Teaching music theory through interactive coding
   - Demonstrating historical tuning systems
   - Creating accessible arrangements

4. **Researchers and Musicologists**
   - Analyzing large corpora of scores
   - Studying performance practice
   - Experimenting with alternative tunings

5. **Church Musicians and Organists**
   - Access to historical organ repertoire
   - Authentic Werkmeister temperaments for baroque music
   - Practice tool when organ access is limited

## Unique Value Propositions

### 1. Organ Music Specialization
- **Multi-staff complexity**: 3 staves (right hand, left hand, pedals) provide rich training data
- **Historical authenticity**: Werkmeister temperaments essential for baroque organ music
- **Polyphonic richness**: Multiple simultaneous voices per hand
- **Clear notation standards**: Centuries of consistent notation practice

### 2. Werkmeister Tuning Integration
- First live coding environment with historical temperament support
- Authentic baroque sound reproduction
- Educational tool for understanding historical performance practice
- Six Werkmeister temperaments plus custom definitions

### 3. Intelligent Instrument Mapping
- Visual interface for assigning notation to sounds
- Per-instrument tuning configuration
- Sample library integration
- Real-time preview

### 4. Strudel Integration
- Pattern-based code generation matches musical phrases
- Live modifiable output
- Integration with Strudel's extensive sample library
- Export to multiple formats (Strudel, TidalCycles, MIDI)

## Technical Approach

### Pipeline Architecture

```
PDF Input
    ↓
[Image Processing]
    ↓
[OMR Engine] ← Training Data (Organ Scores)
    ↓
[MusicXML Generation]
    ↓
[MIDI Conversion]
    ↓
[Instrument Mapper] ← User Configuration
    ↓
[Tuning Processor] ← Werkmeister Definitions
    ↓
[Strudel Code Generator]
    ↓
Strudel Code Output
```

### Technology Stack

**Core Processing**
- Python 3.8+ (OMR, MIDI processing, orchestration)
- Audiveris or custom OMR engine
- `mido` for MIDI handling
- `music21` for music theory operations

**Frontend**
- Web-based interface (React/Vue)
- PDF.js for PDF rendering
- Interactive score annotations
- Real-time code preview

**Tuning Systems**
- Custom Python implementation of Werkmeister I-VI
- Frequency calculation engine
- MIDI pitch bend for microtonal accuracy

**Integration**
- Strudel JavaScript API
- WebSocket for real-time communication
- Export to multiple formats

### Key Technical Challenges

1. **OMR Accuracy**
   - Solution: Train on high-quality organ scores with clear notation
   - Validation: Manual verification interface
   - Fallback: User correction tools

2. **Polyphonic Voice Separation**
   - Solution: Stem direction analysis, music theory rules
   - For organ: Clear staff separation helps
   - Multi-pass analysis for complex passages

3. **Timing and Rhythm**
   - Solution: Tempo marking recognition
   - User-configurable base tempo
   - Preserve relative durations accurately

4. **Strudel Code Generation**
   - Solution: Pattern templates for common structures
   - Phrase-level generation (not note-by-note)
   - Preserve musical meaning

5. **Tuning Implementation**
   - Solution: Pre-calculated tuning tables
   - MIDI pitch bend messages
   - Per-note frequency adjustment

## Development Phases

### Phase 1: MVP (Months 1-2)
**Goal**: Prove the core concept works

- Basic PDF to image conversion
- Simple monophonic melody recognition
- Direct MIDI output
- Command-line interface
- Equal temperament only

**Deliverable**: Convert a simple one-staff melody to playable MIDI

### Phase 2: Core Features (Months 3-4)
**Goal**: Complete the pipeline

- Full OMR implementation
- Multi-staff recognition
- Strudel code generation
- Basic web interface
- Instrument mapping prototype

**Deliverable**: Convert a simple organ piece to Strudel code

### Phase 3: Advanced Features (Months 5-6)
**Goal**: Add unique capabilities

- Werkmeister tuning implementation
- Advanced instrument mapping UI
- Multiple instrument types (guitar, drums, etc.)
- Training on organ corpus
- Accuracy improvements

**Deliverable**: Baroque organ piece in authentic Werkmeister III

### Phase 4: Polish & Launch (Months 7-8)
**Goal**: Production-ready application

- Performance optimization
- Documentation and tutorials
- Sample library
- Community features
- Public beta launch

**Deliverable**: Public web application with sample gallery

## Training Data Strategy

### Organ Music Advantages

1. **Structural Clarity**
   - Three distinct staves with clear roles
   - Consistent notation conventions
   - Minimal ambiguity in voice leading

2. **Musical Richness**
   - Full harmonic progressions
   - Complex rhythmic relationships
   - Diverse articulations and dynamics

3. **Historical Importance**
   - Well-documented performance practice
   - Authentic tuning requirements
   - Educational value

4. **Notation Quality**
   - Professionally engraved scores
   - High-quality PDF scans available
   - Public domain repertoire (Bach, Buxtehude, etc.)

### Sample Collection Plan

- Bach organ works (BWV 525-748)
- Buxtehude praeludia and fugues
- French classical organ school
- Modern practice editions with clear notation
- Public domain sources (IMSLP)

## Market Validation

### Similar Projects (Gaps Analysis)

1. **MuseScore OMR**: Good recognition, no live coding output
2. **SmartScore**: Commercial, no temperament support
3. **Audiveris**: Open source OMR, no Strudel integration
4. **PhotoScore**: Expensive, limited output formats

**Our Advantage**: Only solution combining OMR + historical tuning + live coding

### Community Interest Indicators

- Growing live coding community (Toplap, Algorave)
- Renewed interest in historical performance practice
- Music education seeking interactive tools
- DIY music technology enthusiasm

## Business Model (Optional)

### Free Tier
- Basic OMR (monophonic melodies)
- Equal temperament
- Limited conversions per month
- Open source core components

### Premium Tier
- Advanced OMR (polyphonic, multi-staff)
- All tuning systems
- Unlimited conversions
- Priority processing
- Advanced features

### Enterprise/Education
- Batch processing
- Custom tuning definitions
- Integration APIs
- Support and training

## Success Metrics

### Technical Metrics
- OMR accuracy: >95% for organ scores
- Processing time: <30 seconds for typical page
- Code compilation rate: >98% (valid Strudel syntax)

### User Metrics
- Active users converting scores weekly
- Library of user-contributed scores
- Community contributions to OMR training
- Tutorial completion rates

### Impact Metrics
- Performances using converted scores
- Academic citations
- Educational adoption
- Open source contributions

## Risk Mitigation

### Technical Risks
- **OMR accuracy**: Provide manual correction tools
- **Complex notation**: Start with simple pieces, expand gradually
- **Tuning precision**: Use pitch bend, accept MIDI limitations

### Market Risks
- **Niche audience**: Focus on quality over quantity
- **Competition**: Emphasize unique features (tuning, Strudel)
- **Adoption**: Extensive documentation and examples

### Legal Risks
- **Copyright**: Focus on public domain scores
- **Licensing**: Clear open source license
- **Fair use**: Educational and transformative use

## Why This Matters

### Musical Heritage + Modern Technology
- Makes 500 years of music accessible to new generation
- Preserves historical performance practice
- Enables new forms of musical expression

### Educational Impact
- Interactive learning tool for music theory
- Demonstrates tuning systems tangibly
- Bridges classical training and modern technology

### Creative Possibilities
- Live remixing of classical works
- Algorithmic variations on traditional pieces
- New compositional techniques combining old and new

### Research Value
- Corpus analysis tools
- Performance practice experiments
- Computational musicology applications

## Call to Action

This project sits at the intersection of music history, artificial intelligence, and live coding culture. By starting with organ music—with its rich notation, historical significance, and clear structure—we can build a robust foundation for bringing all forms of sheet music into the live coding ecosystem.

The time is right: OMR technology has matured, live coding is growing, and there's renewed interest in historical music. This application can become the standard tool for musicians bridging traditional and electronic music practices.

## Next Steps

1. **Immediate (Week 1-2)**
   - Finalize technology choices
   - Set up development environment
   - Acquire initial organ score samples
   - Build OMR proof-of-concept

2. **Short-term (Month 1)**
   - Implement basic pipeline
   - Test with simple monophonic examples
   - Validate MIDI conversion accuracy
   - Create project website/landing page

3. **Medium-term (Months 2-3)**
   - Complete multi-staff recognition
   - Implement Strudel code generation
   - Build basic web interface
   - Begin Werkmeister tuning implementation

4. **Long-term (Months 4-8)**
   - Full feature implementation
   - Training and accuracy improvements
   - Public beta and community building
   - Documentation and educational content

---

*"Every piece of sheet music is frozen music waiting to be brought to life. Let's give it a new voice."*
