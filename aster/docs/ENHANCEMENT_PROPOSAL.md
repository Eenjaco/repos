# Universal Document Processor - Enhancement Proposal

**Date:** 2025-11-13
**Project:** mdclean_universal
**Goal:** Create a unified tool that converts ANY input to clean, structured markdown ready for knowledge management

---

## Executive Summary

Build a single, powerful document processor that:
1. **Accepts any input**: Images (handwritten/printed), audio, PDFs, EPUB, DOCX, HTML, TXT, MD
2. **Extracts content intelligently**: OCR for images, transcription for audio, parsing for documents
3. **Structures with AI**: Uses Unstructured library to detect document elements
4. **Cleans with LLM**: Uses Ollama 3.2 1B to add punctuation, capitalization, fix errors
5. **Outputs for KM**: Generates markdown with frontmatter, metadata, tags ready for Obsidian/Zettelkasten

---

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                       INPUT LAYER                                │
├─────────────────────────────────────────────────────────────────┤
│  Images (JPG/PNG)  │  Audio (MP3/M4A)  │  Docs (PDF/EPUB/DOCX) │
│  Text (TXT/MD)     │  Web (HTML)       │                        │
└──────────┬──────────────────┬───────────────────┬───────────────┘
           │                  │                   │
           ▼                  ▼                   ▼
    ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
    │ OCR Extract  │   │ Transcribe   │   │ Parse/Extract│
    │  (Tesseract) │   │ (Vosk/Whisper│   │  (pandoc)    │
    └──────┬───────┘   └──────┬───────┘   └──────┬───────┘
           │                  │                   │
           └──────────────────┴───────────────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │  RAW TEXT CONTENT    │
                   └──────────┬───────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │  UNSTRUCTURED.IO     │
                   │  - Detect elements   │
                   │  - Find structure    │
                   │  - Identify lists    │
                   │  - Detect tables     │
                   └──────────┬───────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │  OLLAMA 3.2 1B       │
                   │  - Add punctuation   │
                   │  - Capitalize        │
                   │  - Fix errors        │
                   │  - Structure paras   │
                   └──────────┬───────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │  KM POST-PROCESSOR   │
                   │  - Add frontmatter   │
                   │  - Extract metadata  │
                   │  - Add tags          │
                   │  - Create wikilinks  │
                   └──────────┬───────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │  CLEAN MARKDOWN      │
                   │  Ready for Obsidian  │
                   └──────────────────────┘
```

---

## Supported Input Types

### 1. Images (OCR Pipeline)
**File types:** `.jpg`, `.jpeg`, `.png`, `.tiff`, `.bmp`

**Use cases:**
- Photos of handwritten notes
- Scanned book pages
- Whiteboard captures
- Screenshots of text
- Photos of printed documents

**Processing:**
```python
Image → Preprocessing → Tesseract OCR → Raw Text → Pipeline
```

**Preprocessing steps:**
- Deskew (straighten)
- Denoise (remove artifacts)
- Contrast enhancement
- Resize for optimal DPI (300)

### 2. Audio (Transcription Pipeline)
**File types:** `.mp3`, `.m4a`, `.wav`, `.flac`

**Use cases:**
- Voice memos
- Sermon recordings
- Lecture audio
- Interview recordings
- Podcast episodes

**Processing:**
```python
Audio → Vosk/Whisper → Timestamped Text → Pipeline
```

### 3. Documents (Parser Pipeline)
**File types:** `.pdf`, `.epub`, `.docx`, `.odt`, `.rtf`

**Use cases:**
- Books
- Research papers
- Articles
- Reports

**Processing:**
```python
Document → pandoc/pdftotext → Raw Text → Pipeline
```

### 4. Web Content (Parser Pipeline)
**File types:** `.html`, `.htm`, `.mhtml`

**Use cases:**
- Saved web articles
- Blog posts
- Documentation pages

**Processing:**
```python
HTML → pandoc → Raw Text → Pipeline
```

### 5. Plain Text (Direct Pipeline)
**File types:** `.txt`, `.md`

**Use cases:**
- Quick notes
- Already extracted text
- Markdown that needs cleanup

**Processing:**
```python
Text → Pipeline (skip extraction)
```

---

## Core Components

### Component 1: Input Router
**Purpose:** Detect file type and route to appropriate handler

```python
def route_input(file_path: Path) -> str:
    """Route to: ocr, transcribe, parse, or direct"""
    extension = file_path.suffix.lower()

    if extension in ['.jpg', '.png', '.tiff']:
        return 'ocr'
    elif extension in ['.mp3', '.m4a', '.wav']:
        return 'transcribe'
    elif extension in ['.pdf', '.epub', '.docx']:
        return 'parse'
    elif extension in ['.html', '.htm']:
        return 'web'
    elif extension in ['.txt', '.md']:
        return 'direct'
    else:
        raise UnsupportedFormat(extension)
```

### Component 2: OCR Handler
**Purpose:** Extract text from images with preprocessing

```python
def process_image_ocr(image_path: Path) -> str:
    """
    1. Load image
    2. Preprocess (deskew, denoise, enhance)
    3. Run Tesseract OCR
    4. Return raw text
    """
    # Use PIL + pytesseract
    # Apply cv2 preprocessing for better accuracy
    # Support multiple languages
```

**Key features:**
- Automatic image enhancement
- Multi-language support (English, Afrikaans, etc.)
- Handwriting mode option
- Batch processing for multi-page scans

### Component 3: Transcription Handler
**Purpose:** Convert audio to text

```python
def process_audio_transcription(audio_path: Path) -> str:
    """
    1. Detect audio format
    2. Convert if needed (ffmpeg)
    3. Transcribe with Vosk or Whisper
    4. Return text (with optional timestamps)
    """
    # Reuse existing transcribe_vosk_stream.py logic
    # Option to use Whisper for better accuracy
```

### Component 4: Document Parser
**Purpose:** Extract text from structured documents

```python
def process_document(doc_path: Path) -> str:
    """
    1. Detect document type
    2. Use appropriate tool (pdftotext, pandoc)
    3. Clean obvious artifacts
    4. Return raw text
    """
    # Reuse logic from mdcon
    # Handle scanned PDFs with OCR fallback
```

### Component 5: Unstructured Processor
**Purpose:** Detect and structure document elements

```python
def structure_with_unstructured(raw_text: str) -> List[Element]:
    """
    1. Partition text into elements
    2. Detect: titles, narratives, lists, tables
    3. Return structured elements
    """
    from unstructured.partition.text import partition_text

    elements = partition_text(text=raw_text)

    # Element types:
    # - Title (headings)
    # - NarrativeText (paragraphs)
    # - ListItem (bullet/numbered)
    # - Table
    # - Image (metadata)

    return elements
```

### Component 6: Ollama Cleaner
**Purpose:** Polish text with LLM (punctuation, capitalization, errors)

```python
def clean_with_ollama(elements: List[Element]) -> str:
    """
    1. Process each element with Ollama 3.2 1B
    2. Add punctuation and capitalization
    3. Fix obvious errors
    4. Preserve structure
    5. Return cleaned markdown
    """
    model = "llama3.2:1b"

    for element in elements:
        if isinstance(element, NarrativeText):
            # Clean paragraphs
            cleaned = ollama_polish(element.text, model)
        elif isinstance(element, Title):
            # Format headings
            cleaned = format_heading(element.text)
        # etc.
```

**Ollama 3.2 1B Advantages:**
- Fast (optimized for low-memory systems)
- Good at punctuation and capitalization
- Low RAM usage (~1GB)
- Can run while other apps are open

### Component 7: Knowledge Management Formatter
**Purpose:** Add metadata and structure for KM systems

```python
def format_for_knowledge_management(
    cleaned_text: str,
    source_file: Path,
    metadata: dict
) -> str:
    """
    1. Generate frontmatter (YAML)
    2. Extract key concepts
    3. Add tags
    4. Create wikilinks for important terms
    5. Format final markdown
    """
    frontmatter = f"""---
source: {source_file.name}
date_processed: {datetime.now().isoformat()}
type: {metadata.get('type', 'document')}
tags: {metadata.get('tags', [])}
---

"""
    return frontmatter + cleaned_text
```

---

## Use Cases & Examples

### Use Case 1: Handwritten Notes Photo
**Input:** Phone photo of handwritten notebook page (JPG)

**Process:**
1. User drags photo into tool
2. OCR extracts handwritten text (Tesseract)
3. Unstructured detects paragraphs and bullet points
4. Ollama cleans up OCR errors, adds punctuation
5. KM formatter adds frontmatter and tags

**Output:**
```markdown
---
source: notebook_page_20251113.jpg
date_processed: 2025-11-13T14:30:00
type: fleeting_note
tags: [handwritten, personal, ideas]
---

## Meeting Notes

Today's discussion covered three main points:

- Project timeline needs adjustment
- Budget allocation for Q4
- Team member responsibilities

Key action items:
- Follow up with client by Friday
- Review budget proposal
- Schedule next meeting
```

### Use Case 2: Sermon Audio Recording
**Input:** MP3 recording of church sermon (45 minutes)

**Process:**
1. User runs: `mdclean sermon_2025_11_10.mp3`
2. Vosk transcribes audio to text
3. Unstructured detects natural paragraph breaks
4. Ollama adds punctuation and fixes transcription errors
5. KM formatter adds sermon metadata

**Output:**
```markdown
---
source: sermon_2025_11_10.mp3
date_processed: 2025-11-13T14:30:00
type: sermon
speaker: Pastor John
date_recorded: 2025-11-10
duration: 45m
tags: [sermon, faith, Romans-8]
---

Good morning, everyone. Today we're going to talk about Romans chapter 8, specifically verses 28 through 30.

We know that in all things God works for the good of those who love Him, who have been called according to His purpose. This is such a powerful promise.

## Main Points

The scripture tells us three important things...
```

### Use Case 3: Scanned PDF Book
**Input:** PDF of scanned book (200 pages)

**Process:**
1. User runs: `mdclean book_scanned.pdf`
2. Tool detects scanned PDF, runs OCR on each page
3. Unstructured detects chapters, headings, paragraphs
4. Ollama cleans text and fixes OCR errors
5. KM formatter creates structured markdown with chapters

**Output:**
```markdown
---
source: book_scanned.pdf
title: Living Into Community
author: Christine Pohl
type: book
pages: 200
tags: [book, community, theology]
---

# Living Into Community

## Chapter 1: Introduction

Community is at the heart of Christian life. Throughout history, believers have gathered together to share their lives, resources, and faith.

In this chapter, we will explore three foundational principles...
```

### Use Case 4: Screenshot of Web Article
**Input:** PNG screenshot of interesting blog post

**Process:**
1. User drags screenshot
2. OCR extracts text from image
3. Unstructured detects article structure
4. Ollama formats and cleans
5. Output saved to Inbox/

**Output:**
```markdown
---
source: blog_screenshot_20251113.png
type: web_article
tags: [web, article, productivity]
---

## How to Build a Second Brain

The concept of a second brain is simple: capture everything, organize systematically, and retrieve effortlessly.

Here are the key principles:

1. Capture: Write everything down
2. Organize: Use a consistent system
3. Distill: Extract key insights
4. Express: Share your knowledge
```

### Use Case 5: Plain Text Cleanup
**Input:** Messy text file from quick notes

**Process:**
1. User runs: `mdclean messy_notes.txt`
2. Skip OCR/transcription (already text)
3. Unstructured structures content
4. Ollama adds proper formatting
5. Output ready for vault

**Output:**
```markdown
---
source: messy_notes.txt
type: fleeting_notes
tags: [notes, ideas]
---

## Project Ideas

Three interesting concepts came up today during the brainstorming session.

First, we should consider building a unified document processor. This would handle any input type and output clean markdown.

Second, integration with knowledge management systems is crucial...
```

---

## Technical Implementation Plan

### Phase 1: Core Architecture (Week 1)
- [ ] Create project structure
- [ ] Implement input router
- [ ] Build file type detection
- [ ] Set up logging and error handling

### Phase 2: Input Handlers (Week 2)
- [ ] OCR handler with Tesseract
  - Image preprocessing (deskew, denoise)
  - Multi-language support
  - Handwriting recognition mode
- [ ] Audio transcription handler
  - Integrate existing Vosk code
  - Add Whisper option
- [ ] Document parser
  - PDF (text and scanned)
  - EPUB, DOCX via pandoc
- [ ] HTML parser
- [ ] Direct text handler

### Phase 3: Unstructured Integration (Week 2-3)
- [ ] Install and configure Unstructured
- [ ] Element detection and classification
- [ ] Structure preservation
- [ ] Table and list handling

### Phase 4: Ollama Integration (Week 3)
- [ ] Ollama 3.2 1B setup
- [ ] Chunking strategy (avoid token limits)
- [ ] Prompt engineering for cleanup
- [ ] Element-aware processing
- [ ] Error handling and fallbacks

### Phase 5: Knowledge Management Features (Week 4)
- [ ] Frontmatter generation
- [ ] Metadata extraction
- [ ] Tag generation
- [ ] Wikilink creation
- [ ] Template system

### Phase 6: CLI & Batch Processing (Week 4)
- [ ] User-friendly CLI with typer
- [ ] Interactive mode
- [ ] Batch processing
- [ ] Progress indicators
- [ ] Configuration file support

### Phase 7: Testing & Documentation (Week 5)
- [ ] Test with all file types
- [ ] Edge case handling
- [ ] Performance optimization
- [ ] User documentation
- [ ] Example workflows

---

## Configuration File

**`~/.mdclean/config.yaml`**

```yaml
# Model configuration
ollama:
  model: "llama3.2:1b"
  endpoint: "http://localhost:11434"
  temperature: 0.2
  max_tokens: 4096

# OCR settings
ocr:
  language: "eng"  # or "eng+afr" for multiple
  preprocess: true
  handwriting_mode: false
  dpi: 300

# Transcription settings
transcription:
  engine: "vosk"  # or "whisper"
  model_path: "~/.cache/vosk-model-small-en-us-0.15"
  timestamps: false

# Knowledge management
knowledge_management:
  add_frontmatter: true
  extract_tags: true
  create_wikilinks: true
  output_template: "zettelkasten"  # or "obsidian", "simple"

# Output settings
output:
  default_dir: "~/Documents/Vault/Inbox/"
  filename_pattern: "{source_name}_processed_{date}.md"
  preserve_structure: true
```

---

## Command-Line Interface

### Basic Usage

```bash
# Single file (auto-detect type)
mdclean document.pdf

# With output path
mdclean notes.jpg --output ~/Vault/Inbox/

# Batch process folder
mdclean --batch ~/Documents/to-process/

# Interactive mode
mdclean
```

### Advanced Options

```bash
# Specify processing mode
mdclean image.jpg --ocr-language eng+afr --handwriting

# Audio with timestamps
mdclean sermon.mp3 --timestamps

# Skip LLM cleaning (fast mode)
mdclean doc.pdf --no-llm

# Custom template
mdclean article.html --template literature_note

# Preserve original + create cleaned
mdclean notes.txt --keep-original
```

---

## Performance Expectations

### Hardware: 8GB RAM, CPU-only

| Input Type | File Size | Processing Time | Memory Usage |
|------------|-----------|-----------------|--------------|
| Image (JPG) | 5MB | ~10-15s | ~500MB |
| Audio (MP3) | 50MB (30min) | ~2-3min | ~1GB |
| PDF (text) | 10MB (200 pages) | ~30-45s | ~800MB |
| PDF (scanned) | 20MB (200 pages) | ~3-5min | ~1.5GB |
| HTML | 1MB | ~5-10s | ~400MB |
| Plain text | 1MB | ~5-10s | ~400MB |

**Bottlenecks:**
- OCR: Tesseract (CPU-bound)
- Transcription: Vosk model (CPU-bound)
- LLM: Ollama 3.2 1B (~1GB RAM, CPU-bound)

**Optimization:**
- Process in chunks to manage memory
- Use streaming for large files
- Parallel processing where possible
- Cache OCR results

---

## Success Criteria

### Functional Requirements
- ✅ Support all specified input types
- ✅ Extract text accurately (>90% for clear inputs)
- ✅ Structure content intelligently
- ✅ Clean text with LLM
- ✅ Generate KM-ready markdown
- ✅ Batch processing capability

### Quality Requirements
- ✅ OCR accuracy >85% for clear images
- ✅ Transcription accuracy >90% for clear audio
- ✅ Structure detection >90% for standard documents
- ✅ LLM cleanup improves readability significantly

### Performance Requirements
- ✅ Single document <5min (excluding long audio)
- ✅ Batch 10 documents <30min
- ✅ Memory usage <2GB peak
- ✅ Graceful handling of large files

### Usability Requirements
- ✅ Simple CLI (drag-and-drop friendly)
- ✅ Clear progress indicators
- ✅ Helpful error messages
- ✅ Sensible defaults
- ✅ Easy configuration

---

## Archive Plan for Existing Tools

### Tools to Archive
1. **mp3_txt/mdclean.py** → Archive (replaced by unified tool)
2. **mp3_txt/mdclean_simple.py** → Archive (logic absorbed)
3. **mp3_txt/mdclean_claude.py** → Keep as option (high-quality API backup)
4. **convert_to_markdown/mdcon** → Archive (absorbed into unified tool)
5. **convert_to_markdown/mdclean** → Archive (absorbed)

### Archive Structure
```
archive/
├── old_mdclean_variants/
│   ├── mdclean_v1.py (mp3_txt version)
│   ├── mdclean_simple_v1.py
│   └── README_archived.md
├── old_mdcon/
│   ├── mdcon_v1.sh
│   ├── mdclean_v1.sh
│   └── README_archived.md
└── MIGRATION_GUIDE.md
```

---

## Next Steps

1. ✅ Review and approve this proposal
2. [ ] Set up project structure
3. [ ] Implement core architecture
4. [ ] Build input handlers one by one
5. [ ] Integrate Unstructured + Ollama
6. [ ] Test with real files
7. [ ] Document usage
8. [ ] Archive old tools

---

## Questions to Resolve

1. **Default model:** Stick with Ollama 3.2 1B or allow easy switching?
   - **Recommendation:** Default to 1B, config option for others

2. **Handwriting OCR:** Use standard Tesseract or add specialized model?
   - **Recommendation:** Start with standard, add advanced option later

3. **Output location:** Default to Inbox/ or ask every time?
   - **Recommendation:** Config default, CLI override

4. **Processing priority:** Structure or LLM cleanup first?
   - **Current design:** Structure → LLM (preserves detected elements)

5. **Batch processing:** Sequential or parallel?
   - **Recommendation:** Sequential (safer with RAM limits)

---

**Status:** ✅ Proposal Complete - Ready for Implementation

**Author:** Claude + User
**Last Updated:** 2025-11-13
