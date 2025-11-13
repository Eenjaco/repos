# File Status Guide

**Last Updated:** 2025-11-03
**Installation Status:** ✅ Both commands installed and working

---

## 🌟 ACTIVE FILES (Use These)

### Primary Scripts (Installed as System Commands)
- **`mdcon`** - Convert to Markdown - ✅ INSTALLED
  - Handles: PDF (scanned/text), EPUB, DOCX, HTML
  - Interactive prompts
  - Auto-detection of file types
  - Run from anywhere: `mdcon`

- **`mdclean`** - Clean Markdown - ✅ INSTALLED
  - Cleans OCR-generated markdown
  - Auto-detects headings
  - Fixes spacing and common errors
  - Run from anywhere: `mdclean`

**Naming Convention:** Both prefixed with `md` for consistency

### Documentation
- **`DESIGN.md`** - Living design document (you are here!)
- **`README.md`** - User guide and technical reference
- **`QUICKSTART.md`** - Quick reference guide

---

## 📦 LEGACY FILES (Keep for Reference)

### Scripts - Superseded by `mdcon`
- **`pdf_to_md_interactive.sh`**
  - Status: Redundant (functionality in `mdcon`)
  - Keep: Yes (good code reference)
  - Use: Only if you want PDF-only version

- **`pdf_to_md.sh`**
  - Status: Redundant (OCR logic now in `mdcon`)
  - Keep: Yes (shows detailed OCR pipeline)
  - Use: Only for understanding how OCR works

- **`pdf_to_md_simple.sh`**
  - Status: Redundant (simple conversion in `mdcon`)
  - Keep: Yes (ocrmypdf reference)
  - Use: Only if you want ocrmypdf approach

### Special Purpose
- **`forever_notes_ocr.sh`**
  - Status: May still be useful
  - Keep: Yes
  - Use: If you need Forever Notes integration

---

## 📚 DOCUMENTATION FILES

### Keep All
- `INDEX.md` - File organization reference
- `FOREVER_NOTES_INTEGRATION.md` - Forever Notes specific docs
- `FILE-STATUS.md` - This file

### To Create
- `TROUBLESHOOTING.md` - Common issues and solutions
- `CONNECTIONS.md` - If project integrates with others

---

## 🗑️ SAFE TO DELETE (None Currently)

All files serve a purpose - either active use or reference.

---

## Recommendation

**Keep current structure:**
- Clear which file to use (`conmd`)
- Legacy files useful for reference
- Good documentation

**If you want to clean up:**
Create a `legacy/` subdirectory and move:
```bash
mkdir legacy
mv pdf_to_md.sh legacy/
mv pdf_to_md_simple.sh legacy/
mv pdf_to_md_interactive.sh legacy/
```

But not urgent - directory is well-organized.

---

## Quick Reference

**Want to convert a file?** → Use `mdcon`
**Want to clean markdown?** → Use `mdclean`
**Want to understand OCR?** → Read `pdf_to_md.sh`
**Want to understand project?** → Read `DESIGN.md`
**Need quick help?** → Read `QUICKSTART.md`
**Detailed docs?** → Read `README.md`

---

## 🔧 Installation Notes

**Method:** Shell functions in `~/.zshrc` (not aliases)
**Why:** Functions handle spaces in paths correctly

**Installed commands:**
```bash
mdcon      # Convert to Markdown - Run from anywhere
mdclean    # Clean Markdown - Run from anywhere
```

**Naming:** Both prefixed with `md` for consistency

**Location of actual scripts:**
`/Users/mac/Documents/Local Vault/Claude/Projects/Convert to markdown/`

**To uninstall:** Remove function definitions from `~/.zshrc`

**Rename History:**
- Originally `conmd` → renamed to `mdcon` for consistency with `mdclean`
