# Testing Framework for mdclean_universal

## Overview

This directory contains a comprehensive testing framework for mdclean_universal with 16 diverse test files covering all major document types.

## Quick Start

```bash
# 1. Install system dependencies (Mac)
brew install pandoc poppler tesseract ffmpeg

# 2. Install Python dependencies
pip3 install -r ../requirements.txt

# 3. Make sure Ollama is running with the model
ollama pull llama3.2:1b

# 4. Run the full test suite
python3 run_tests.py
```

## Test Files (16 total)

### By Category

| Category | Count | Files | Status |
|----------|-------|-------|--------|
| PDF | 7 | Books, newsletters, music scores | ✅ Supported |
| DOCX | 2 | Church documents (Afrikaans) | ✅ Supported |
| JPEG | 2 | Photos/documents (OCR) | ✅ Supported |
| HTML | 1 | Church website | ✅ Supported |
| EPUB | 1 | Biography | ✅ Supported |
| XLSX | 1 | Calendar/data | ✅ Added (needs pandas) |
| WMA | 1 | Audio | ✅ Added (needs ffmpeg) |
| PPTX | 1 | Presentation | ✅ Added (needs pandoc) |

### By Language

- **Afrikaans**: 5 files (religious content)
- **English**: 11 files (books, documents, images)

### By Size

- **Small** (< 100KB): 4 files
- **Medium** (100KB - 1MB): 9 files
- **Large** (> 1MB): 3 files

## Test Infrastructure

### Files Created

1. **`run_tests.py`** - Automated test runner
   - Processes all files systematically
   - Measures processing time
   - Generates comprehensive reports
   - Saves results in JSON and Markdown

2. **`TEST_ANALYSIS.md`** - Test file analysis
   - Categorizes all test files
   - Identifies format support gaps
   - Documents expected challenges
   - Defines success criteria

3. **`TEST_RESULTS.md`** - Generated test report
   - Summary statistics
   - Results by category
   - Individual file results
   - Recommendations

4. **`test_results.json`** - Machine-readable results
   - Complete test data
   - Processing times
   - Error messages
   - Output metrics

5. **`SETUP_GUIDE.md`** - Environment setup instructions
   - System dependencies
   - Python packages
   - Ollama configuration
   - Troubleshooting

6. **`OLLAMA_PROMPTS.md`** - Prompt optimization guide
   - Specialized prompts for each content type
   - Model-specific settings
   - Integration examples
   - Validation strategies

7. **`outputs/`** - Generated markdown files
   - One output file per test file
   - Contains processed content
   - Includes frontmatter and structure

## Recent Improvements

### Format Support Added

1. **Excel (.xlsx, .xls)**
   ```python
   # Now handles Excel files like CSV
   ./mdclean_universal.py "Year A 2022-2023.xlsx" --analyze
   ```

2. **Windows Media Audio (.wma)**
   ```python
   # Converts to .wav using ffmpeg before transcription
   ./mdclean_universal.py "01 Track 1.wma" -o output.md
   ```

3. **PowerPoint (.pptx, .ppt)**
   ```python
   # Uses pandoc for conversion
   ./mdclean_universal.py "02 Jun 2024.pptx" -o output.md
   ```

### Dependencies Required

New dependencies for format support:

```bash
# Python packages
pip3 install pandas openpyxl

# System tools
brew install ffmpeg  # For .wma audio conversion
```

## Running Tests

### Full Test Suite

```bash
python3 tests/run_tests.py
```

**Expected Output:**
- Progress for each of 16 files
- Processing time per file
- Success/failure status
- Generated reports in tests/

### Individual File Testing

```bash
# Test single file
./mdclean_universal.py "tests/Cal Newport - Deep Work.pdf"

# With specific output
./mdclean_universal.py "tests/Cal Newport - Deep Work.pdf" -o "tests/outputs/deep_work.md"

# With AI analysis
./mdclean_universal.py "tests/Cal Newport - Deep Work.pdf" --analyze

# Specify model
./mdclean_universal.py "tests/Cal Newport - Deep Work.pdf" --model llama3.2:3b
```

### Batch Testing

```bash
# Process all files in tests/ directory
./mdclean_universal.py --batch tests/
```

## Expected Results (with dependencies installed)

| Format | Expected Success Rate | Notes |
|--------|----------------------|-------|
| PDF | 100% | May have issues with music scores (graphical) |
| DOCX | 100% | Large files may be slow |
| JPEG | 100% | Quality depends on image clarity |
| HTML | 100% | - |
| EPUB | 100% | - |
| XLSX | 100% | Requires pandas + openpyxl |
| WMA | ~80% | Requires ffmpeg (transcription not fully implemented) |
| PPTX | 100% | Requires pandoc |

## Analyzing Results

### Key Metrics

1. **Success Rate**: % of files processed without errors
2. **Processing Time**: Seconds per file (varies by size/type)
3. **Output Quality**: Subjective assessment of markdown quality
4. **Structure Preservation**: How well original structure is maintained
5. **Accuracy**: Correctness of extracted content

### Quality Assessment

For each output file in `outputs/`, check:

- ✅ **Frontmatter**: Contains source, date, type, tags
- ✅ **Headings**: Proper hierarchy (# ## ###)
- ✅ **Content**: Complete and accurate
- ✅ **Formatting**: Clean markdown syntax
- ✅ **Language**: Preserves multilingual content
- ✅ **Special Elements**: Tables, lists, quotes formatted correctly

### Common Issues

1. **Musical Scores** (VONKK PDFs)
   - Extract as gibberish (graphical notation)
   - Solution: Keep as PDF, extract metadata only

2. **Large Files** (NG Kerk Alma.docx - 5.9MB)
   - May be slow (30-60 seconds)
   - May trigger timeout in some configurations

3. **OCR Quality** (Images)
   - Depends on image clarity and text size
   - May need manual cleanup

4. **Afrikaans Content**
   - Ollama may struggle with proper nouns
   - Use specialized prompts (see OLLAMA_PROMPTS.md)

## Ollama Optimization

### Model Selection

**For Testing:**
```bash
# Fast, good for most content
ollama pull llama3.2:1b

# Better quality, slightly slower
ollama pull llama3.2:3b

# Best quality, slowest
ollama pull llama2:13b
```

### Specialized Prompts

See `OLLAMA_PROMPTS.md` for:
- Content-type detection
- Optimized prompts per document type
- Model-specific settings
- Integration examples

## Troubleshooting

### "pdftotext not installed"

```bash
brew install poppler
```

### "pandoc not installed"

```bash
brew install pandoc
```

### "Tesseract OCR not installed"

```bash
brew install tesseract
```

### "ffmpeg not installed"

```bash
brew install ffmpeg
```

### "No module named 'pandas'"

```bash
pip3 install pandas openpyxl
```

### "Ollama connection error"

```bash
# Start Ollama service
ollama serve

# In another terminal, pull model
ollama pull llama3.2:1b
```

### Tests All Failing

1. Check system dependencies are installed
2. Verify Python packages are installed
3. Ensure Ollama is running
4. Check file permissions
5. Review test_results.json for specific errors

## Continuous Improvement

### Adding New Test Files

```bash
# 1. Add file to tests/ directory
cp ~/Documents/newfile.pdf tests/

# 2. Run tests
python3 tests/run_tests.py

# 3. Review results
cat tests/TEST_RESULTS.md
```

### Improving Prompts

1. Identify problematic file types
2. Review outputs in outputs/ directory
3. Adjust prompts in OLLAMA_PROMPTS.md
4. Implement in mdclean_universal.py
5. Re-run tests and compare

### Performance Monitoring

Track over time:
- Processing time trends
- Success rate by format
- Common error patterns
- Output quality ratings

## Next Steps

1. **Run baseline tests** on your Mac with all dependencies
2. **Review results** and identify areas for improvement
3. **Implement content-type detection** using prompts from OLLAMA_PROMPTS.md
4. **Create specialized handlers** for problematic file types
5. **Add automated quality validation** (e.g., markdown linting)
6. **Expand test suite** with more diverse files
7. **Create regression tests** using pytest framework

## Files in This Directory

```
tests/
├── README_TESTING.md          # This file
├── TEST_ANALYSIS.md           # Test file analysis and planning
├── SETUP_GUIDE.md             # Environment setup instructions
├── OLLAMA_PROMPTS.md          # Prompt optimization guide
├── run_tests.py               # Automated test runner
├── TEST_RESULTS.md            # Generated test results (after running)
├── test_results.json          # JSON test data (after running)
├── outputs/                   # Generated markdown files (after running)
│   ├── Cal Newport - Deep Work.md
│   ├── First 90 Days.md
│   └── ...
└── [16 test files]            # Diverse document types
```

## Contributing Test Results

When you run tests:

1. Save TEST_RESULTS.md and test_results.json
2. Note any special observations
3. Document manual fixes needed
4. Share insights about Ollama prompt effectiveness
5. Suggest improvements to the test framework

## Support

For issues with:
- **Test framework**: Review run_tests.py and TEST_ANALYSIS.md
- **Dependencies**: See SETUP_GUIDE.md
- **Prompts**: See OLLAMA_PROMPTS.md
- **Format support**: Check mdclean_universal.py InputRouter class

## Summary

This testing framework provides:
- ✅ 16 diverse test files
- ✅ Automated test runner
- ✅ Comprehensive reporting
- ✅ Format support for all major types
- ✅ Optimization guides for Ollama prompts
- ✅ Clear setup instructions
- ✅ Quality assessment criteria

Ready to validate mdclean_universal against real-world content!
