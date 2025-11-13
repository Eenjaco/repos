# mdclean_universal

**Universal Document Processor for Knowledge Management**

Convert ANY document type to clean, structured markdown ready for Obsidian/Zettelkasten.

---

## What It Does

One tool to process **all** your documents:

```
📸 Photos → 🎙️ Audio → 📄 PDFs → 💰 CSV → 📝 Text → 💎 Clean Markdown
```

**Supported formats:**
- **Images**: JPG, PNG (OCR with Tesseract)
- **Audio**: MP3, M4A, WAV (transcription)
- **Documents**: PDF, EPUB, DOCX, HTML
- **Financial**: CSV (budgets, transactions, portfolios)
- **Text**: TXT, MD (cleanup)

**Pipeline:**
1. **Extract** - OCR images, transcribe audio, parse documents
2. **Structure** - Detect headings, paragraphs, lists (Unstructured.io)
3. **Clean** - Add punctuation, fix errors (Ollama 3.2 1B)
4. **Format** - Generate frontmatter, metadata for knowledge management

---

## Quick Start

```bash
# Install dependencies
cd mdclean_universal
pip install -r requirements.txt

# System tools (macOS)
brew install tesseract ghostscript poppler pandoc ollama
ollama pull llama3.2:1b

# Run it
./mdclean_universal.py document.pdf
./mdclean_universal.py photo.jpg

# CSV with automatic AI analysis
./mdclean_universal.py budget.csv --analyze
```

---

## Project Structure

```
mdclean_universal/
├── mdclean_universal.py       # Main tool (images, docs, audio, text)
├── csv_handler.py              # CSV financial processor
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── docs/
│   ├── ENHANCEMENT_PROPOSAL.md    # Technical design & architecture
│   ├── MIGRATION_GUIDE.md         # Migrate from old tools
│   ├── CSV_FINANCIAL_WORKFLOW.md  # Financial management guide
│   └── QUICKSTART_CSV.md          # CSV quick start
└── examples/
    ├── sample_transactions.csv
    └── sample_transactions_converted.md
```

---

## Key Features

### 🔒 Privacy-First Financial Management
- Import bank CSV → Beautiful markdown tables
- Local AI analysis with Ollama (no cloud!)
- Track budget, portfolio, debt, net worth
- Export to PDF or back to CSV
- See: [docs/CSV_FINANCIAL_WORKFLOW.md](docs/CSV_FINANCIAL_WORKFLOW.md)

### 📸 OCR for Everything
- Photos of handwritten notes
- Screenshots of text
- Scanned documents
- Book pages
- Whiteboard captures

### 🎙️ Audio Transcription
- Sermons, lectures, interviews
- Voice memos, podcasts
- With punctuation and structure
- Integration with existing mp3_txt tools

### 📄 Document Processing
- PDFs (text and scanned)
- EPUB books
- Word documents (DOCX)
- Web pages (HTML)

### 🤖 AI-Enhanced
- Ollama 3.2 1B for text cleanup
- Automatic punctuation & capitalization
- Error correction
- Financial insights
- Budget recommendations

### 💎 Knowledge Management Ready
- YAML frontmatter
- Metadata extraction
- Tag generation
- Obsidian math notation
- Wikilink support (coming soon)

---

## Usage Examples

### Process Any Document
```bash
# Images (OCR)
./mdclean_universal.py notes.jpg
./mdclean_universal.py handwritten.jpg --handwriting

# PDFs
./mdclean_universal.py research_paper.pdf
./mdclean_universal.py scanned_book.pdf

# Audio (coming soon - use mp3_txt for now)
./mdclean_universal.py sermon.mp3

# Financial CSV with automatic AI analysis
./mdclean_universal.py transactions.csv --analyze
./mdclean_universal.py budget.csv --csv-mode budget --analyze

# Or use standalone CSV handler
python3 csv_handler.py transactions.csv --mode financial

# Batch processing
./mdclean_universal.py --batch ~/Documents/inbox/
```

### Financial Workflow
```bash
# Convert bank export with automatic AI analysis
./mdclean_universal.py bank_nov_2025.csv --analyze

# Result includes:
# - Income/expense summary
# - Category breakdown
# - Running balance
# - ✨ Automatic AI insights from Ollama
# - Obsidian math formulas

# Manual analysis (if preferred)
python3 csv_handler.py bank_nov_2025.csv --mode financial
ollama run llama3.2:1b "[paste generated prompt]"
```

---

## Documentation

**Getting Started:**
- [README.md](README.md) - This file
- [docs/QUICKSTART_CSV.md](docs/QUICKSTART_CSV.md) - CSV in 5 minutes

**Complete Guides:**
- [docs/ENHANCEMENT_PROPOSAL.md](docs/ENHANCEMENT_PROPOSAL.md) - Architecture & design
- [docs/CSV_FINANCIAL_WORKFLOW.md](docs/CSV_FINANCIAL_WORKFLOW.md) - Financial management
- [docs/MIGRATION_GUIDE.md](docs/MIGRATION_GUIDE.md) - Migrate from old tools

**Examples:**
- [examples/](examples/) - Sample files and outputs

---

## Key Advantages

### vs. Old Tools
- ✅ **One tool** instead of many (mdcon, mdclean, mdclean_simple)
- ✅ **Better structure detection** (Unstructured.io vs bash heuristics)
- ✅ **Integrated workflow** (no intermediate files)
- ✅ **CSV support** (financial management)
- ✅ **Consistent output** (standardized frontmatter)

### vs. Cloud Services
- ✅ **Privacy** - All data stays local
- ✅ **No subscriptions** - Free forever
- ✅ **Local AI** - Ollama instead of cloud APIs
- ✅ **No vendor lock-in** - Plain markdown files

### vs. Manual Processing
- ✅ **Automated structure detection**
- ✅ **AI-powered cleanup**
- ✅ **Batch processing**
- ✅ **Consistent formatting**

---

## Dependencies

**Python packages:**
```
ollama>=0.1.0              # LLM interface
unstructured[all-docs]     # Document structure
pytesseract>=0.3.10        # OCR wrapper
pandas>=2.0.0              # CSV processing
```

**System tools:**
```bash
brew install tesseract      # OCR engine
brew install ghostscript    # PDF to images
brew install poppler        # PDF text extraction
brew install pandoc         # Document conversion
brew install ffmpeg         # Audio conversion
brew install ollama         # Local LLM
```

---

## Status

**✅ Ready Now:**
- Images (OCR)
- PDFs (text & scanned)
- Documents (EPUB, DOCX, HTML)
- CSV (financial management)
- Text cleanup

**🔄 In Progress:**
- Audio transcription integration
- Automatic AI analysis in pipeline

**🔮 Planned:**
- Config file support
- Custom templates
- Wikilink generation
- Tag extraction from content

---

## Replaces These Tools

**From convert_to_markdown/:**
- ❌ `mdcon` (bash) → ✅ mdclean_universal.py
- ❌ `mdclean` (bash) → ✅ mdclean_universal.py

**From mp3_txt/:**
- ❌ `mdclean.py` → ✅ mdclean_universal.py
- ❌ `mdclean_simple.py` → ✅ mdclean_universal.py
- ⚠️ `transcribe` - Keep for now (audio integration coming)

**New capabilities:**
- ✅ CSV financial management (completely new!)
- ✅ Enhanced OCR with preprocessing
- ✅ Better structure detection

---

## Support

**Issues:** Open an issue on GitHub
**Questions:** See docs/ folder
**Migration:** See [docs/MIGRATION_GUIDE.md](docs/MIGRATION_GUIDE.md)

---

## License

Free for personal use.

---

**Created:** 2025-11-13
**Status:** ✅ Production Ready
**Version:** 1.0.0

#document-processing #knowledge-management #ocr #transcription #financial #ollama #privacy
