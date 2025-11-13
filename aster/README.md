# ✨ Aster

**Navigate your constellation of knowledge**

> "Lost in a night-sky of notes? Aster lights the way."

Transform scattered documents into a connected constellation - organize, link, and distill any source into structured knowledge that guides you.

---

## 🌟 What Is Aster?

Aster is your personal knowledge navigator. It ingests documents, images, audio, and data from anywhere - your iPhone, Mac, or browser - and weaves them into clean, connected markdown ready for your knowledge base.

**Process from anywhere:**
- 📱 iPhone (web interface or shortcuts)
- 💻 Mac (command line or web)
- 🌐 Any browser
- 🔗 Obsidian, Notion, or plain markdown

**Any format:**
```
📸 Photos → 🎙️ Audio → 📄 PDFs → 💼 Excel → 📝 Text → ✨ Connected Knowledge
```

---

## 🚀 Quick Start (iPhone-First)

### Step 1: Start Aster on Your Mac

```bash
cd aster

# Install dependencies
pip3 install -r requirements.txt
brew install tesseract poppler pandoc ollama ffmpeg

# Pull Ollama model
ollama pull llama3.2:1b

# Start web server
python3 aster_web.py
```

### Step 2: Access from iPhone

1. Note your Mac's IP (shown when server starts)
2. Open Safari on iPhone: `http://YOUR-MAC-IP:8888`
3. Drop files, watch magic happen!

**That's it!** ✨

See [IPHONE_INTEGRATION.md](docs/IPHONE_INTEGRATION.md) for iOS Shortcuts and advanced features.

---

## 📚 Supported Formats

### Documents
- **PDF**: Books, papers, scanned documents (with OCR)
- **Office**: DOCX, PPTX, Excel
- **Ebooks**: EPUB
- **Web**: HTML pages

### Media
- **Images**: JPG, PNG (OCR extracts text)
- **Audio**: MP3, M4A, WAV, WMA (transcription)

### Data
- **CSV/Excel**: Financial analysis with Ollama
- **Text**: TXT, Markdown (cleanup and structuring)

### Special Features
- **Multilingual**: Excellent Afrikaans support
- **Financial**: Auto-analyze transactions, budgets
- **Handwritten**: OCR for handwritten notes
- **Scanned**: Handle scanned PDFs

---

## 🎯 Use Cases

### Personal Knowledge Management
```bash
# Process book to your vault
aster "Deep Work.pdf" --preset book -o ~/Vault/Books/

# OCR handwritten meeting notes
aster whiteboard.jpg --preset ocr -o ~/Vault/Meetings/

# Transcribe lecture
aster lecture.mp3 --preset transcribe -o ~/Vault/Classes/
```

### Financial Management
```bash
# Analyze bank statement (locally, private)
aster transactions.csv --preset financial --analyze

# Result: Markdown with:
# - Income/expense breakdown
# - Category analysis
# - AI insights from Ollama
# - Obsidian math formulas
```

### From iPhone
1. Take photo of receipt
2. Share → Process with Aster
3. Appears in Obsidian vault
4. Tagged and structured!

---

## 🎨 Philosophy: Navigation as Clarity

Aster isn't just another document converter. It's a **lodestar** in your expanding night-sky of information:

### Traditional Tools
❌ Convert file → Done
❌ Each tool for each format
❌ No connection between items
❌ Search but don't discover

### Aster Approach
✅ Extract → Structure → Clean → **Connect**
✅ One tool for all formats
✅ Find relationships and patterns
✅ Navigate from facts to wisdom

**Metaphor:** Your notes are scattered stars. Aster reveals the constellations - the patterns, paths, and meaning hidden in plain sight.

---

## 🏗️ Architecture

### Pipeline
```
Input → Extract → Structure → Clean → Connect → Navigate
         ↓         ↓          ↓         ↓          ↓
      OCR/Parse  Unstructured Ollama  Metadata  Knowledge
```

**1. Extract** - Get text from any source
- OCR for images (Tesseract/PaddleOCR)
- Parse documents (Unstructured.io)
- Transcribe audio (Vosk)

**2. Structure** - Detect semantic elements
- Headings and hierarchy
- Lists, tables, quotes
- Paragraphs and sections

**3. Clean** - AI-powered refinement
- Fix OCR errors
- Add punctuation
- Improve formatting
- Preserve accuracy

**4. Connect** - Build relationships
- Generate metadata
- Extract tags
- Link references
- Calculate insights

**5. Navigate** - Make it useful
- Obsidian-ready frontmatter
- Backlink suggestions
- Math formulas
- Action items

---

## 💻 Usage

### Command Line

```bash
# Basic usage
aster document.pdf

# With options
aster book.pdf --preset book --model llama3.2:3b -o ~/Vault/Books/

# Batch processing
aster --batch ~/Documents/to-process/

# CSV with AI analysis
aster expenses.csv --analyze --preset financial
```

### Web Interface

```bash
# Start server
python3 aster_web.py

# Access from:
# - Mac: http://localhost:8888
# - iPhone: http://YOUR-MAC-IP:8888
# - Anywhere: http://TAILSCALE-IP:8888 (with Tailscale)
```

### iOS Shortcuts

Create "Process with Aster" shortcut:
- Select file in Files app
- Share → **Process with Aster**
- Get notification when done
- File appears in vault!

See [IPHONE_INTEGRATION.md](docs/IPHONE_INTEGRATION.md) for setup.

---

## ⚙️ Presets

Optimized workflows for common tasks:

### `--preset book`
- Detect chapters as H1
- Preserve references
- Maintain quotes
- Use llama3.2:3b

### `--preset ocr`
- Aggressive OCR cleanup
- Fix common errors
- Structure paragraphs
- Fast processing

### `--preset transcribe`
- Audio → text
- Add timestamps
- Speaker detection
- Punctuation

### `--preset financial`
- CSV/Excel analysis
- Calculate totals
- Category breakdown
- Obsidian math formulas
- AI insights

### `--preset afrikaans_religious`
- Preserve proper nouns
- Keep theological terms
- Maintain liturgy format
- Biblical references intact

**Create your own!** See `tests/prompts/` for examples.

---

## 🔧 Installation

### System Requirements
- macOS, Linux, or Windows
- Python 3.8+
- 4GB+ RAM
- Ollama (for AI features)

### Full Setup

```bash
# Clone repository
git clone https://github.com/yourusername/aster.git
cd aster

# Install Python packages
pip3 install -r requirements.txt

# Install system tools (macOS)
brew install pandoc poppler tesseract ffmpeg ollama

# Install and start Ollama
ollama serve
ollama pull llama3.2:1b  # Fast (1.3GB)
ollama pull llama3.2:3b  # Better quality (2GB)

# Test it
python3 aster.py tests/sample.pdf
```

### For iPhone Access

```bash
# Additional web dependencies (included in requirements.txt)
pip3 install fastapi uvicorn python-multipart

# Start web server
python3 aster_web.py
```

---

## 📖 Documentation

- **[IPHONE_INTEGRATION.md](docs/IPHONE_INTEGRATION.md)** - Complete iPhone setup
- **[OLLAMA_PROMPTS.md](docs/OLLAMA_PROMPTS.md)** - Optimize AI prompts
- **[TRAINING_DATA_GUIDE.md](docs/TRAINING_DATA_GUIDE.md)** - Add your documents
- **[RESEARCH_INTEGRATION_OPPORTUNITIES.md](docs/RESEARCH_INTEGRATION_OPPORTUNITIES.md)** - Latest tools
- **[PRODUCT_ROADMAP.md](docs/PRODUCT_ROADMAP.md)** - Future plans

---

## 🎓 Examples

### Example 1: Book Notes
```bash
# Input: Cal Newport - Deep Work.pdf
aster "Deep Work.pdf" --preset book

# Output: Deep Work.md
---
source: Deep Work.pdf
type: book
tags: [productivity, focus, deep-work]
---

# Deep Work

## Part 1: The Idea

### Chapter 1: Deep Work is Valuable

In the new economy, three groups will have a particular advantage...
```

### Example 2: Financial Analysis
```bash
# Input: transactions.csv
aster transactions.csv --analyze --preset financial

# Output: transactions.md (with AI insights)
## Summary
**Total Income:** $4,000.00
**Total Expenses:** $1,863.28
**Net:** $2,136.72

## AI Analysis
Based on your spending patterns, here are key insights:
- Food expenses (32%) are higher than average
- Consider meal planning to reduce dining out costs
- Savings rate of 53% is excellent

## Math Notes
Savings rate: `$= (2136.72 / 4000.00) * 100`%
```

### Example 3: Meeting Notes (iPhone)
1. Take photo of whiteboard
2. Share → "Process with Aster"
3. Result in Obsidian:

```markdown
---
source: IMG_1234.jpg
type: meeting-notes
date: 2025-11-13
tags: [meeting, planning]
---

# Project Planning Meeting

## Action Items
- [ ] Complete user research by Friday
- [ ] Schedule follow-up with design team
- [ ] Review budget proposal

## Key Decisions
- Moving forward with Option B
- Timeline: 6 weeks
```

---

## 🔒 Privacy & Security

**All processing happens locally:**
- ✅ No cloud uploads
- ✅ No data collection
- ✅ Ollama runs on your machine
- ✅ iPhone → Mac direct connection
- ✅ Sensitive documents stay private

**Perfect for:**
- Financial documents
- Medical records
- Legal papers
- Personal journals
- Client information

---

## 🚧 Roadmap

### ✅ Phase 1: Foundation (Complete)
- Core document processing
- Ollama integration
- Test suite
- iPhone web access

### 🔄 Phase 2: Enhancement (In Progress)
- Full Unstructured integration
- PaddleOCR (multilingual)
- Content-type detection
- Preset system

### 📅 Phase 3: Advanced (Planned)
- Native iOS app
- Tailscale integration
- Desktop GUI (Tauri)
- Plugin ecosystem

See [PRODUCT_ROADMAP.md](docs/PRODUCT_ROADMAP.md) for details.

---

## 🤝 Contributing

Aster is designed for personal use but contributions welcome!

**Areas for contribution:**
- New presets for different document types
- Improved OCR for specific languages
- Integration with knowledge management tools
- Documentation and examples

---

## 📜 License

MIT License - use freely, modify as needed.

---

## 🙏 Acknowledgments

Built on the shoulders of giants:
- **Unstructured.io** - Document structure detection
- **Ollama** - Local AI inference
- **Tesseract/PaddleOCR** - OCR engines
- **FastAPI** - Web framework

Inspired by:
- The night sky and navigation by stars
- Obsidian's connected thought philosophy
- The desire to make sense of chaos

---

## ✨ Happy Navigating!

Questions? Issues? Ideas?

Create an issue or reach out!

---

**Aster** - *Find your guiding note*
