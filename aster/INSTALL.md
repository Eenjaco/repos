# Aster - Complete Installation Guide

**Navigate your constellation of knowledge**

Complete setup guide for installing Aster on a fresh Mac or Linux system.

---

## 🚀 Quick Install (Mac)

```bash
# 1. Clone the repository
git clone <repository-url> aster
cd aster

# 2. Run the automated installer
./install.sh

# 3. Start the web server
./aster_web
```

Scan the QR code with your iPhone and start processing documents!

---

## 📋 What Gets Installed

### System Dependencies (via Homebrew/apt)
- **Python 3.12** - Stable Python version with full package support
- **Tesseract OCR** - Text extraction from images (163 languages including Afrikaans)
- **Poppler** - PDF text extraction
- **Pandoc** - Document format conversion
- **FFmpeg** - Audio format conversion
- **Ollama** - Local LLM inference

### Python Packages
- **FastAPI & Uvicorn** - Web server for iPhone/remote access
- **Ollama SDK** - LLM integration
- **Unstructured** - Document structure detection
- **Pandas & OpenPyXL** - Excel and CSV processing
- **Pytesseract** - Tesseract wrapper
- **Vosk & Soundfile** - Audio transcription
- **QRCode** - Terminal QR codes for easy iPhone connection

### NLTK Data
- punkt_tab, averaged_perceptron_tagger_eng - Text processing

### Ollama Models
- **llama3.2:1b** (1.3GB) - Fast, recommended for most uses
- Optional: qwen2.5:0.5b (397MB) - Even faster

---

## 🔧 Manual Installation

If the automated installer doesn't work, follow these steps:

### Step 1: Install System Dependencies

**macOS:**
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python@3.12 tesseract tesseract-lang poppler pandoc ffmpeg ollama

# Start Ollama service
brew services start ollama
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install -y python3.12 python3.12-venv tesseract-ocr tesseract-ocr-all \
    poppler-utils pandoc ffmpeg curl

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh
```

### Step 2: Set Up Python Environment

```bash
# Create virtual environment with Python 3.12
/usr/local/opt/python@3.12/bin/python3.12 -m venv venv  # macOS
# OR
python3.12 -m venv venv  # Linux

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install Python packages
pip install -r requirements.txt
pip install 'qrcode[pil]'
```

### Step 3: Download Ollama Models

```bash
# Download recommended model (required)
ollama pull llama3.2:1b

# Optional: Download faster model
ollama pull qwen2.5:0.5b
```

### Step 4: Download NLTK Data

```bash
python3 -c "import nltk; nltk.download('punkt_tab'); nltk.download('averaged_perceptron_tagger_eng')"
```

### Step 5: Make Scripts Executable

```bash
chmod +x aster.py aster_web
```

### Step 6: Test Installation

```bash
# Test with a sample file
python3 aster.py tests/Year\ A\ 2022-2023.xlsx -o /tmp/test.md --model llama3.2:1b

# If successful, start the web server
./aster_web
```

---

## 📱 iPhone Setup

Once the server is running:

1. **Scan the QR code** displayed in the terminal
2. **Bookmark the page** to your iPhone home screen for quick access
3. **Upload documents** directly from your iPhone (photos, files, etc.)
4. **Download processed files** as clean markdown

### For Access from Anywhere (Optional)

Install Tailscale for secure remote access:
```bash
brew install tailscale  # macOS
# OR
curl -fsSL https://tailscale.com/install.sh | sh  # Linux

# Start Tailscale
tailscale up

# Get your Tailscale IP
tailscale ip -4

# Access from anywhere: http://TAILSCALE-IP:8888
```

---

## 🎯 Quick Start Guide

### CLI Usage

```bash
# Process a single document
./aster.py document.pdf -o output.md

# Process with specific model
./aster.py document.pdf -o output.md --model llama3.2:1b

# Batch process a folder
./aster.py --batch ~/Documents/to-process/
```

### Web Interface Usage

```bash
# Start the server
./aster_web

# Scan QR code with iPhone
# Or visit: http://localhost:8888 on your Mac
```

---

## 🗂️ Training Data

Organize your documents for processing:

```bash
tests/training_data/
├── books/          # PDF books, EPUB files
├── newsletters/    # Newsletters, bulletins
├── religious/      # Church documents, sermons
├── financial/      # CSV budgets, receipts
├── technical/      # Technical docs, manuals
├── personal/       # Personal notes, journals
├── audio/          # MP3, WMA recordings
└── images/         # Photos of handwritten notes
```

Process all training data:
```bash
python3 tests/run_tests.py
```

---

## ⚙️ Configuration

### Default LLM Model

Edit `aster_web.py` to change default model:
```python
<option value="llama3.2:1b" selected>llama 3.2: 1B (fast)</option>
```

### Change Server Port

Edit `aster_web.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8888)  # Change 8888 to your port
```

---

## 🐛 Troubleshooting

### "Module not found" errors
```bash
# Ensure venv is activated
source venv/bin/activate
pip install -r requirements.txt
```

### Numpy ABI errors
```bash
# Reinstall with Python 3.12 (not 3.14)
rm -rf venv
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Tesseract language not found
```bash
# macOS
brew install tesseract-lang

# Linux
sudo apt install tesseract-ocr-all
```

### Ollama not responding
```bash
# macOS
brew services restart ollama

# Linux
sudo systemctl restart ollama
```

### Web interface "Processing failed"
Check Terminal 1 (where aster_web is running) for detailed error messages.

---

## 📚 Documentation

- **README.md** - Project overview
- **INSTALL.md** - This installation guide (you are here)
- **docs/IPHONE_INTEGRATION.md** - Detailed iPhone setup
- **docs/TRAINING_DATA_GUIDE.md** - Training data organization
- **tests/README_TESTING.md** - Testing guide

---

## ✨ Features

- **Multi-format Support**: PDF, DOCX, PPTX, XLSX, images, audio, EPUB, HTML
- **OCR**: 163 languages including Afrikaans
- **Audio Transcription**: Convert voice recordings to text
- **Local AI**: Privacy-first with Ollama (no cloud uploads)
- **iPhone Integration**: Upload and process from your phone
- **8-bit Retro UI**: Beautiful pixel-perfect interface
- **Obsidian Ready**: Generates markdown with frontmatter

---

## 🤝 Support

For issues, check the troubleshooting section above or create an issue in the repository.

---

## 📄 License

See LICENSE file for details.
