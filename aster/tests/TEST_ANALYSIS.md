# Test File Analysis

## Test Files Overview

Total files: 16
Total size: ~16MB
Languages: English, Afrikaans

## File Categories

### 📊 Spreadsheets (1 file)
- `Year A 2022-2023.xlsx` (17KB)
  - Excel format
  - Likely liturgical calendar data
  - **Status**: Need to add .xlsx support (currently only .csv)

### 🎵 Audio (1 file)
- `01 Track 1.wma` (158KB)
  - Windows Media Audio format
  - **Status**: Need to add .wma support (currently only .mp3, .wav, .m4a)
  - Requires ffmpeg conversion to compatible format

### 🖼️ Images (2 files)
- `Ron Kraybill.jpeg` (63KB)
  - Portrait/photo - likely text overlay or document photo
  - **Status**: OCR supported via Tesseract

- `The Post-Individual.jpeg` (3.7MB)
  - Large image - likely scanned document or infographic
  - **Status**: OCR supported via Tesseract

### 📄 Word Documents (2 files)
- `A S Verslag. Missionale Aard van die kerk.docx` (68KB)
  - Afrikaans church report on missional nature
  - **Status**: Supported via python-docx

- `NG Kerk Alma.docx` (5.9MB)
  - Large church document
  - **Status**: Supported via python-docx

### 📑 PDFs (6 files)
- `11 APRIL 2025 NUUSBRIEF.pdf` (322KB)
  - Afrikaans newsletter
  - **Status**: Supported via pdfplumber

- `Anthony de Mello - Sadhana - A Way to God.pdf` (1.5MB)
  - Spiritual book
  - **Status**: Supported via pdfplumber

- `Biddae en Feesdae.pdf` (54KB)
  - Afrikaans prayer days and feast days
  - **Status**: Supported via pdfplumber

- `Cal Newport - Deep Work.pdf` (727KB)
  - Productivity book
  - **Status**: Supported via pdfplumber

- `First 90 Days.pdf` (2.0MB)
  - Leadership book
  - **Status**: Supported via pdfplumber

- `VONKK 0023 OB Full Score.pdf` (100KB)
  - Musical score
  - **Status**: Supported but may extract poorly (graphical)

- `VONKK 0203 OB.pdf` (332KB)
  - Musical score
  - **Status**: Supported but may extract poorly (graphical)

### 📊 Presentations (1 file)
- `02 Jun 2024.pptx` (51KB)
  - PowerPoint presentation
  - **Status**: Should be supported via python-pptx (need to verify)

### 📚 Ebooks (1 file)
- `Tiyo Soga (1829–1871) at the intersection of 'universes in collision'.epub` (194KB)
  - Historical biography
  - **Status**: Supported via ebooklib

### 🌐 Web Pages (1 file)
- `Tuis - Kerkbode.html` (489KB)
  - Afrikaans church website page
  - **Status**: Supported via BeautifulSoup

## Test Objectives

### 1. Format Support Testing
- ✅ Verify existing format handlers work correctly
- ⚠️ Identify missing format support (.wma, .xlsx)
- 🔧 Test edge cases (large files, special characters, multilingual)

### 2. Ollama Prompt Optimization
Test different content types require different prompts:
- **Religious texts** (Afrikaans): Preserve theological terms, proper nouns
- **Books**: Chapter detection, heading hierarchy, reference preservation
- **Newsletters**: Date formatting, article separation, contact info
- **Technical documents**: Preserve formatting, code blocks, lists

### 3. Language Handling
- Afrikaans content (multiple files)
- English content
- Mixed language documents
- Special characters (accents, diacritics)

### 4. Performance Testing
- Small files (< 100KB): Fast processing
- Medium files (100KB - 1MB): Reasonable speed
- Large files (> 1MB): Progress indicators needed

### 5. Quality Metrics
- Text extraction accuracy
- Structure preservation (headings, lists, tables)
- Special character handling
- Metadata extraction
- Ollama enhancement quality

## Test Execution Plan

### Phase 1: Quick Compatibility Test
Run all files through mdclean_universal and document:
- Success/failure status
- Processing time
- Output quality (1-5 rating)
- Errors encountered

### Phase 2: Format Extension
Add missing format support:
- .xlsx → convert to CSV handler
- .wma → add audio format support with ffmpeg
- .pptx → verify/add python-pptx handler

### Phase 3: Ollama Prompt Engineering
Create specialized prompts for:
- Religious/theological content
- Technical documentation
- Newsletter formatting
- Book chapter structure
- Multilingual content

### Phase 4: Automated Testing
Create pytest suite with:
- Format detection tests
- Conversion accuracy tests
- Output validation tests
- Performance benchmarks

## Expected Challenges

1. **Musical scores (PDFs)**: Likely extract as gibberish - may need image-based OCR
2. **Large Word doc (5.9MB)**: May be slow or have embedded images
3. **Afrikaans content**: Ollama may struggle with proper nouns and theological terms
4. **Audio file**: Need ffmpeg for format conversion
5. **Excel file**: Different structure than CSV - need cell/sheet handling

## Success Criteria

- ✅ 80%+ of files process successfully
- ✅ Output is readable and structured
- ✅ Afrikaans content preserved accurately
- ✅ Processing completes within reasonable time
- ✅ Ollama enhancements add value (not just noise)
