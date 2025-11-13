# Exporting Aster to Another Computer

This guide explains how to package and transfer Aster to a fresh computer.

---

## 📦 What to Export

### Method 1: Git Clone (Recommended)

The simplest way is to have the recipient clone directly from your repository:

```bash
git clone <your-repository-url> aster
cd aster
./install.sh
```

### Method 2: ZIP Archive

If you need to transfer without git:

**On your current computer:**
```bash
# Navigate to parent directory
cd /Users/mac/Documents/Applications/repos

# Create a clean export (excludes unnecessary files)
zip -r aster-export.zip aster \
  -x "aster/venv/*" \
  -x "aster/__pycache__/*" \
  -x "aster/**/__pycache__/*" \
  -x "aster/.git/*" \
  -x "aster/uploads/*" \
  -x "aster/outputs/*" \
  -x "aster/tests/outputs/*" \
  -x "aster/tests/training_outputs/*" \
  -x "aster/**/*.pyc" \
  -x "aster/.DS_Store"

# Result: aster-export.zip (~5-10MB)
```

**On the new computer:**
```bash
# Extract the archive
unzip aster-export.zip
cd aster

# Run the installer
chmod +x install.sh
./install.sh
```

---

## 📋 What's Included in Export

### Core Files (Always Include)
```
aster/
├── aster.py                    # Main CLI script
├── aster_web.py                # Web server
├── aster_web                   # Launcher script
├── requirements.txt            # Python dependencies
├── install.sh                  # Automated installer
├── README.md                   # Project documentation
├── INSTALL.md                  # Installation guide
├── EXPORT_GUIDE.md            # This file
├── LICENSE                     # License file
├── .gitignore                  # Git ignore rules
├── docs/                       # Documentation folder
│   ├── IPHONE_INTEGRATION.md
│   ├── TRAINING_DATA_GUIDE.md
│   └── RESEARCH_*.md
└── tests/                      # Test files and structure
    ├── run_tests.py
    ├── README_TESTING.md
    ├── [sample test files]
    └── training_data/
        └── README.md
```

### What NOT to Include
```
❌ venv/                        # Virtual environment (regenerated on new system)
❌ __pycache__/                 # Python cache (regenerated)
❌ .git/                        # Git history (optional, can include if needed)
❌ uploads/                     # Temporary uploads
❌ outputs/                     # Generated outputs
❌ tests/outputs/               # Test outputs
❌ tests/training_outputs/      # Training outputs
❌ .DS_Store                    # macOS metadata
❌ *.pyc                        # Compiled Python files
```

---

## 🚀 Installation on New Computer

### Prerequisites

The new computer needs:
- **macOS** (10.15+) or **Linux** (Ubuntu 20.04+)
- **Internet connection** (for downloading dependencies)
- **~5GB free space** (for dependencies and models)
- **Admin/sudo access** (for system packages)

### Installation Steps

1. **Transfer the files** (git clone or extract ZIP)

2. **Run the automated installer:**
   ```bash
   cd aster
   chmod +x install.sh
   ./install.sh
   ```

3. **The installer will:**
   - Install Homebrew (macOS) or update apt (Linux)
   - Install Python 3.12
   - Install Tesseract OCR (163 languages)
   - Install Poppler, Pandoc, FFmpeg
   - Install Ollama
   - Create Python virtual environment
   - Install all Python packages (~500MB)
   - Download NLTK data
   - Download Ollama models (1.3GB)
   - Create directory structure
   - Test the installation

4. **Start using Aster:**
   ```bash
   # Test CLI
   ./aster.py tests/Year\ A\ 2022-2023.xlsx -o /tmp/test.md

   # Start web server
   ./aster_web
   ```

---

## ⏱️ Installation Time

- **Fast internet (100+ Mbps):** 15-20 minutes
- **Medium internet (25-50 Mbps):** 30-45 minutes
- **Slow internet (10 Mbps):** 60-90 minutes

Most time is spent downloading:
- Ollama model (1.3GB)
- Python packages (~500MB)
- System packages (~200MB)

---

## 🐛 Troubleshooting

### Installation fails on step X

Check the error message and refer to INSTALL.md "Troubleshooting" section.

### Missing Homebrew (macOS)

The installer will install it automatically, but if manual installation is needed:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Python 3.12 not found

**macOS:**
```bash
brew install python@3.12
```

**Linux:**
```bash
sudo apt install python3.12 python3.12-venv
```

### Ollama not starting

**macOS:**
```bash
brew services restart ollama
```

**Linux:**
```bash
sudo systemctl restart ollama
```

---

## 📝 Notes for Recipients

### First Time Setup Checklist

- [ ] Extract/clone Aster files
- [ ] Run `./install.sh`
- [ ] Test with sample file
- [ ] Configure iPhone (scan QR code)
- [ ] Import training data (optional)
- [ ] Bookmark web interface on iPhone

### System Requirements

**Minimum:**
- 4GB RAM
- 5GB free disk space
- macOS 10.15+ or Ubuntu 20.04+

**Recommended:**
- 8GB+ RAM (for faster LLM processing)
- 10GB free disk space
- macOS 13+ or Ubuntu 22.04+

### Performance Notes

- **LLM Speed:** Depends on CPU
  - M1/M2 Mac: Very fast (2-5 sec per page)
  - Intel Mac: Fast (5-10 sec per page)
  - Linux: Varies by CPU
- **Model Options:**
  - llama3.2:1b (1.3GB) - Recommended, good quality
  - qwen2.5:0.5b (397MB) - Faster, slightly lower quality
  - llama3.2:3b (2.0GB) - Slower, best quality (may be slow on older hardware)

---

## 🔒 Privacy Note

All processing happens locally:
- ✅ No cloud uploads
- ✅ No API keys needed
- ✅ No tracking
- ✅ Complete privacy

Your documents never leave your computer (unless you explicitly export them).

---

## 📞 Support

If the recipient has issues:

1. Check INSTALL.md troubleshooting section
2. Verify all prerequisites are met
3. Check system compatibility
4. Try manual installation steps if automated installer fails

---

## ✅ Verification

After installation, verify everything works:

```bash
# 1. Check Python packages
python3 -c "import pandas, unstructured, ollama; print('✓ Packages OK')"

# 2. Check Tesseract
tesseract --list-langs | wc -l  # Should show 100+

# 3. Check Ollama
ollama list  # Should show llama3.2:1b

# 4. Test processing
./aster.py tests/Year\ A\ 2022-2023.xlsx -o /tmp/test.md

# 5. Test web server
./aster_web  # Should show QR code
```

All checks should pass ✓

---

## 🎉 Ready to Use

Once installed, the recipient can:
- Process documents from CLI
- Upload from iPhone via web interface
- Organize training data
- Run batch processing
- Customize prompts and settings

Enjoy navigating your constellation of knowledge! ✨
