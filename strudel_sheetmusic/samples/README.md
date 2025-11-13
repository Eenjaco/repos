# Sample Sheet Music Directory

This directory contains PDF sheet music samples for training, testing, and demonstrating the Strudel Sheet Music Converter.

## Directory Structure

```
samples/
├── organ/        # Organ music (primary training data)
├── guitar/       # Guitar music and tablature
├── voice/        # Vocal scores
├── drums/        # Percussion notation
└── bass/         # Bass notation
```

## Organ Music (`organ/`)

**Why organ music is ideal for training:**

1. **Multi-staff complexity**: Typically 3 staves (RH, LH, Pedal)
2. **Clear notation standards**: Centuries of consistent engraving
3. **Rich polyphony**: Multiple simultaneous voices
4. **Historical importance**: Baroque repertoire perfect for Werkmeister tunings
5. **Public domain availability**: Bach, Buxtehude, and others

### Recommended Organ Works to Include

**J.S. Bach:**
- BWV 565 - Toccata and Fugue in D minor
- BWV 578 - Fugue in G minor (Little Fugue)
- BWV 582 - Passacaglia and Fugue in C minor
- BWV 599-644 - Orgelbüchlein (various chorale preludes)
- BWV 525-530 - Trio Sonatas

**Buxtehude:**
- BuxWV 137-160 - Praeludia
- BuxWV 175-225 - Chorale preludes

**Sources:**
- IMSLP (International Music Score Library Project)
- Public domain editions
- Modern Urtext editions (check copyright)

### Naming Convention

```
composer_work_movement.pdf

Examples:
bach_bwv565_toccata.pdf
bach_bwv578_fugue_g_minor.pdf
buxtehude_buxwv137_praeludium_c_major.pdf
```

## Guitar Music (`guitar/`)

Guitar music presents unique challenges:
- Tablature notation (numbers on staff lines)
- Standard notation (treble clef, sounds octave lower)
- Chord diagrams
- Various techniques (hammer-on, pull-off, bend)

### Recommended Content
- Classical guitar pieces (Renaissance, Baroque transcriptions)
- Jazz standards with chord charts
- Fingerstyle arrangements
- Simple melodies for testing

## Voice Music (`voice/`)

Vocal music organized by voice type:
- Soprano (soprano/)
- Alto (alto/)
- Tenor (tenor/)
- Bass (bass/)
- SATB (satb/) - Four-part choral music

### Recommended Content
- Simple hymns and chorales
- Art songs (Lieder, Melodies)
- Opera arias
- Folk songs
- SATB Bach chorales

## Drums Music (`drums/`)

Percussion notation challenges:
- Non-pitched notation (note positions indicate instruments)
- Various note heads (x for cymbals, etc.)
- No traditional pitch recognition needed
- Rhythm is primary feature

### Recommended Content
- Basic rock/pop beats
- Jazz drum charts
- Orchestral percussion parts
- Marching band snare drum exercises

## Bass Music (`bass/`)

Bass guitar or double bass:
- Bass clef notation
- Tablature (for bass guitar)
- Walking bass lines
- Slap notation and techniques

### Recommended Content
- Jazz walking bass lines
- Rock/pop bass parts
- Classical double bass exercises
- Funk and R&B patterns

## File Requirements

### Format
- **Preferred**: PDF (vector or high-resolution scan)
- **Minimum resolution**: 300 DPI for scanned scores
- **Color**: Grayscale or B&W preferred (cleaner OMR)

### Quality Checklist
- [ ] Clear staff lines (straight, not warped)
- [ ] Sharp note heads (not blurred)
- [ ] Consistent spacing
- [ ] Minimal printing artifacts
- [ ] No coffee stains or damage
- [ ] Proper orientation (not rotated)

### Metadata
Each sample should include a companion `.json` file with metadata:

```json
{
  "filename": "bach_bwv578_fugue_g_minor.pdf",
  "composer": "Johann Sebastian Bach",
  "title": "Fugue in G minor (Little Fugue)",
  "catalog_number": "BWV 578",
  "instrument": "organ",
  "key": "G minor",
  "time_signature": "4/4",
  "staff_count": 3,
  "page_count": 4,
  "difficulty": "intermediate",
  "period": "baroque",
  "recommended_tuning": "werkmeister_i",
  "source": "IMSLP",
  "copyright": "public_domain",
  "edition": "Breitkopf & Härtel",
  "notes": "Three-voice fugue with pedal. Excellent test case for polyphonic recognition."
}
```

## Training vs. Testing Split

Organize samples for machine learning:

```
samples/
├── organ/
│   ├── train/      # 80% of samples for training
│   ├── validate/   # 10% for validation during training
│   └── test/       # 10% for final testing
```

## Ground Truth Data

For training OMR systems, provide ground truth:

```
samples/organ/train/bach_bwv578/
├── bach_bwv578.pdf              # Original PDF
├── bach_bwv578_metadata.json    # Metadata
├── bach_bwv578.musicxml         # Ground truth MusicXML
├── bach_bwv578.mid              # Ground truth MIDI
└── pages/
    ├── page_001.png             # Page images
    ├── page_002.png
    └── ...
```

## Copyright and Licensing

**Important**: Only include public domain or properly licensed music.

### Public Domain Sources
- Pre-1928 publications (in USA)
- Expired copyrights (varies by country)
- Creative Commons licensed works
- Government works

### Attribution
Always include:
- Composer name
- Original publication info
- Source URL (e.g., IMSLP link)
- License information

### Prohibited
- Modern copyrighted editions without permission
- Arrangements under copyright
- Performance editions with copyright restrictions

## Adding New Samples

1. **Verify copyright status**
2. **Check quality** (resolution, clarity)
3. **Add to appropriate directory**
4. **Create metadata JSON file**
5. **If possible, create ground truth** (MusicXML/MIDI)
6. **Update this README** with sample count

## Current Sample Inventory

| Category | Sample Count | Notes |
|----------|--------------|-------|
| Organ    | 0           | TODO: Add Bach chorales, fugues |
| Guitar   | 0           | TODO: Add classical pieces |
| Voice    | 0           | TODO: Add simple songs |
| Drums    | 0           | TODO: Add basic beats |
| Bass     | 0           | TODO: Add walking bass lines |

**Total**: 0 samples

## Usage in Training

These samples will be used for:

1. **OMR Training**: Teaching the system to recognize notation
2. **Validation**: Testing accuracy during development
3. **Benchmarking**: Measuring improvement over time
4. **Demos**: Showcasing capabilities to users
5. **Edge Cases**: Collecting challenging examples

## Contribution Guidelines

To contribute samples:

1. Ensure public domain or proper licensing
2. Scan at 300+ DPI if physical score
3. Name files consistently
4. Create metadata JSON
5. Test with current OMR system
6. Submit with description of what makes it useful

## Resources

### Score Sources
- [IMSLP](https://imslp.org) - Petrucci Music Library
- [MuseScore](https://musescore.com) - Some public domain scores
- [CPDL](https://www.cpdl.org) - Choral Public Domain Library
- [Mutopia Project](https://www.mutopiaproject.org) - Free sheet music

### Scanning Tips
- Use flatbed scanner, not photo
- 300-600 DPI resolution
- Grayscale mode
- Save as PDF (not JPEG if possible)
- Deskew if necessary

### Quality Control Tools
- `pdftoppm` - Extract images from PDF
- ImageMagick - Process and clean scans
- Audiveris - Test OMR recognition
- MuseScore - Create ground truth MusicXML

---

**Note**: This directory is critical for project success. Quality and quantity of training data directly impact OMR accuracy. Start with organ music, then expand to other instruments as the system improves.
