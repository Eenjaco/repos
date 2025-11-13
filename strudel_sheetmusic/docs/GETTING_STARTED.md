# Getting Started - Development Guide

This guide will help you set up the Strudel Sheet Music Converter development environment.

## Prerequisites

### System Requirements
- **OS**: Linux, macOS, or Windows (WSL recommended)
- **Python**: 3.9 or higher
- **Node.js**: 16+ (for Strudel integration)
- **Memory**: 8GB RAM minimum (16GB recommended for OMR training)
- **Disk**: 5GB free space for dependencies and samples

### Required Software

1. **Python 3.9+**
   ```bash
   python --version  # Should be 3.9 or higher
   ```

2. **pip** (Python package manager)
   ```bash
   pip --version
   ```

3. **poppler-utils** (for PDF processing)
   ```bash
   # Ubuntu/Debian
   sudo apt-get install poppler-utils

   # macOS
   brew install poppler

   # Windows (via Chocolatey)
   choco install poppler
   ```

4. **Java 11+** (if using Audiveris for OMR)
   ```bash
   java --version
   ```

5. **Git**
   ```bash
   git --version
   ```

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd strudel_sheetmusic
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Linux/macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
# Test imports
python -c "import PIL; import pdf2image; import music21; print('All imports successful!')"
```

### 5. Download Audiveris (Optional)

If using Audiveris for OMR:

```bash
# Download from: https://github.com/Audiveris/audiveris/releases
# Extract and set AUDIVERIS_HOME environment variable
export AUDIVERIS_HOME=/path/to/audiveris
```

## Project Structure Overview

```
strudel_sheetmusic/
├── src/                    # Source code
│   ├── omr/               # PDF → MusicXML
│   ├── midi/              # MusicXML → MIDI
│   ├── strudel/           # MIDI → Strudel code
│   ├── mapping/           # Instrument mapping
│   └── tuning/            # Tuning systems
├── samples/               # Training sheet music
├── docs/                  # Documentation
├── config/                # Configuration files
├── tests/                 # Test suite
├── requirements.txt       # Python dependencies
└── README.md             # Main readme
```

## Quick Start - Running a Test

### Test 1: PDF to Image Conversion

```python
from src.omr.pdf_processor import PDFProcessor

# Create processor
processor = PDFProcessor(dpi=300)

# Convert PDF to images
images = processor.convert_to_images("samples/organ/test.pdf")

# Save images
processor.save_images(images, "output/images", prefix="test")

print(f"Converted {len(images)} pages")
```

### Test 2: Tuning System Calculation

```python
from src.tuning.werkmeister import WerkmeisterI

# Create Werkmeister I temperament (A4 = 440 Hz)
tuning = WerkmeisterI(base_frequency=440)

# Calculate frequency for C4
c4_freq = tuning.calculate_frequency(60)  # MIDI 60 = C4
print(f"C4 in Werkmeister I: {c4_freq:.2f} Hz")

# Get frequency table for octave 4
freq_table = tuning.get_frequency_table(octave=4)
for note, freq in freq_table.items():
    print(f"{note}4: {freq:.2f} Hz")

# Calculate pitch bend for MIDI
pitch_bend = tuning.get_pitch_bend(60)
print(f"Pitch bend for C4: {pitch_bend}")
```

## Development Workflow

### 1. Setting Up for Development

```bash
# Install development dependencies
pip install pytest pytest-cov black flake8 mypy

# Run code formatter
black src/

# Run linter
flake8 src/

# Run type checker
mypy src/
```

### 2. Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_tuning.py

# Run with verbose output
pytest -v
```

### 3. Adding New Features

1. Create feature branch
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Write code in appropriate module
   ```bash
   # Example: adding new tuning system
   vim src/tuning/meantone.py
   ```

3. Write tests
   ```bash
   vim tests/test_meantone.py
   ```

4. Run tests and ensure they pass
   ```bash
   pytest tests/test_meantone.py
   ```

5. Commit and push
   ```bash
   git add .
   git commit -m "Add meantone temperament"
   git push origin feature/your-feature-name
   ```

## Configuration

### Edit Configuration Files

```bash
# Werkmeister tunings
vim config/werkmeister_tunings.yaml

# Instrument mappings
vim config/instrument_mappings.yaml
```

### Environment Variables

Create `.env` file in project root:

```bash
# .env
DEBUG=true
LOG_LEVEL=INFO
AUDIVERIS_HOME=/path/to/audiveris
OUTPUT_DIR=./output
CACHE_DIR=./cache
```

## Adding Sample Sheet Music

1. Obtain public domain PDF
2. Verify quality (300+ DPI)
3. Add to appropriate directory:
   ```bash
   cp ~/Downloads/bach_fugue.pdf samples/organ/
   ```

4. Create metadata file:
   ```bash
   vim samples/organ/bach_fugue_metadata.json
   ```

5. Add entry to samples/README.md

## Common Tasks

### Convert PDF to Images

```bash
python -m src.omr.pdf_processor input.pdf output_dir/
```

### Generate Frequency Table

```python
from src.tuning.werkmeister import WerkmeisterI

tuning = WerkmeisterI()
table = tuning.get_frequency_table(octave=4)

# Export to CSV
import csv
with open('frequencies.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Note', 'Frequency (Hz)'])
    for note, freq in table.items():
        writer.writerow([note, freq])
```

### Test OMR Engine (once implemented)

```bash
python scripts/test_omr.py samples/organ/bach_bwv578.pdf
```

## Troubleshooting

### PDF Conversion Fails

**Problem**: `pdf2image` fails to convert PDF

**Solution**:
```bash
# Install poppler
# Ubuntu/Debian:
sudo apt-get install poppler-utils

# macOS:
brew install poppler

# Test poppler installation
pdftoppm -v
```

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'music21'`

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall requirements
pip install -r requirements.txt
```

### Memory Issues

**Problem**: Out of memory when processing large PDFs

**Solution**:
- Process pages individually instead of all at once
- Reduce DPI (e.g., 200 instead of 300)
- Close other applications
- Increase system swap space

### Permission Errors

**Problem**: Permission denied when writing files

**Solution**:
```bash
# Ensure output directory is writable
chmod -R u+w output/

# Or specify different output location
export OUTPUT_DIR=~/Documents/strudel_output
```

## Next Steps

### Immediate Tasks

1. **Add Sample Sheet Music**
   - Download Bach chorales from IMSLP
   - Add to `samples/organ/`
   - Create metadata files

2. **Implement OMR Engine**
   - Research Audiveris integration
   - OR implement basic recognition
   - Test with sample PDFs

3. **Complete MIDI Pipeline**
   - Implement MusicXML parser
   - Create MIDI converter
   - Test with known scores

4. **Build Strudel Generator**
   - Study Strudel syntax
   - Implement basic note → code conversion
   - Test output in Strudel REPL

### Learning Resources

**Music Theory & Notation**
- [Music21 Documentation](http://web.mit.edu/music21/)
- [MusicXML Tutorial](https://www.musicxml.com/tutorial/)

**OMR**
- [Audiveris Handbook](https://audiveris.github.io/audiveris/)
- [OMR Research Papers](https://github.com/OMR-Research)

**Strudel**
- [Strudel Documentation](https://strudel.tidalcycles.org/)
- [TidalCycles Learn](https://tidalcycles.org/docs/)

**Tuning Systems**
- [Kyle Gann's Tuning Guide](https://www.kylegann.com/tuning.html)
- [Huygens-Fokker Foundation](https://www.huygens-fokker.org/)

## Getting Help

- **Documentation**: See `docs/` directory
- **Issues**: GitHub issues (if applicable)
- **Discussions**: Community forum (if applicable)

## Contributing

See [ARCHITECTURE.md](ARCHITECTURE.md) for technical details.

---

**Ready to start developing?** Try running the tuning system test above, then explore the codebase!
