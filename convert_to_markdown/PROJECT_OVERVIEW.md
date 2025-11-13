# LLM-Enhanced Markdown Conversion Pipeline

## Goal

Create a self-improving, two-stage markdown conversion pipeline that uses local LLM analysis to iteratively enhance conversion quality. The system learns from each batch of conversions and suggests targeted improvements to the bash conversion scripts.

## Key Principles

### A. Organization for AI Discoverability
- Flat structure when possible — Keep conversion logs and analysis reports shallow (max 2-3 levels).
- Descriptive file names — Use clear names like `conversion.log`, `analysis_report.md`.
- Consistent naming — Use hyphens for output files: `document-raw.md`, `document.md`.
- Index files — Each project has documentation listing purpose and important files.
- Tags in headers — Start important files with metadata (project, category, last_updated).

### B. Easy to Edit & Update
- Markdown (.md) for documentation, runbooks, and analysis reports.
- Bash scripts for conversion pipeline (portable, readable).
- JSON/plain text for structured logs and metrics.
- Clear separation — One concern per script (convert vs clean vs analyze).

### C. Keep Files Small & Fast
- Split large conversions into stages (raw → cleaned).
- Separate concerns: conversion logs, cleaning logs, LLM analysis.
- Use references, archive old analysis reports.
- Target size: Aim for <50KB per file when possible.

## Current File Structure

```
Projects/Convert to markdown/
│
├── PROJECT_OVERVIEW.md                  # This file
├── README.md                            # User-facing documentation
├── DESIGN.md                            # Technical design decisions
├── SESSION-*.md                         # Development session notes
│
├── Core Pipeline (Stage 1 & 2)
├── mdcon                                # Stage 1: Convert to raw markdown
├── mdclean                              # Stage 2: Clean and structure markdown
├── mdcon-batch                          # Batch conversion wrapper
│
├── LLM Enhancement (Stage 3 - TO BE BUILT)
├── analyze-conversion                   # Analyze conversion quality with LLM
├── apply-improvements                   # Apply LLM suggestions to scripts
└── learning-loop                        # Orchestrate analyze → improve cycle
│
├── Legacy Scripts
├── pdf_to_md.sh                         # Original PDF converter
├── pdf_to_md_interactive.sh             # Interactive version
└── forever_notes_ocr.sh                 # OCR-focused converter
│
└── Logs & Analysis (Generated)
    ├── *.conversion.log                 # Per-file conversion logs
    ├── analysis_reports/                # LLM analysis outputs
    └── improvements/                    # Applied improvements history
```

## Two-Stage Pipeline (Current)

### Stage 1: `mdcon` - Raw Conversion
**Input**: PDF, DOCX, EPUB, HTML
**Output**: `filename-raw.md` + `filename-raw.conversion.log`

**What it logs**:
- Source file info (size, type)
- Page count (PDF) or document structure
- Extraction metrics (lines extracted, patterns filtered)
- Header/footer removal stats
- Conversion time

**Key features**:
- Uses `pdftotext`, `pandoc`, `tesseract` (OCR fallback)
- Detects and removes repeated headers/footers
- Strips page numbers and artifacts
- Preserves document structure as much as possible

### Stage 2: `mdclean` - Intelligent Cleaning
**Input**: Original file + `filename-raw.md`
**Output**: `filename.md` (cleaned)

**Usage**:
```bash
mdclean original.pdf raw.md              # → creates clean.md
mdclean original.docx raw.md output.md   # Custom output
mdclean --auto folder/                   # Batch: all *-raw.md files
```

**What it does**:
- Extracts heading structure from original file (PDF heuristics, DOCX/EPUB/HTML via pandoc)
- Matches detected headings in cleaned markdown
- Applies spacing fixes, paragraph detection
- Removes excessive blank lines
- Appends cleaning stats to conversion.log

## LLM Enhancement Pipeline (To Be Built)

### Stage 3: `analyze-conversion` - Quality Analysis
**Purpose**: Use local LLM (qwen2.5-coder:3b) to analyze conversion quality and suggest improvements.

**Inputs**:
- Original file (for ground truth reference)
- `filename-raw.md` (raw conversion output)
- `filename.md` (cleaned output)
- `filename-raw.conversion.log` (metrics and stats)

**LLM Analysis Tasks**:
1. **Structure Validation**
   - Compare detected headings vs actual document structure
   - Identify missed sections or chapters
   - Flag incorrect heading levels

2. **Content Quality**
   - Detect garbled text (OCR errors)
   - Identify formatting artifacts (page numbers, headers/footers that slipped through)
   - Flag missing paragraphs or merged sections

3. **Pattern Recognition**
   - Identify common error patterns across multiple conversions
   - Suggest regex patterns for repeated issues
   - Detect document-type-specific problems (academic papers vs books)

4. **Improvement Suggestions**
   - Specific bash/awk improvements for mdcon
   - Enhanced heuristics for mdclean
   - New filtering patterns to add

**Output**: `filename.analysis.md` with structured findings and suggestions

### Stage 4: `apply-improvements` - Script Enhancement
**Purpose**: Semi-automated application of LLM suggestions to pipeline scripts.

**Process**:
1. Parse analysis reports from multiple conversions
2. Group suggestions by category (filtering, structure detection, etc.)
3. Generate git diff previews for proposed changes
4. User reviews and approves changes
5. Apply to mdcon/mdclean with version tracking

### Stage 5: `learning-loop` - Continuous Improvement
**Purpose**: Orchestrate the full learning cycle.

**Workflow**:
```bash
# Batch convert
mdcon-batch ~/Documents/books/

# Analyze all conversions
learning-loop analyze ~/Documents/books/

# Review suggestions
learning-loop review

# Apply approved improvements
learning-loop apply

# Re-test with improved scripts
learning-loop test ~/Documents/books/test_set/
```

## Local LLM Integration

### Model Choice
**qwen2.5-coder:3b** via Ollama
- Excellent code understanding
- Good reasoning for structured text analysis
- Fits in 8GB RAM (tight but workable)
- Strong bash/scripting knowledge

### Installation
```bash
# Install Ollama (user will do this)
brew install ollama

# Pull model
ollama pull qwen2.5-coder:3b

# Test
ollama run qwen2.5-coder:3b
```

### API Integration
Ollama provides OpenAI-compatible API at `http://localhost:11434`

```bash
# Example prompt structure
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5-coder:3b",
  "prompt": "Analyze this markdown conversion quality...",
  "stream": false
}'
```

## File Format Guide

### For Documentation & Analysis → Use `.md`
Include front-matter metadata:
- project: md_convert_ai_enhanced
- category: analysis | design | runbook
- last_updated: YYYY-MM-DD
- status: draft | active | archived

### For Config → Use `.json`
Keys use camelCase; file names use underscores.

Suggested keys for future config:
- `llmModel`: "qwen2.5-coder:3b"
- `llmEndpoint`: "http://localhost:11434"
- `analysisDepth`: "quick" | "thorough"
- `autoApply`: false (require manual review)
- `maxSuggestions`: 10

### For Logs → Use `.log` (plain text, append-only)
Standard format: `YYYY-MM-DDTHH:MM:SSZ LEVEL MESSAGE`

### For Conversion Logs → Use `.conversion.log`
Structured format with sections:
```
SOURCE: filename.pdf (2.3MB)
TYPE: .pdf
PAGES: 245
EXTRACTED: 8234 lines from PDF
...
MDCLEAN STAGE
==============
STRUCTURE: Extracted 34 headings from PDF
HEADINGS: Marked 28 headings from structure
TIME: 12s
```

## Naming Conventions

### Files
- Scripts: lowercase, no extension or .sh: `mdcon`, `mdclean`, `analyze-conversion`
- Output markdown: hyphenated: `document-raw.md`, `document.md`
- Logs: hyphenated with extension: `document-raw.conversion.log`
- Analysis: hyphenated: `document.analysis.md`
- Date format: `YYYY-MM-DD` when included

### Folders
- lowercase with spaces: `Convert to markdown/`
- Generated folders: underscores: `analysis_reports/`, `improvements/`

## Acceptance Criteria

### Current Pipeline (Stages 1-2)
- ✅ Convert PDF/DOCX/EPUB/HTML to raw markdown
- ✅ Log detailed conversion metrics
- ✅ Extract structure from original files
- ✅ Apply intelligent cleaning with structure awareness
- ✅ Batch processing with progress tracking

### LLM Enhancement (Stages 3-5) - TO BE BUILT
- [ ] Analyze conversion quality with local LLM
- [ ] Generate actionable improvement suggestions
- [ ] Track suggestions in structured reports
- [ ] Semi-automated script improvements with user review
- [ ] Version tracking for all script changes
- [ ] Regression testing against known-good conversions
- [ ] Learning loop orchestration script

## Example Workflow (Full Pipeline)

```bash
# 1. Convert batch of documents
mdcon-batch ~/Documents/research_papers/

# 2. Clean all raw markdown files
mdclean --auto ~/Documents/research_papers/

# 3. Analyze conversion quality (future)
analyze-conversion ~/Documents/research_papers/*.pdf

# 4. Review LLM suggestions (future)
cat ~/Documents/research_papers/analysis_reports/summary.md

# 5. Apply improvements (future)
apply-improvements --preview
apply-improvements --apply

# 6. Re-convert test set to verify improvements
mdcon-batch ~/Documents/test_set/
```

## LLM Prompt Structure (Design)

### Analysis Prompt Template
```
You are a bash scripting expert analyzing markdown conversion quality.

INPUT FILES:
- Original: [filename.pdf]
- Raw Markdown: [filename-raw.md]
- Cleaned Markdown: [filename.md]
- Conversion Log: [filename-raw.conversion.log]

TASK:
Analyze the conversion quality and suggest specific bash/awk improvements.

FOCUS AREAS:
1. Structure: Are headings correctly detected?
2. Content: Are there OCR errors or artifacts?
3. Patterns: What repeated issues do you see?

OUTPUT FORMAT:
## Issues Found
- [Issue 1 with line references]
- [Issue 2 with line references]

## Suggested Bash Improvements
```bash
# Improvement 1: Better header detection
awk 'pattern here'
```

## Priority
HIGH | MEDIUM | LOW
```

## Next Steps for Implementation

1. ✅ Complete two-stage pipeline (mdcon + mdclean)
2. ✅ Ensure robust logging at each stage
3. ⏳ User installs Ollama and pulls qwen2.5-coder:3b
4. [ ] Build `analyze-conversion` script
5. [ ] Test LLM analysis on sample conversions
6. [ ] Build `apply-improvements` script
7. [ ] Create `learning-loop` orchestrator
8. [ ] Document full workflow in README.md
9. [ ] Create runbook for common scenarios

## Success Metrics

### Conversion Quality
- Heading detection accuracy: >90%
- OCR error rate: <5% for standard docs
- Artifact removal: >95% of page numbers/headers removed

### LLM Enhancement
- Suggestions implemented: Track % of LLM suggestions that improve quality
- Learning cycles: Measure quality improvement over iterations
- Time to improvement: Days to apply and test suggestions

### Performance
- Stage 1 (mdcon): <5s per 100-page PDF
- Stage 2 (mdclean): <2s per document
- Stage 3 (analyze): <30s per document with LLM

## Technical Constraints

### Hardware Limits
- 8GB RAM, 1.5GB VRAM
- qwen2.5-coder:3b is near limit
- Must use efficient prompts (minimal context)

### Dependencies
- pdftotext (poppler)
- pandoc
- tesseract (OCR)
- ollama
- bash 3.2+ (macOS compatible)

## Future Enhancements

- Web UI for batch conversion management
- Support for more file types (RTF, ODT)
- Cloud LLM fallback when local model unavailable
- Parallel processing for batch conversions
- Pre-trained model fine-tuned on conversion tasks
