# System Dependencies for Aster

Aster requires several system-level tools for processing different file types.

## Required Dependencies

### 1. FFmpeg (Audio Processing)
**Required for**: MP3, M4A, WMA, FLAC, OGG audio files

```bash
# macOS
brew install ffmpeg

# Linux (Ubuntu/Debian)
sudo apt-get install ffmpeg

# Linux (Fedora/RHEL)
sudo dnf install ffmpeg
```

**What it does**: Converts audio files to WAV format for transcription with Vosk

**Files affected**: `.mp3`, `.m4a`, `.wma`, `.flac`, `.ogg`

---

### 2. Pandoc (Document Conversion)
**Required for**: PowerPoint, Word documents (alternative to Unstructured)

```bash
# macOS
brew install pandoc

# Linux (Ubuntu/Debian)
sudo apt-get install pandoc

# Linux (Fedora/RHEL)
sudo dnf install pandoc
```

**What it does**: Converts PPTX, DOCX, and other document formats to text

**Files affected**: `.pptx`, `.ppt`, `.docx` (when Unstructured is not available)

---

### 3. Poppler (PDF Processing)
**Required for**: PDF text extraction

```bash
# macOS
brew install poppler

# Linux (Ubuntu/Debian)
sudo apt-get install poppler-utils

# Linux (Fedora/RHEL)
sudo dnf install poppler-utils
```

**What it does**: Provides `pdftotext` command for extracting text from PDFs

**Files affected**: `.pdf`

---

### 4. Tesseract OCR (Image Text Extraction)
**Required for**: Images, scanned PDFs

```bash
# macOS (with all languages)
brew install tesseract tesseract-lang

# Linux (Ubuntu/Debian)
sudo apt-get install tesseract-ocr tesseract-ocr-all

# Linux (Fedora/RHEL)
sudo dnf install tesseract tesseract-langpack-all
```

**Important languages for your use case**:
- `afr` - Afrikaans (critical for church documents)
- `eng` - English
- `nld` - Dutch

**What it does**: OCR for extracting text from images and scanned documents

**Files affected**: `.jpg`, `.jpeg`, `.png`, `.tiff`, `.pdf` (scanned)

---

### 5. Ghostscript (PDF OCR)
**Required for**: OCR on scanned PDFs

```bash
# macOS
brew install ghostscript

# Linux (Ubuntu/Debian)
sudo apt-get install ghostscript

# Linux (Fedora/RHEL)
sudo dnf install ghostscript
```

**What it does**: Converts PDFs to images for OCR processing

**Files affected**: Scanned `.pdf` files

---

### 6. ImageMagick (Optional - Image Preprocessing)
**Required for**: Enhanced image preprocessing for better OCR

```bash
# macOS
brew install imagemagick

# Linux (Ubuntu/Debian)
sudo apt-get install imagemagick

# Linux (Fedora/RHEL)
sudo dnf install ImageMagick
```

**What it does**: Enhances image quality before OCR (contrast, rotation, etc.)

**Files affected**: `.jpg`, `.jpeg`, `.png` (optional enhancement)

---

## Quick Install (macOS)

Install all dependencies at once:

```bash
brew install ffmpeg pandoc poppler tesseract tesseract-lang ghostscript imagemagick
```

## Quick Install (Linux Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install -y \
    ffmpeg \
    pandoc \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-all \
    ghostscript \
    imagemagick
```

## Verification

Check which dependencies are installed:

```bash
# FFmpeg
ffmpeg -version

# Pandoc
pandoc --version

# Poppler (pdftotext)
pdftotext -v

# Tesseract
tesseract --version
tesseract --list-langs  # Show installed languages

# Ghostscript
gs --version

# ImageMagick
convert --version
```

## Current Issues (From Test Results)

Based on your test results, you're currently missing:

1. **ffmpeg** - Blocks WMA audio processing
   ```
   ❌ 01 Track 1.wma failed: ffmpeg not installed
   ```

2. **pandoc** - Blocks PPTX processing
   ```
   ❌ 02 Jun 2024.pptx failed: pandoc not installed
   ```

3. **poppler** - Blocks PDF processing
   ```
   ❌ 11 APRIL 2025 NUUSBRIEF.pdf failed: pdftotext not installed
   ```

## Next Steps

Run this command on your Mac to install all missing dependencies:

```bash
cd /Users/mac/Documents/Applications/repos/aster
source venv/bin/activate
brew install ffmpeg pandoc poppler
```

Then re-run your tests:

```bash
python3 tests/run_tests.py
```

## Python Dependencies

These are installed via pip (in requirements.txt):

- `vosk` - Speech recognition engine
- `soundfile` - Audio file reading
- `unstructured[all-docs]` - Document structure detection
- `pytesseract` - Python wrapper for Tesseract
- `pandas` - Excel/CSV processing
- `ollama` - LLM interface

Already installed via your venv!
