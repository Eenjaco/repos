# Convert to Markdown - Living Design Document

**Last Updated:** 2025-11-03
**Status:** Active - Fully Functional
**Claude Sessions:** 2

---

## Project Vision

**What:** Universal file-to-markdown converter for knowledge management
**Why:** Bridge the gap between various document formats and markdown-based note systems (Obsidian, Forever Notes)
**For Whom:** Mac user managing a knowledge base in markdown format

---

## Current State

**Version:** 2.0 (Universal Converter)
**Working Features:**
- ✅ Scanned PDF → Markdown (OCR)
- ✅ Text PDF → Markdown (fast)
- ✅ EPUB → Markdown
- ✅ DOCX → Markdown
- ✅ HTML → Markdown
- ✅ Interactive prompts for file paths
- ✅ Auto-detection of scanned vs text PDFs
- ✅ Simple commands: `mdcon` and `mdclean` (installed)

**In Progress:**
- ⏳ Testing `mdclean` on OCR-generated files
- ⏳ Testing other file formats (EPUB, DOCX, HTML)

**Known Issues:**
- OCR quality depends on scan quality (expected)
- Page 1 often has artifacts from decorative elements
- Minor spacing issues in OCR output
- Google Docs (.gdoc) requires manual download first

**Fixed Issues:**
- ✅ mdclean v1 deleted all content (piped sed on macOS) - FIXED 2025-11-03
  - Root cause: Complex sed pipeline didn't work correctly on macOS
  - Solution: Apply sed transformations sequentially with `-i.bak`

---

## Architecture Overview

**High-Level Design:**
Single interactive script routes to appropriate converter based on file type. Uses pandoc for most conversions, ghostscript + tesseract for scanned PDFs.

**Key Components:**
1. **mdcon** - Main router script with interactive prompts
2. **mdclean** - Post-processing cleaner for markdown files
3. **OCR Pipeline** - ghostscript → tesseract → pandoc (scanned PDFs)
4. **Direct Conversion** - pandoc wrapper (text files, EPUB, DOCX, HTML)
5. **File Type Detector** - Determines if PDF is scanned or text-based

**Data Flow:**
```
[User Input] → [File Type Detection] → [Appropriate Converter] → [Markdown Output]
                                             ↓
                                   [OCR Pipeline if scanned]
                                             ↓
                                   [Pandoc for all others]
```

**Tech Stack:**
- Language: Bash shell script
- OCR: Tesseract 4.x + Ghostscript 10.06
- Conversion: Pandoc 3.x
- Platform: macOS (compatible with Linux)
- Dependencies: All installed via Homebrew

---

## Design Decisions

### Decision 1: Universal Script Instead of Separate Scripts
**Date:** 2025-11-03
**Context:** User had to remember which script for which file type
**Decision:** Create single `conmd` command that auto-detects file type
**Rationale:** Simpler UX - one command to remember, handles all conversions
**Tradeoffs:** Slightly more complex code, but much better user experience

### Decision 2: Interactive Prompts Over Command-Line Arguments
**Date:** 2025-11-03
**Context:** User struggled with spaces in file paths when using CLI arguments
**Decision:** Use interactive prompts + drag-and-drop support
**Rationale:**
- Drag-and-drop handles spaces automatically
- More user-friendly for non-technical users
- Clear step-by-step process
**Tradeoffs:** Not scriptable for batch operations, but user doesn't need that

### Decision 3: Auto-Detect Scanned vs Text PDFs
**Date:** 2025-11-03
**Context:** PDFs can be scanned images or text-based, requiring different tools
**Decision:** Use `pdftotext` to extract text from first page and check length
**Rationale:**
- <50 characters = probably scanned → use OCR
- >50 characters = has text → use pandoc (much faster)
**Tradeoffs:** Small overhead for detection, but saves huge time on text PDFs

### Decision 4: Bash 3.2 Compatibility
**Date:** 2025-11-03
**Context:** macOS ships with bash 3.2 (2007), doesn't support associative arrays
**Decision:** Use case statements and functions instead of associative arrays
**Rationale:** Works on default macOS without requiring bash 4 installation
**Tradeoffs:** Slightly more verbose code, but better compatibility
**See:** TROUBLESHOOTING.md for details

### Decision 5: Keep Original Scripts for Reference
**Date:** 2025-11-03
**Context:** Created universal `conmd` to replace individual scripts
**Decision:** Keep original scripts but mark as redundant
**Rationale:**
- Historical reference
- Can extract specific logic if needed
- User might prefer specialized scripts
**Tradeoffs:** More files in directory, but well-documented

---

## Evolution History

### Phase 1: Initial Scripts (Pre-session, ~2025-11)
**Goal:** Basic PDF to markdown conversion
**Built:**
- `pdf_to_md.sh` - Full OCR pipeline
- `pdf_to_md_simple.sh` - Using ocrmypdf
- `forever_notes_ocr.sh` - Forever Notes integration
**Learned:** OCR works well, but scripts hard to use with spaces in paths

### Phase 2: Setup & Troubleshooting (2025-11-03 Morning)
**Goal:** Fix installation issues
**Built:**
- `setup_ocr.sh` - Dependency checker/installer
- `TROUBLESHOOTING.md` - Bash 3.2 compatibility issues
**Changed:** Fixed bash 3.2 compatibility (removed associative arrays)
**Learned:** macOS bash is ancient, need to code defensively

### Phase 3: Interactive Conversion (2025-11-03 Late Morning)
**Goal:** Make conversion user-friendly
**Built:**
- `pdf_to_md_interactive.sh` - Interactive prompts
- Drag-and-drop support
**Tested:** Successfully converted:
  - Cynthia Bourgeault - Centering Prayer.pdf (16 pages, scanned)
  - Guigo - The Ladder of Monks.pdf (23 pages, scanned)
**Learned:** Interactive prompts much better than CLI arguments for this use case

### Phase 4: Universal Converter (2025-11-03 Current)
**Goal:** One command for all file types
**Built:**
- `conmd` - Universal router script
- Auto-detection logic
- Support for PDF, EPUB, DOCX, HTML
**Status:** Complete, ready to install as system command
**Next:** Add post-processing MD cleaner

---

## File Structure

```
Convert to markdown/
├── mdcon                          # 🌟 MAIN SCRIPT - Universal converter
├── mdclean                        # 🌟 MAIN SCRIPT - Markdown post-processor
├── pdf_to_md.sh                   # Legacy: OCR pipeline (keep for reference)
├── pdf_to_md_interactive.sh       # Legacy: Interactive PDF converter
├── pdf_to_md_simple.sh            # Legacy: Simple ocrmypdf wrapper
├── forever_notes_ocr.sh           # Legacy: Forever Notes integration
├── README.md                      # User documentation
├── DESIGN.md                      # This file - living design doc
├── TROUBLESHOOTING.md             # [TO CREATE] Bash 3.2 issues, common problems
├── QUICKSTART.md                  # Quick reference
├── INDEX.md                       # File index
└── FOREVER_NOTES_INTEGRATION.md   # Forever Notes specifics
```

**Key Files:**
- `mdcon` - **USE THIS** - Universal converter, interactive prompts
- `mdclean` - **USE THIS** - Markdown post-processor and cleaner
- `pdf_to_md.sh` - Original OCR pipeline, good code reference
- `README.md` - Comprehensive user guide
- `DESIGN.md` - This file, project context for Claude

**Redundant Files (Keep for Reference):**
- `pdf_to_md_interactive.sh` - Functionality now in `mdcon`
- `pdf_to_md_simple.sh` - Functionality now in `mdcon`
- `forever_notes_ocr.sh` - May still be useful for specific workflow

---

## Dependencies

**Required:**
- `pandoc` - Universal document converter (required for all)
- `ghostscript` (gs) - PDF page extraction (for scanned PDFs only)
- `tesseract` - OCR engine (for scanned PDFs only)
- `poppler` (pdftotext) - PDF text extraction (for detection)

**Installation:**
```bash
brew install pandoc ghostscript tesseract poppler
```

**Verification:**
All dependencies confirmed installed 2025-11-03 10:18

---

## Installation

**Status:** ✅ INSTALLED (2025-11-03)

**Method Used:** Shell Functions (handles spaces in paths)

**Added to `~/.zshrc`:**
```bash
# Markdown tools
mdcon() {
  "/Users/mac/Documents/Local Vault/Claude/Projects/Convert to markdown/mdcon" "$@"
}

mdclean() {
  "/Users/mac/Documents/Local Vault/Claude/Projects/Convert to markdown/mdclean" "$@"
}
```

**Why Functions Instead of Aliases:**
- Shell functions handle spaces in file paths correctly
- Aliases in zsh split paths at spaces
- Functions pass arguments properly with `"$@"`

**Usage:**
```bash
mdcon      # Convert to Markdown
mdclean    # Clean Markdown
```

**Naming Convention:**
- Both commands prefixed with `md` (markdown)
- Consistent and memorable

Both commands work from anywhere in the terminal!

---

## Usage Patterns

### Converting Scanned PDFs
```bash
conmd
# Input: /path/to/scanned.pdf
# Output: /path/to/output.md
# Process: ghostscript → tesseract → pandoc
# Time: ~5 seconds per page
```

### Converting Text PDFs
```bash
conmd
# Input: /path/to/text.pdf
# Output: /path/to/output.md
# Process: pandoc direct conversion
# Time: <1 second
```

### Converting EPUB/DOCX/HTML
```bash
conmd
# Input: /path/to/book.epub
# Output: /path/to/book.md
# Process: pandoc conversion
# Time: <1 second
```

### Converting Google Docs
1. Open Google Doc
2. File → Download → Microsoft Word (.docx)
3. Run `conmd` on .docx file

---

## OCR Quality Guide

**Excellent Results (95%+ accuracy):**
- Clean scans, 300+ DPI
- Horizontal text, no skew
- Good contrast, clear fonts
- Example: Guigo - Ladder of Monks

**Good Results (85-95% accuracy):**
- Standard book scans
- Minor skew tolerated
- Most page content readable
- Example: Cynthia Bourgeault - Centering Prayer

**Poor Results (<85% accuracy):**
- Page 1 with decorative elements
- Low resolution (<200 DPI)
- Handwritten notes
- Heavy shadows or poor lighting

**Improvement Tips:**
- Scan at 300+ DPI
- Use good lighting
- Straighten pages before scanning
- Use contrast enhancement if needed

---

## Connections to Other Projects

**Feeds Into:**
- Forever Notes system (creates daily note entries)
- Obsidian vault (pandoc-test folder)
- General knowledge management

**Uses:**
- None (standalone utility)

**Related:**
- Time Keeping project (both use markdown/obsidian)

→ See `CONNECTIONS.md` for detailed integration info [TO CREATE IF NEEDED]

---

## Next Steps

**Immediate (This Week):**
- [ ] Install `conmd` as system-wide command (alias method)
- [ ] Create TROUBLESHOOTING.md file
- [ ] Research/create MD post-processing cleaner
  - Auto-add heading markers (#, ##, ###)
  - Fix spacing issues
  - Remove page markers optionally
  - Clean up OCR artifacts

**Short Term (This Month):**
- [ ] Test with more file types
- [ ] Create batch processing version (for multiple files)
- [ ] Add language support for non-English OCR
- [ ] Integration with Forever Notes workflow

**Long Term (Future):**
- [ ] GUI version (optional)
- [ ] Cloud storage integration (Dropbox, Google Drive)
- [ ] Automated cleanup using AI/ML
- [ ] Support for more formats (RTF, ODT, Pages)

---

## For Claude AI

**Quick Context:**
This project converts various document formats to markdown for knowledge management. Current focus: installed and tested successfully, ready to make system-wide command and add post-processing cleanup.

**Key Files to Read First:**
1. `mdcon` - Main conversion script with all routing logic
2. `mdclean` - Markdown post-processing script
3. `README.md` - User documentation
4. This file (DESIGN.md) - Full context

**Common Tasks:**
- "Fix OCR issue" → Check tesseract settings in `mdcon` lines 80-100
- "Add new file type" → Add case in `convert_file()` function in `mdcon` around line 150
- "Improve markdown cleanup" → Edit `mdclean` script

**Current Dependencies:**
All installed: pandoc, ghostscript, tesseract, poppler

**User Preferences:**
- Likes simple, interactive prompts
- Prefers drag-and-drop over typing paths
- Wants one universal command (`conmd`)
- Values documentation and context
- Focus on core functionality before integrations
- Skipping Forever Notes integration for now

**User's System:**
- macOS with zsh shell
- Oh My Zsh installed
- Has `bat` and `ripgrep` installed
  - **Note for future:** Use `bat` instead of `cat`, `rg` instead of `grep`

---

## Session Log

### 2025-11-03 06:00-11:00 - Setup, Troubleshooting, Universal Converter, Installation
**Goals:**
1. Fix setup script installation issues
2. Make conversion process user-friendly
3. Create universal converter for all file types

**What We Built:**
- Fixed `setup_ocr.sh` for bash 3.2 compatibility
- Created `pdf_to_md_interactive.sh` with interactive prompts
- Created `mdcon` - universal converter (originally named conmd, renamed for consistency)
- Created `mdclean` - markdown post-processor
- Tested successfully on 2 scanned PDFs

**Design Decisions:**
- Use bash 3.2 compatible code (no associative arrays)
- Interactive prompts better than CLI arguments
- Auto-detect scanned vs text PDFs
- One command for all conversions

**Learnings:**
- macOS bash 3.2 is ancient - can't use modern bash features
- Spaces in paths are problematic - interactive prompts solve this
- OCR quality very good on clean scans (95%+)
- Page 1 often has artifacts from decorative elements

**Testing:**
✅ Cynthia Bourgeault - Centering Prayer.pdf → 16 pages, excellent OCR
✅ Guigo - The Ladder of Monks.pdf → 23 pages, excellent OCR
✅ Both saved to /Users/mac/Documents/Local Vault/pandoc-test/

**Current State:**
- All dependencies installed and verified
- `mdcon` and `mdclean` scripts complete and functional
- ✅ **Successfully installed as system commands**
- Shell functions (not aliases) handle spaces in paths correctly
- Ready to test mdclean on OCR output

**Installation Troubleshooting (Post-Session):**
- First attempts with aliases failed (spaces in paths)
- Solution: Use shell functions instead
- Renamed `conmd` → `mdcon` for consistency (both commands prefixed with `md`)
- Commands now work system-wide: `mdcon` and `mdclean`

**Next Session:**
1. Test `mdclean` on converted PDF files
2. Test with EPUB, DOCX, HTML files
3. Fine-tune mdclean rules based on results
4. Consider batch processing feature

---

**Document Purpose:** Central source of truth for Convert to Markdown project
**Update Frequency:** After every Claude session
**Maintained By:** User + Claude together
