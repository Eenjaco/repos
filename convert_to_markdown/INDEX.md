# PDF to Markdown OCR Converter - Complete Package

Everything you need to convert scanned PDFs to markdown for your knowledge management system.

## 📦 What's Included

### Core Scripts

1. **`pdf_to_md.sh`** - Full-featured conversion script
   - Transparent process (see each step)
   - Maximum control over OCR parameters
   - Educational - understand how it works
   - Best for: Learning, customization, problem scans

2. **`pdf_to_md_simple.sh`** - Streamlined conversion
   - Uses ocrmypdf for simplicity
   - Faster, more automated
   - Best for: Quick conversions, batch processing

3. **`forever_notes_ocr.sh`** - Forever Notes integration
   - Converts and adds to daily notes automatically
   - Preserves your journal structure
   - Best for: Daily capture workflow

4. **`setup_ocr.sh`** - Dependency installer
   - Checks what's installed
   - Offers to install missing tools
   - Works on macOS and Linux

### Documentation

1. **`README.md`** - Complete reference guide
   - How everything works
   - Unix philosophy connections
   - Advanced usage examples
   - Troubleshooting

2. **`QUICKSTART.md`** - Get started in 3 minutes
   - Installation steps
   - Basic usage
   - Common examples

3. **`FOREVER_NOTES_INTEGRATION.md`** - Journal workflow guide
   - Integration with Forever Notes
   - Daily capture workflows
   - Zettelkasten connections
   - Automation ideas

4. **`THIS_FILE.md`** - Package index (you're reading it!)

## 🚀 Quick Start

```bash
# 1. Setup dependencies
chmod +x setup_ocr.sh
./setup_ocr.sh

# 2. Make scripts executable (if setup didn't)
chmod +x pdf_to_md.sh pdf_to_md_simple.sh forever_notes_ocr.sh

# 3. Test basic conversion
./pdf_to_md.sh your_scan.pdf

# 4. Or integrate with Forever Notes
# (Edit VAULT_PATH first!)
vim forever_notes_ocr.sh  # Set your vault path
./forever_notes_ocr.sh your_scan.pdf
```

## 📚 Which Script Should I Use?

### For Learning & Experimentation
→ Use `pdf_to_md.sh`
- See how OCR works step-by-step
- Customize every parameter
- Understand the pipeline

### For Quick Conversions
→ Use `pdf_to_md_simple.sh`
- Just works™
- Fast and reliable
- Less noise in output

### For Daily Knowledge Capture
→ Use `forever_notes_ocr.sh`
- Integrates with your Forever Notes system
- Maintains structure
- Part of your daily workflow

## 🔧 Dependencies

All scripts require:
- **ghostscript** (`gs`) - PDF manipulation
- **tesseract** - OCR engine
- **pandoc** - Format conversion

Simple script additionally needs:
- **ocrmypdf** - Streamlined OCR processing
- **pdftotext** - Text extraction (from poppler)

Optional but useful:
- **imagemagick** (`convert`) - Image preprocessing

## 📖 Reading Order

**New to OCR and CLI tools?**
1. Start with `QUICKSTART.md`
2. Read `README.md` sections as needed
3. Experiment with `pdf_to_md.sh`

**Just want it working?**
1. Run `setup_ocr.sh`
2. Use `pdf_to_md_simple.sh`
3. Check `QUICKSTART.md` if issues

**Integrating with Forever Notes?**
1. Set up basic conversion first
2. Read `FOREVER_NOTES_INTEGRATION.md`
3. Configure and test `forever_notes_ocr.sh`
4. Build it into your daily routine

## 🔄 Workflow Patterns

### Pattern 1: Ad-hoc Conversion
```bash
# Got a scan? Convert it.
./pdf_to_md.sh document.pdf
```

### Pattern 2: Batch Processing
```bash
# Convert all PDFs in folder
for pdf in ~/Scans/*.pdf; do
    ./pdf_to_md_simple.sh "$pdf"
done
```

### Pattern 3: Daily Capture
```bash
# Evening routine: process today's scans
./forever_notes_ocr.sh notebook_scan.pdf
# Review in Obsidian
# Add wikilinks
# Extract permanent notes during weekly review
```

### Pattern 4: Automated Pipeline
```bash
# Watch folder for new scans
# Add to crontab:
*/10 * * * * find ~/Scans -name "*.pdf" -mmin -10 -exec ~/scripts/pdf_to_md.sh {} \;
```

## 🎯 Integration with Your System

### Zettelkasten Workflow
```
Handwritten → Scan → OCR → Fleeting Notes → Literature Notes → Permanent Zettels
```

### Forever Notes Workflow
```
Notebook → Scan → forever_notes_ocr.sh → Daily Note (2025 section) → Weekly Review
```

### Mental Models / Systems Thinking
- **Input:** Analog notes (your thinking on paper)
- **Process:** OCR pipeline (transformation)
- **Output:** Digital markdown (searchable, linkable)
- **Feedback:** Review → Refine → Improve scan quality

## 🛠️ Customization Ideas

### Enhance OCR Quality
Edit `pdf_to_md.sh`:
```bash
# Add preprocessing step
for page in "$temp_dir"/page_*.png; do
    convert "$page" -deskew 40% -contrast-stretch 0 "$page"
    tesseract "$page" ...
done
```

### Auto-add Tags
Edit `forever_notes_ocr.sh`:
```bash
# Add custom tags to OCR'd content
CONTENT="$CONTENT

#handwritten #fleeting #$(date +%Y-%m-%d)"
```

### Better Wikilinks
```bash
# Auto-create wikilinks for keywords
CONTENT=$(echo "$CONTENT" | sed 's/\bsystems thinking\b/[[Systems Thinking]]/gi')
```

## 🧩 Unix Philosophy in Practice

These scripts demonstrate core Unix principles:

1. **Modularity** - Each tool does one thing well
   - `gs` splits PDFs
   - `tesseract` does OCR
   - `pandoc` converts formats

2. **Composition** - Tools work together
   ```bash
   gs → tesseract → pandoc → your_note.md
   ```

3. **Text as interface** - Everything flows through plain text
   - PDFs become text
   - Text becomes markdown
   - Markdown feeds your knowledge system

4. **Simplicity** - Scripts are readable, modifiable
   - No magic
   - Clear steps
   - Easy to debug

## 🐛 Troubleshooting Quick Reference

| Problem | Solution |
|---------|----------|
| Command not found | Run `./setup_ocr.sh` |
| Poor OCR quality | Rescan at 300+ DPI, better lighting |
| Forever Notes not found | Check `VAULT_PATH` in script |
| Permission denied | `chmod +x *.sh` |
| Empty output | Check if PDF is actually scanned (not text PDF) |

## 📊 File Sizes & Performance

**Typical conversion times (300 DPI scans):**
- 1 page: ~5-10 seconds
- 10 pages: ~1-2 minutes
- 50 pages: ~5-10 minutes

**Disk space:**
- Scripts: ~50KB total
- Temp files during conversion: ~10MB per page (auto-cleaned)
- Final markdown: ~10-50KB per page

## 🔐 Privacy & Security

All processing happens **locally on your machine**:
- No cloud services
- No data leaves your computer
- No API calls
- No internet required (after dependencies installed)

Perfect for sensitive documents, private notes, confidential work.

## 🚧 Future Enhancements

Ideas for extending these scripts:

1. **GUI wrapper** - Drag-and-drop interface
2. **Watch service** - Auto-process new scans
3. **Mobile scanning** - iOS Shortcuts integration
4. **Multi-language** - Add language detection
5. **Smart linking** - Auto-detect and create wikilinks
6. **Quality metrics** - Report OCR confidence scores

## 🤝 Contributing

Want to improve these scripts?

1. Test on your system
2. Note what works / doesn't work
3. Share improvements
4. Follow Unix philosophy: keep it simple, composable

## 📜 License

These scripts are provided as-is for learning and personal use.

Core tools used:
- Ghostscript: AGPL
- Tesseract: Apache 2.0
- Pandoc: GPL
- ocrmypdf: MPL 2.0

## 🎓 Learning Resources

Want to learn more about the tools and concepts?

**OCR & Document Processing:**
- Tesseract docs: https://github.com/tesseract-ocr/tesseract
- Ghostscript manual: https://www.ghostscript.com/doc/
- Pandoc guide: https://pandoc.org/MANUAL.html

**Unix Philosophy:**
- "The Art of Unix Programming" by ESR
- "Unix and Linux System Administration Handbook"

**Knowledge Management:**
- "How to Take Smart Notes" by Sönke Ahrens
- Forever Notes system: https://www.myforevernotes.com/
- Zettelkasten method: https://zettelkasten.de/

**Systems Thinking:**
- "Thinking in Systems" by Donella Meadows
- "The Fifth Discipline" by Peter Senge

## 📞 Getting Help

1. **Check documentation** - Start with QUICKSTART.md
2. **Test basic commands** - Verify each tool works individually
3. **Review logs** - Scripts show what's happening
4. **Simplify** - Test with a small, clear scan first

## ✅ Checklist for Success

Before first use:
- [ ] Run `setup_ocr.sh`
- [ ] Verify dependencies installed
- [ ] Test `pdf_to_md.sh` with a sample PDF
- [ ] Read QUICKSTART.md

For Forever Notes integration:
- [ ] Set `VAULT_PATH` in forever_notes_ocr.sh
- [ ] Test on a single note first
- [ ] Verify backup created
- [ ] Check content appears correctly
- [ ] Build into daily routine

For optimal results:
- [ ] Scan at 300+ DPI
- [ ] Use good lighting
- [ ] Keep paper flat
- [ ] Write clearly (if handwritten)
- [ ] Review OCR output
- [ ] Add wikilinks manually
- [ ] Extract insights to permanent notes

---

## 🎉 You're Ready!

You now have:
- ✅ Complete OCR to Markdown pipeline
- ✅ Forever Notes integration
- ✅ Knowledge management workflows
- ✅ Unix-philosophy-compliant tools
- ✅ Full documentation

Start with a single scan, see how it works, then integrate into your daily practice.

**Happy knowledge building!** 📚→💭→🔗
