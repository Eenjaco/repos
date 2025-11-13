# Setup Guide for Test Environment

## System Dependencies Required

To run all tests successfully on your Mac, install these dependencies:

```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required tools
brew install pandoc          # For DOCX, EPUB, HTML conversion
brew install poppler         # For PDF text extraction (includes pdftotext)
brew install tesseract       # For OCR on images
brew install ffmpeg          # For audio format conversion

# Verify installations
pandoc --version
pdftotext -v
tesseract --version
ffmpeg -version
```

## Python Dependencies

```bash
# Navigate to mdclean_universal directory
cd /Users/mac/Documents/Applications/repos/mdclean_universal

# Install Python packages
pip3 install -r requirements.txt

# Optional: Install unstructured for advanced document processing
pip3 install 'unstructured[all-docs]'
```

## Ollama Setup

```bash
# Install Ollama (if not already installed)
brew install ollama

# Pull the model we're using for testing
ollama pull llama3.2:1b

# Verify
ollama list
```

## Running Tests

Once all dependencies are installed:

```bash
# Run full test suite
python3 tests/run_tests.py

# Or test individual files
./mdclean_universal.py "tests/Cal Newport - Deep Work.pdf" -o "tests/outputs/test.md"

# With AI analysis
./mdclean_universal.py "tests/Cal Newport - Deep Work.pdf" --analyze
```

## Expected Results

After installing dependencies, you should see:

- **PDFs (7 files)**: 100% success - All religious texts, books, and music scores processed
- **Documents (2 files)**: 100% success - Afrikaans church documents converted
- **Images (2 files)**: 100% success - OCR extraction from JPEGs
- **HTML (1 file)**: 100% success - Web page converted
- **EPUB (1 file)**: 100% success - Ebook converted
- **XLSX (1 file)**: Will work after adding .xlsx support (see below)
- **WMA (1 file)**: Will work after adding .wma support (see below)
- **PPTX (1 file)**: Will work after adding .pptx support (see below)

## Missing Format Support

Currently not supported (but easy to add):

1. **`.xlsx` (Excel)** - Can be handled similar to CSV
2. **`.wma` (Windows Media Audio)** - Needs ffmpeg conversion
3. **`.pptx` (PowerPoint)** - Needs python-pptx library

These will be added in the next update.

## Troubleshooting

### "pandoc not installed"
```bash
brew install pandoc
```

### "pdftotext not installed"
```bash
brew install poppler
```

### "Tesseract OCR not installed"
```bash
brew install tesseract
```

### "No module named 'ollama'"
```bash
pip3 install ollama
```

### Ollama connection errors
```bash
# Start Ollama service
ollama serve

# In another terminal
ollama pull llama3.2:1b
```

## File-Specific Notes

### Large Files
These files may take longer to process:
- **NG Kerk Alma.docx** (5.9MB) - ~30-60 seconds
- **The Post-Individual.jpeg** (3.7MB) - OCR intensive, ~45-90 seconds
- **First 90 Days.pdf** (2.0MB) - ~20-40 seconds
- **Anthony de Mello - Sadhana - A Way to God.pdf** (1.5MB) - ~15-30 seconds

### Music Scores
- **VONKK PDFs** - Will extract text but may not be useful (musical notation)
- Consider using image-based OCR instead

### Afrikaans Content
Files containing Afrikaans text:
- 11 APRIL 2025 NUUSBRIEF.pdf
- A S Verslag. Missionale Aard van die kerk.docx
- Biddae en Feesdae.pdf
- NG Kerk Alma.docx
- Tuis - Kerkbode.html

These require special Ollama prompts to preserve proper nouns and theological terms.

## Test Coverage

| Format | Files | Status |
|--------|-------|--------|
| PDF | 7 | ✅ Supported |
| DOCX | 2 | ✅ Supported |
| JPEG | 2 | ✅ Supported (with Tesseract) |
| HTML | 1 | ✅ Supported |
| EPUB | 1 | ✅ Supported |
| XLSX | 1 | ⚠️ Needs implementation |
| WMA | 1 | ⚠️ Needs implementation |
| PPTX | 1 | ⚠️ Needs implementation |

## Next Steps

1. Install all dependencies on your Mac
2. Run tests to establish baseline
3. Add missing format support (.xlsx, .wma, .pptx)
4. Create specialized Ollama prompts for different content types
5. Run tests again and compare results
