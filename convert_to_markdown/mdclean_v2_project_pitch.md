# mdclean v2.0 - Intelligent Academic Document Processor

**Date:** 2025-11-05
**Model for Implementation:** Claude Opus (claude-opus-4-20250514)
**Estimated Complexity:** High
**Priority:** High

---

## 🎯 Project Goal

Rewrite `mdclean` from scratch as an intelligent academic document processor that:
1. **Cleans** markdown from PDF/DOCX conversions
2. **Extracts** metadata automatically (author, title, date, abstract)
3. **Generates** Harvard-style filenames (`surname_name_title.md`)
4. **Preserves** page numbers for academic citations
5. **Creates** Obsidian-compatible frontmatter
6. **Enables** easy referencing and citation

---

## 📋 Current State vs Desired State

### Current mdclean Issues

❌ **Batch mode broken** — Reports all files failed, creates no output
❌ **No metadata extraction** — Manual entry required
❌ **Generic filenames** — Uses PDF name, not Harvard format
❌ **No citation support** — Page numbers not preserved
❌ **No frontmatter** — No Obsidian properties
❌ **Complex codebase** — 700+ lines, hard to debug
❌ **Mixed responsibilities** — Interactive UI + batch + cleaning

### Desired mdclean v2.0

✅ **Clean separation** — mdclean (single file) + mdclean-batch (batch processing)
✅ **Metadata extraction** — Author, title, date from PDF/DOCX content
✅ **Harvard naming** — `rollins_peter_idolatry_of_god.md`
✅ **Page markers preserved** — `<!-- Page 42 -->` for citations
✅ **Obsidian frontmatter** — YAML properties with metadata
✅ **Citation templates** — Easy copy-paste Harvard references
✅ **Maintainable code** — ~300 lines, modular functions, well-commented
✅ **Robust batch** — Progress tracking, error handling, summary

---

## 🏗️ Architecture Design

### Component Breakdown

```
mdclean (v2.0)
├── Core Cleaning Engine
│   ├── Text normalization
│   ├── Paragraph reconstruction
│   ├── Heading detection (structure-aware)
│   ├── List/table preservation
│   └── Artifact removal (headers/footers)
│
├── Metadata Extraction Module
│   ├── Author detection (first pages, cover, bylines)
│   ├── Title extraction (largest font, first heading)
│   ├── Date parsing (publication, copyright)
│   ├── Abstract/summary (first substantial paragraph)
│   └── Source URL detection (if from web)
│
├── Harvard Naming Engine
│   ├── Author surname extraction
│   ├── Title keyword extraction (stop words removed)
│   ├── Filename generation (max 60 chars)
│   ├── Collision handling (add year/number suffix)
│   └── Validation (safe chars only)
│
├── Page Number System
│   ├── Page marker preservation: `<!-- Page N -->`
│   ├── Page range extraction (e.g., pages 1-42)
│   ├── Citation helper (generate: Author, Year, p. X)
│   └── Jump-to-page support
│
├── Obsidian Frontmatter Generator
│   ├── YAML header creation
│   ├── Property population (title, author, date, etc.)
│   ├── Tag generation (auto-tag by content type)
│   └── Wikilink formatting for authors
│
└── Single File Mode (default)
    ├── Interactive prompts
    ├── Drag-and-drop support
    ├── Preview before save
    └── Metadata review/edit

mdclean-batch (separate script)
├── Folder scanning
├── Original file matching (PDF/DOCX)
├── Progress tracking
├── Error handling & retry
├── Summary report
└── Bulk metadata extraction
```

---

## 📊 Feature Specifications

### 1. Harvard-Style Naming

**Input:** `David_Bentley_Hart_That_All_Shall_Be_Sav.pdf`

**Processing:**
1. Extract author from PDF metadata or first pages
2. Extract title from document
3. Generate: `hart_david_bentley_that_all_shall_be_saved.md`

**Format Rules:**
- `surname_firstname_title_keywords.md`
- All lowercase
- Underscores for spaces
- Max 60 characters (truncate title if needed)
- Remove articles (a, an, the) from title
- If collision: add `_2025.md` or `_2.md`

**Examples:**
```
rollins_peter_idolatry_of_god.md
hart_david_bentley_that_all_shall_be_saved.md
bonhoeffer_dietrich_life_together.md
dube_siphiwe_christian_nationalism_postapartheid.md
```

---

### 2. Metadata Extraction

**Goal:** Automatically extract from PDF/DOCX content

**Fields to Extract:**
```yaml
---
title: "The Idolatry of God"
author:
  - "[[Peter Rollins]]"
year: 2013
published: 2013-08-19  # If detectable
source: ""  # Empty for PDFs, URL for web
type: "book" | "article" | "paper" | "chapter"
pages: 1-234  # Total pages or page range
created: 2025-11-05  # Conversion date
description: |
  First substantial paragraph or abstract.
  Multiple lines preserved.
tags:
  - "theology"
  - "christianity"
  - "philosophy"
---
```

**Extraction Methods:**

**Author Detection:**
1. PDF metadata (Author field)
2. First page patterns:
   - "by [Name]"
   - Larger font under title
   - Author line above affiliation
3. DOCX properties
4. Fallback: prompt user or use "unknown"

**Title Detection:**
1. PDF metadata (Title field)
2. Largest font on first page
3. First markdown `# Heading`
4. DOCX title property
5. Fallback: filename

**Year/Date Detection:**
1. PDF metadata (CreationDate, ModDate)
2. Text patterns: "Copyright © 2013", "Published 2013"
3. Footer/header dates
4. Fallback: current year (with warning)

**Description/Abstract:**
1. Look for "Abstract" section
2. First substantial paragraph (>200 chars)
3. First 2-3 sentences
4. Fallback: empty

**Type Detection:**
1. "Journal of..." = article
2. "Chapter" in heading = chapter
3. Publisher name = book
4. ".edu" domain = paper
5. Fallback: "document"

---

### 3. Page Number Preservation

**During Conversion (mdcon):**
```markdown
<!-- Page 1 -->
First page content here...

<!-- Page 2 -->
Second page content...
```

**During Cleaning (mdclean):**
- **Keep** page markers: `<!-- Page N -->`
- Add to frontmatter: `pages: 1-42`
- Create citation helper section

**Citation Section (auto-added to end):**
```markdown
---

## Citation

**Harvard Format:**
Rollins, P. (2013). *The Idolatry of God: Breaking Our Addiction to Certainty and Satisfaction*. Howard Books.

**To cite a specific quote:**
(Rollins, 2013, p. XX)

**Page markers preserved:** Use Ctrl+F "<!-- Page" to find page numbers.
```

---

### 4. Obsidian Properties Template

**Based on example file:**

```yaml
---
title: "Full Document Title"
author:
  - "[[Surname, Firstname]]"  # Wikilink format
year: 2013
published: 2013-08-19  # YYYY-MM-DD if known
source: "https://..."  # URL if web clipping, empty if PDF
type: "book" | "article" | "paper" | "chapter" | "clipping"
pages: "1-234"  # Page range
created: 2025-11-05  # Today's date
description: |
  First substantial paragraph or abstract from document.
  Provides context when browsing in Obsidian.
tags:
  - "theology"
  - "academic"
  - "reference"
---
```

**Auto-tagging Logic:**
- Detect subject from title/content (theology, philosophy, history, etc.)
- Always add: "reference", "academic"
- Add "clipping" if source URL present
- User can edit after generation

---

### 5. Batch Processing Improvements

**mdclean-batch workflow:**

```bash
mdclean-batch /path/to/folder
```

**Process:**
1. Scan for `*-raw.md` files
2. Find matching original (PDF/DOCX/EPUB)
3. For each file:
   a. Extract metadata
   b. Generate Harvard filename
   c. Clean markdown
   d. Add frontmatter
   e. Preserve page numbers
   f. Save as Harvard name
4. Show progress: `[3/12] rollins_peter_idolatry_of_god.md ✓`
5. Generate summary report

**Summary Report:**
```
Batch Processing Complete!

Processed: 12 files
Success:   10 files
Failed:    2 files
Skipped:   0 files

Created Files:
  rollins_peter_idolatry_of_god.md
  hart_david_bentley_that_all_shall_be_saved.md
  (... 8 more ...)

Failed Files:
  document_without_author.pdf (no author detected)
  corrupted_file.pdf (extraction error)

Time: 45s

Output: /Users/mac/Documents/Local Vault/mdcon_tests/
```

---

## 🔧 Technical Implementation Plan

### Technology Stack

- **Language:** Bash 3.2+ (macOS compatible)
- **Dependencies:**
  - `pdfinfo` (metadata extraction from PDF)
  - `pdftotext` (text extraction for author/title detection)
  - `pandoc` (DOCX metadata extraction)
  - `exiftool` (optional, fallback metadata)
- **Testing:** Sample PDFs in mdcon_tests/

### Code Structure

**mdclean (single file mode) - ~300 lines:**
```bash
#!/usr/bin/env bash
# mdclean v2.0 - Intelligent Academic Document Processor

# SECTION 1: Core Functions (lines 1-100)
# - extract_pdf_metadata()
# - extract_docx_metadata()
# - detect_author()
# - detect_title()
# - detect_year()
# - extract_abstract()

# SECTION 2: Naming Engine (lines 101-150)
# - generate_harvard_filename()
# - sanitize_filename()
# - handle_collision()

# SECTION 3: Cleaning Engine (lines 151-220)
# - clean_markdown()
# - preserve_page_numbers()
# - detect_headings()
# - fix_paragraphs()

# SECTION 4: Frontmatter Generator (lines 221-260)
# - generate_frontmatter()
# - format_yaml()
# - create_citation()

# SECTION 5: Main Logic (lines 261-300)
# - parse_args()
# - interactive_mode()
# - main()
```

**mdclean-batch - ~150 lines:**
```bash
#!/usr/bin/env bash
# mdclean-batch - Bulk processing for mdclean v2.0

# SECTION 1: Batch Logic (lines 1-80)
# - scan_folder()
# - match_originals()
# - process_batch()

# SECTION 2: Progress & Reporting (lines 81-150)
# - show_progress()
# - generate_report()
# - main()
```

---

## 📝 Example Use Cases

### Use Case 1: Single Academic Paper

**Input:**
```bash
mdclean "Journal Article.pdf" "Journal Article-raw.md"
```

**Process:**
1. Extracts: Author "Siphiwe Dube", Title "Christian nationalism..."
2. Generates filename: `dube_siphiwe_christian_nationalism.md`
3. Creates frontmatter with metadata
4. Preserves page markers
5. Adds citation template

**Output:** `dube_siphiwe_christian_nationalism.md`

---

### Use Case 2: Batch Convert Folder

**Input:**
```bash
mdclean-batch ~/Documents/papers/
```

**Contents:**
- 12 PDFs converted with mdcon-batch
- 12 `*-raw.md` files ready

**Output:**
- 12 cleaned files with Harvard names
- All with frontmatter + metadata
- Summary report
- Failed files logged

---

### Use Case 3: Web Article with Existing Metadata

**Input:** Obsidian web clipper already added frontmatter

**Process:**
1. mdclean detects existing frontmatter
2. Preserves source URL, published date
3. Adds missing fields (created, pages)
4. Cleans content below frontmatter
5. Renames to Harvard format if author present

---

## 🎓 Academic Features Wishlist

### Future Enhancements (v2.1+)

1. **Bibliography Generator**
   - Scan Obsidian vault for all academic docs
   - Generate bibliography.md with all citations
   - Sort by author, date, type

2. **Smart Cross-References**
   - Detect when docs cite each other
   - Create backlinks automatically
   - "Also cited in: [[other_paper.md]]"

3. **BibTeX Export**
   - Generate .bib file from frontmatter
   - Compatible with LaTeX/Zotero
   - Update on document changes

4. **Reading List Management**
   - Tag: "to-read", "reading", "read"
   - Track: date-started, date-completed
   - Generate reading log

5. **Smart Tagging**
   - NLP-based subject detection
   - Auto-suggest tags from content
   - Tag hierarchy (theology > systematic > christology)

6. **Quote Extraction**
   - Detect blockquotes with page numbers
   - Create quote index
   - Link quotes to sources

---

## 🚀 Implementation Plan

### Phase 1: Core Rewrite (Opus)
**Tasks:**
1. Write mdclean v2.0 from scratch
2. Metadata extraction functions
3. Harvard naming engine
4. Frontmatter generator
5. Page number preservation
6. Single file mode

**Deliverable:** Working mdclean v2.0 (300 lines, clean code)

---

### Phase 2: Batch Processing (Opus)
**Tasks:**
1. Write mdclean-batch from scratch
2. Folder scanning
3. Progress tracking
4. Error handling
5. Summary report

**Deliverable:** Working mdclean-batch (150 lines)

---

### Phase 3: Testing & Refinement (Sonnet)
**Tasks:**
1. Test on all 12 files in mdcon_tests/
2. Fix edge cases
3. Improve metadata detection accuracy
4. Add error messages
5. Create documentation

**Deliverable:** Tested, production-ready scripts

---

### Phase 4: Integration (Sonnet)
**Tasks:**
1. Update mdcon to work seamlessly with mdclean v2.0
2. Create unified workflow documentation
3. Archive old mdclean as mdclean-legacy
4. Update .zshrc if needed

**Deliverable:** Complete workflow: PDF → mdcon → mdclean v2.0

---

## 📊 Success Criteria

### Must Have (MVP)
- ✅ Cleans markdown correctly (no broken headings/lists)
- ✅ Extracts author and title from 80%+ of academic docs
- ✅ Generates Harvard-style filenames
- ✅ Creates valid YAML frontmatter
- ✅ Preserves page numbers
- ✅ Batch mode processes 10+ files successfully
- ✅ Clear error messages when metadata missing

### Should Have
- ✅ Detects publication year from content
- ✅ Extracts meaningful description/abstract
- ✅ Handles DOCX and PDF equally well
- ✅ Auto-tags documents by type
- ✅ Citation template generation
- ✅ Progress bar in batch mode

### Nice to Have
- ✅ Interactive metadata review/edit before save
- ✅ Duplicate detection (same author+title)
- ✅ Smart truncation of long titles
- ✅ Author name normalization (handles multiple formats)
- ✅ BibTeX export option

---

## 🎯 Why Rewrite vs Fix?

### Reasons for Clean Rewrite

1. **Current code too complex** — 700 lines, multiple modes embedded
2. **Batch mode fundamentally broken** — Easier to rewrite than debug
3. **New requirements** — Metadata extraction, naming, frontmatter
4. **Clean separation** — mdclean (single) + mdclean-batch (bulk)
5. **Maintainability** — Opus can write clean, well-documented code
6. **Testing** — Fresh start = easier to test each module
7. **Future-proof** — Modular design for easy enhancement

### What to Preserve from Current

- ✅ Structure-aware heading detection (works well)
- ✅ Paragraph reconstruction logic (solid)
- ✅ Page marker preservation concept
- ✅ Color-coded terminal output (good UX)

---

## 📋 Detailed Requirements Doc (for Opus)

### Input Specifications

**Supported Original Formats:**
- PDF (primary focus)
- DOCX (secondary)
- EPUB (if time permits)
- HTML (if time permits)

**Required Input Files:**
1. Original file (PDF/DOCX) — for metadata extraction
2. Raw markdown file (*-raw.md) — from mdcon output

**Raw Markdown Format (from mdcon):**
```markdown
# Title

> Converted from PDF on YYYY-MM-DD

<!-- Page 1 -->

Content with excessive blank lines...


And broken paragraphs...

<!-- Page 2 -->

More content...
```

---

### Output Specifications

**Cleaned Markdown File:**

```markdown
---
title: "The Idolatry of God: Breaking Our Addiction to Certainty and Satisfaction"
author:
  - "[[Rollins, Peter]]"
year: 2013
published: 2013-08-19
source: ""
type: "book"
pages: "1-234"
created: 2025-11-05
description: |
  Peter Rollins thinks that much modern Christianity has become,
  in essence, idolatry. Today the "Good News" of Christianity
  operates with much the same logic.
tags:
  - "theology"
  - "christianity"
  - "reference"
---

# The Idolatry of God

<!-- Page 1 -->

Peter Rollins thinks that much modern Christianity has become, in essence, idolatry.

Today the "Good News" of Christianity operates with much the same logic. It is sold to us as that which can fulfill our desire rather than as that which evokes transformation in the very way that we desire.

<!-- Page 2 -->

(... cleaned content with proper paragraphs and headings ...)

---

## Citation

**Harvard Format:**
Rollins, P. (2013). *The Idolatry of God: Breaking Our Addiction to Certainty and Satisfaction*. Howard Books.

**To cite this work:**
(Rollins, 2013, p. XX)

**Page markers preserved:** Search for `<!-- Page` to navigate.
```

**Filename:** `rollins_peter_idolatry_of_god.md`

---

### Metadata Extraction Algorithms

**Author Extraction Priority:**
1. PDF metadata `/Author` field
2. DOCX properties (creator/author)
3. Text patterns on first 3 pages:
   - Line matching: `^by (.+)$`
   - Line matching: `^(.+),$` followed by affiliation
   - Largest non-title text on page 1
4. Prompt user if all fail

**Title Extraction Priority:**
1. PDF metadata `/Title` field
2. DOCX title property
3. Largest font on first page (if >24pt)
4. First `# Heading` in markdown
5. First all-caps or title-case line
6. Filename (remove extension and clean)

**Year Extraction Patterns:**
```regex
Copyright © (\d{4})
Published (\d{4})
(\d{4}) [Pp]ublisher
\((\d{4})\)  # Year in parentheses
```

**Abstract Detection:**
```markdown
# Look for section headers
Abstract
ABSTRACT
Summary
Executive Summary

# Or first substantial paragraph
(Paragraph >200 chars, not title/author, within first 3 pages)
```

---

### Harvard Filename Generation

**Algorithm:**

```python
def generate_harvard_filename(author, title):
    # 1. Extract surname
    surname = extract_surname(author)  # "Peter Rollins" → "rollins"

    # 2. Extract first name
    firstname = extract_firstname(author)  # "Peter Rollins" → "peter"

    # 3. Clean title
    title_words = remove_stop_words(title)
    # "The Idolatry of God" → ["idolatry", "god"]

    # 4. Build filename
    filename = f"{surname}_{firstname}_{title_words_joined}"
    # "rollins_peter_idolatry_of_god"

    # 5. Sanitize
    filename = lowercase(filename)
    filename = replace_spaces_with_underscores(filename)
    filename = remove_special_chars(filename)

    # 6. Length limit
    if len(filename) > 60:
        filename = filename[:60]
        filename = truncate_at_word_boundary(filename)

    # 7. Add extension
    filename = filename + ".md"

    # 8. Check collision
    if file_exists(filename):
        filename = add_suffix(filename)  # _2, _3, or _2025

    return filename
```

**Stop Words to Remove:**
```
a, an, the, of, in, on, at, to, for, with, from, by
and, or, but, is, are, was, were
```

**Special Cases:**
- Multiple authors: Use first author only
- No first name: `surname_title.md`
- Very long name: Truncate first name to initial
- Non-Latin chars: Transliterate or use "unknown"

---

## 🛠️ Commands to Switch Claude Model

### Quick Command
```bash
# In Claude Code chat, just type:
@opus

# Or for full model name:
@claude-opus-4-20250514
```

### Alternative: Environment Variable
```bash
# In terminal before starting Claude Code:
export ANTHROPIC_MODEL=claude-opus-4-20250514
claude
```

### In API Call (if scripting)
```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-opus-4-20250514",
    "max_tokens": 4096,
    "messages": [...]
  }'
```

### Model Names Reference
- Sonnet (current): `claude-sonnet-4-20250514` or `@sonnet`
- Opus (powerful): `claude-opus-4-20250514` or `@opus`
- Haiku (fast): `claude-haiku-4-20250514` or `@haiku`

---

## 📦 Deliverables for Opus Session

### What to Provide Opus

1. **This project pitch document** (context)
2. **Example files:**
   - `/Users/mac/Documents/Local Vault/mdcon_tests/Journal Article-raw.md`
   - `/Users/mac/Documents/Local Vault/mdcon_tests/Journal Article.pdf`
   - Obsidian properties example (already read)
3. **Current mdcon output format** (so Opus knows input)
4. **Desired output format** (detailed in this doc)
5. **Success criteria** (test cases)

### What Opus Should Deliver

1. **mdclean v2.0 script** (complete, ~300 lines)
2. **mdclean-batch script** (complete, ~150 lines)
3. **README.md** (usage instructions)
4. **TESTING.md** (how to test, expected results)
5. **Code comments** (explain algorithms)

---

## ✅ Ready to Start?

**Next Steps:**

1. ✅ Review this pitch — ensure all requirements clear
2. ✅ Gather example files for Opus
3. ✅ Start new Opus chat
4. ✅ Paste this pitch + examples
5. ✅ Let Opus write clean, production-ready code
6. ✅ Test on mdcon_tests/ folder
7. ✅ Iterate if needed
8. ✅ Deploy and archive old mdclean

---

**Questions Before We Start:**

1. Any additional metadata fields you want?
2. Specific academic citation styles besides Harvard?
3. Other file formats to support (EPUB, HTML)?
4. Special requirements for theology/academic papers?

---

**Estimated Opus Token Usage:** 50,000-75,000 tokens (full implementation)

**Time to Complete:** 1-2 hours (Opus writing + testing)

**Worth it?** Absolutely. Clean, maintainable, feature-rich academic document processor.
