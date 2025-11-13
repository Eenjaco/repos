# Migration Guide - mdclean_universal

**From:** Legacy tools (mdcon, mdclean bash, mdclean_simple.py, etc.)
**To:** mdclean_universal.py
**Date:** 2025-11-13

---

## Why Migrate?

**Benefits of mdclean_universal:**
- ✅ Single tool for all document types
- ✅ Better structure detection (Unstructured.io)
- ✅ Optimized LLM processing (Ollama 3.2 1B)
- ✅ Automatic KM formatting
- ✅ Batch processing built-in
- ✅ Consistent output format
- ✅ Easier maintenance

---

## Quick Migration Cheatsheet

| Old Command | New Command |
|-------------|-------------|
| `mdcon document.pdf` | `mdclean_universal.py document.pdf` |
| `mdclean original.pdf raw.md` | `mdclean_universal.py document.pdf` |
| `python3 mdclean_simple.py input.md output.md` | `mdclean_universal.py input.md` |
| `./transcribe → mdclean_simple.py` | `mdclean_universal.py audio.mp3` |
| `mdcon --batch folder/` | `mdclean_universal.py --batch folder/` |

---

## Detailed Migration Scenarios

### Scenario 1: PDF Conversion (mdcon → mdclean)

**Old workflow:**
```bash
# Step 1: Convert to raw markdown
cd /path/to/convert_to_markdown
./mdcon document.pdf  # Creates document-raw.md

# Step 2: Clean the raw markdown
./mdclean document.pdf document-raw.md  # Creates document.md
```

**New workflow:**
```bash
# Single step
cd /path/to/repos
./mdclean_universal.py document.pdf  # Creates document_processed.md
```

**What changed:**
- ❌ No more two-step process
- ❌ No more `-raw.md` intermediate files
- ✅ Single command
- ✅ Better structure detection
- ✅ Automatic frontmatter

### Scenario 2: Audio Transcription + Cleaning

**Old workflow:**
```bash
# Step 1: Transcribe audio
cd /path/to/mp3_txt
./transcribe  # Drag-drop audio.mp3 → audio.md

# Step 2: Clean transcript
python3 mdclean_simple.py audio.md cleaned.md
```

**New workflow:**
```bash
# Single step (when audio transcription is fully integrated)
cd /path/to/repos
./mdclean_universal.py audio.mp3  # Creates audio_processed.md
```

**Current workaround** (until audio integration complete):
```bash
# Step 1: Use existing transcribe (for now)
cd /path/to/mp3_txt
./transcribe  # Creates audio.md

# Step 2: Process with universal tool
cd /path/to/repos
./mdclean_universal.py ../mp3_txt/audio.md
```

### Scenario 3: Image OCR

**Old workflow:**
```bash
# Using mdcon
cd /path/to/convert_to_markdown
./mdcon photo.jpg  # Creates photo-raw.md
./mdclean photo.jpg photo-raw.md  # Creates photo.md
```

**New workflow:**
```bash
cd /path/to/repos
./mdclean_universal.py photo.jpg  # Creates photo_processed.md

# With handwriting mode
./mdclean_universal.py handwritten.jpg --handwriting
```

**Advantages:**
- ✅ Better image preprocessing
- ✅ Handwriting mode support
- ✅ Better OCR error correction (LLM)

### Scenario 4: Plain Text Cleanup

**Old workflow:**
```bash
cd /path/to/mp3_txt
python3 mdclean_simple.py input.txt output.md --model qwen2.5:0.5b
```

**New workflow:**
```bash
cd /path/to/repos
./mdclean_universal.py input.txt  # Uses llama3.2:1b by default

# Or specify model
./mdclean_universal.py input.txt --model qwen2.5:0.5b
```

### Scenario 5: Batch Processing

**Old workflow (mdcon):**
```bash
cd /path/to/convert_to_markdown
./mdcon --batch ~/Documents/inbox/

# Then separately clean each file
./mdclean --auto ~/Documents/inbox/
```

**New workflow:**
```bash
cd /path/to/repos
./mdclean_universal.py --batch ~/Documents/inbox/
# → Creates ~/Documents/inbox/processed/ with all cleaned files
```

---

## Configuration Migration

### Old mdclean_simple Config

**Old:** Command-line options every time
```bash
python3 mdclean_simple.py input.md output.md --model llama3.2:1b
```

**New:** Use defaults or config file (future)
```bash
# Uses sensible defaults
./mdclean_universal.py input.md

# Override when needed
./mdclean_universal.py input.md --model qwen2.5:0.5b
```

### Future Config File Support

**Location:** `~/.mdclean/config.yaml`

```yaml
ollama:
  model: "llama3.2:1b"
  temperature: 0.2

ocr:
  language: "eng"
  handwriting_mode: false

output:
  add_frontmatter: true
  default_dir: "~/Documents/Vault/Inbox/"
```

---

## Output Format Changes

### Old Output (mdcon + mdclean)

**mdcon output** (`document-raw.md`):
```markdown
# Document Title

> Converted from PDF on 2025-11-13

<!-- Page 1 -->

raw unformatted text here...
```

**mdclean output** (`document.md`):
```markdown
# Document Title

> Converted from PDF on 2025-11-13

## Section 1

Cleaned text with proper formatting.
```

### New Output (mdclean_universal)

**Single output** (`document_processed.md`):
```markdown
---
source: document.pdf
date_processed: 2025-11-13T14:30:00
type: pdf
tags: [pdf, document]
---

# Document Title

## Section 1

Cleaned text with proper formatting, structure detection, and LLM improvements.
```

**Key improvements:**
- ✅ YAML frontmatter (Obsidian/Zettelkasten ready)
- ✅ Metadata automatically extracted
- ✅ Better structure detection
- ✅ Consistent naming (`_processed.md`)

---

## File Organization After Migration

### Recommended Directory Structure

**Before:**
```
Documents/
├── convert_to_markdown/     # Old bash tools
│   ├── mdcon
│   ├── mdclean
│   └── document-raw.md      # Intermediate files
├── mp3_txt/                 # Old Python tools
│   ├── mdclean_simple.py
│   └── transcriptions/
```

**After:**
```
Documents/
├── repos/                   # New unified tool
│   ├── mdclean_universal.py
│   └── archive/             # Old tools archived
│       ├── convert_to_markdown/
│       └── mp3_txt/
├── Vault/Inbox/            # Clean outputs
│   ├── document_processed.md
│   ├── photo_processed.md
│   └── audio_processed.md
```

---

## Archive Strategy

### What to Archive

**Archive these files** (keep for reference, but stop using):

From `convert_to_markdown/`:
- ✅ `mdcon` (bash)
- ✅ `mdclean` (bash)
- ✅ `mdcon_batch` (bash)
- ✅ `pdf_to_md.sh`
- ✅ `pdf_to_md_interactive.sh`

From `mp3_txt/`:
- ✅ `mdclean.py` (old full version)
- ✅ `mdclean_simple.py` (absorbed into universal)
- ⚠️ `mdclean_claude.py` (KEEP as backup for high-quality API option)
- ⚠️ `transcribe` (KEEP until audio integration complete)
- ⚠️ `transcribe_vosk_stream.py` (KEEP until audio integration complete)

### Archive Commands

```bash
# Create archive directory
mkdir -p ~/repos/archive/

# Archive convert_to_markdown tools
mkdir -p ~/repos/archive/convert_to_markdown/
mv ~/repos/convert_to_markdown/mdcon ~/repos/archive/convert_to_markdown/
mv ~/repos/convert_to_markdown/mdclean ~/repos/archive/convert_to_markdown/
mv ~/repos/convert_to_markdown/mdcon_batch ~/repos/archive/convert_to_markdown/

# Archive mp3_txt tools (keep transcribe for now)
mkdir -p ~/repos/archive/mp3_txt/
mv ~/repos/mp3_txt/mdclean.py ~/repos/archive/mp3_txt/
mv ~/repos/mp3_txt/mdclean_simple.py ~/repos/archive/mp3_txt/

# Create README in archive
cat > ~/repos/archive/README.md << 'EOF'
# Archived Tools

These tools have been replaced by `mdclean_universal.py`.

## Archived on: 2025-11-13

### Replaced Tools
- `convert_to_markdown/mdcon` → `mdclean_universal.py`
- `convert_to_markdown/mdclean` → `mdclean_universal.py`
- `mp3_txt/mdclean.py` → `mdclean_universal.py`
- `mp3_txt/mdclean_simple.py` → `mdclean_universal.py`

### Still Active
- `mp3_txt/transcribe` - Until audio integration complete
- `mp3_txt/mdclean_claude.py` - Backup for high-quality API processing

See MIGRATION_GUIDE.md for migration instructions.
EOF
```

---

## Testing Your Migration

### Test Plan

**1. Test basic file types:**
```bash
# Create test directory
mkdir ~/test_migration

# Test text file
echo "this is a test file with no punctuation or capitals" > ~/test_migration/test.txt
./mdclean_universal.py ~/test_migration/test.txt
# ✓ Check output has proper punctuation and frontmatter

# Test PDF (if you have one)
./mdclean_universal.py ~/Documents/sample.pdf
# ✓ Check output is clean markdown

# Test image (if you have one)
./mdclean_universal.py ~/Pictures/notes.jpg
# ✓ Check OCR extracted text correctly
```

**2. Test batch processing:**
```bash
# Create batch test
mkdir ~/test_migration/batch_test
cp ~/test_migration/test.txt ~/test_migration/batch_test/
cp ~/Documents/*.pdf ~/test_migration/batch_test/  # Copy some PDFs

./mdclean_universal.py --batch ~/test_migration/batch_test/
# ✓ Check all files processed
# ✓ Check output in batch_test/processed/
```

**3. Compare with old tools:**
```bash
# Process same file with old and new
cd ~/repos/convert_to_markdown
./mdcon ~/Documents/sample.pdf  # → sample-raw.md
./mdclean ~/Documents/sample.pdf sample-raw.md  # → sample.md

cd ~/repos
./mdclean_universal.py ~/Documents/sample.pdf  # → sample_processed.md

# Compare outputs
diff ~/repos/convert_to_markdown/sample.md ~/repos/sample_processed.md
# ✓ New version should have better structure, frontmatter
```

---

## Troubleshooting Migration Issues

### Issue: "Module 'unstructured' not found"
**Solution:**
```bash
pip install 'unstructured[all-docs]'
```

### Issue: "Tesseract not found" (OCR)
**Solution:**
```bash
brew install tesseract
```

### Issue: "pdftotext not found" (PDF parsing)
**Solution:**
```bash
brew install poppler
```

### Issue: "Ollama not available"
**Solution:**
```bash
brew install ollama
ollama pull llama3.2:1b
```

### Issue: Output quality not as good as Claude API
**Solution:**
```bash
# Use the old mdclean_claude.py for critical documents
cd ~/repos/mp3_txt
python3 mdclean_claude.py important_document.md output.md
```

### Issue: Missing audio transcription
**Status:** Audio integration is next phase

**Current workaround:**
```bash
# Use existing transcribe, then process
cd ~/repos/mp3_txt
./transcribe  # Creates transcript.md

cd ~/repos
./mdclean_universal.py ~/repos/mp3_txt/transcript.md
```

---

## Rollback Plan

If you need to revert to old tools:

```bash
# Restore from archive
mv ~/repos/archive/convert_to_markdown/* ~/repos/convert_to_markdown/
mv ~/repos/archive/mp3_txt/* ~/repos/mp3_txt/

# Make executable again
chmod +x ~/repos/convert_to_markdown/mdcon
chmod +x ~/repos/convert_to_markdown/mdclean
```

---

## Timeline

**Phase 1:** ✅ Core tool ready (text, PDF, images, documents, HTML)
**Phase 2:** ⏳ Audio transcription integration
**Phase 3:** ⏳ Config file support
**Phase 4:** ⏳ Advanced features (wikilinks, custom templates)

**Recommendation:** Start using `mdclean_universal.py` now for all non-audio tasks. Continue using existing `transcribe` for audio until Phase 2 complete.

---

## Support

If you encounter issues during migration:
1. Check this guide
2. Review [README_mdclean_universal.md](README_mdclean_universal.md)
3. See [ENHANCEMENT_PROPOSAL.md](ENHANCEMENT_PROPOSAL.md) for technical details

---

## Summary

**What to do now:**
1. ✅ Install dependencies: `pip install -r requirements_universal.txt`
2. ✅ Install system tools: `brew install tesseract ghostscript poppler pandoc`
3. ✅ Test with sample files: `./mdclean_universal.py test.txt`
4. ✅ Update workflows to use new tool
5. ✅ Archive old tools (after testing)
6. ⏳ Wait for audio integration (use existing transcribe for now)

**Migration complete when:**
- ✅ All document types processing successfully
- ✅ Output quality meets or exceeds old tools
- ✅ Batch processing working
- ✅ Old tools archived
- ✅ Workflows updated

---

**Status:** 🚀 Ready to migrate
**Last Updated:** 2025-11-13
