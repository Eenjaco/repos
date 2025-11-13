# PDF to Markdown OCR Converter

Convert scanned PDFs to markdown files for your knowledge management system using CLI tools and Unix philosophy principles.

## Overview

These scripts bridge the gap between paper/scanned documents and your digital `.md` knowledge base. Perfect for:

- Converting handwritten notebook scans to searchable markdown
- Processing scanned articles/papers into your Obsidian vault
- Building your Zettelkasten from physical notes
- Creating a unified knowledge lattice across analog and digital sources

### For Scanned PDFs (Images of Pages)

  You have 2 scripts available:

  Option 1: Full OCR Script (Recommended)

  cd "/Users/mac/Documents/Local Vault/Claude/Projects/Convert to markdown"
  chmod +x pdf_to_md.sh
  ./pdf_to_md.sh "/path/to/your/file.pdf"

  Option 2: Simple Script

  cd "/Users/mac/Documents/Local Vault/Claude/Projects/Convert to markdown"
  chmod +x pdf_to_md_simple.sh
  ./pdf_to_md_simple.sh "/path/to/your/file.pdf"

  ---
  What Happens:

  1. OCR extracts text from the scanned images (using Tesseract)
  2. Converts to markdown format
  3. Saves output as filename.md in the same directory

## Scripts Provided

### 1. `pdf_to_md.sh` - Full Control Version

**Unix Philosophy Applied:**
- Does one thing well (PDF → OCR → Markdown)
- Composable (uses gs, tesseract, pandoc separately)
- Transparent process (shows each step)
- Standard input/output

**When to use:** 
- Learning how the process works
- Need fine-grained control
- Want to customize OCR parameters
- Processing low-quality scans

### 2. `pdf_to_md_simple.sh` - Streamlined Version

**Unix Philosophy Applied:**
- Leverage specialized tools (ocrmypdf)
- Keep it simple
- Fast and reliable

**When to use:**
- Quick conversions
- High-quality scans
- Batch processing
- Just want it to work

### Make Scripts Executable

```bash
chmod +x pdf_to_md.sh pdf_to_md_simple.sh
```

## Usage

### Basic Conversion

```bash
# Output will be input_name.md
./pdf_to_md.sh scanned_notes.pdf

# Specify output name
./pdf_to_md.sh scanned_notes.pdf fleeting_notes_2025-11-03.md

# Simple version
./pdf_to_md_simple.sh book_chapter.pdf
```

### Batch Processing

```bash
# Convert all PDFs in current directory
for pdf in *.pdf; do
    ./pdf_to_md.sh "$pdf"
done

# Or using find (Unix way)
find . -name "*.pdf" -exec ./pdf_to_md.sh {} \;
```

## How It Works

### Technical Pipeline (pdf_to_md.sh)

```
┌─────────────┐
│ Scanned PDF │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│ Ghostscript (gs)    │  Split PDF → PNG images (300 DPI)
│ -dBATCH -sDEVICE... │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Tesseract OCR       │  Image → Text (page by page)
│ --psm 3 -l eng      │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Pandoc              │  Text → Markdown
│ -f plain -t md      │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Output: .md file    │
└─────────────────────┘
```

### Why These Tools?

**Ghostscript (gs):**
- Industry standard for PDF manipulation
- Converts PDF pages to high-res images
- Unix tool since 1988

**Tesseract:**
- Google's open-source OCR engine
- Highly accurate, supports 100+ languages
- Originally developed at HP in 1985

**Pandoc:**
- Universal document converter
- Markdown-native
- Perfect for knowledge management workflows

**ocrmypdf (simple version):**
- Wraps tesseract with PDF-specific optimizations
- Adds searchable text layer to PDFs
- Better for clean scans

## Tips for Better OCR Results

1. **Scan Quality:**
   - Use 300 DPI or higher
   - Ensure good lighting (no shadows)
   - Keep text horizontal (not skewed)

2. **Pre-processing:**
   ```bash
   # Increase contrast before OCR
   convert input.pdf -colorspace gray -normalize output.pdf
   ```

3. **Language Support:**
   ```bash
   # Install additional languages for Tesseract
   brew install tesseract-lang  # macOS
   sudo apt install tesseract-ocr-deu  # German on Linux
   
   # Use in script
   tesseract image.png output -l deu  # German
   ```

4. **Multiple Columns:**
   ```bash
   # For newspapers/academic papers (modify tesseract line)
   tesseract "$page" output --psm 1  # Automatic page segmentation
   ```

## Unix Philosophy & Systems Thinking

These scripts embody several Unix principles:

1. **Modularity:** Each tool (gs, tesseract, pandoc) does one thing well
2. **Composition:** Tools pipe together to create complex functionality
3. **Text as universal interface:** Everything flows through plain text
4. **Transparency:** Each step is visible and debuggable

**Systems Thinking Connection:**
- **Input:** Scanned PDF (analog → digital bridge)
- **Transformation:** OCR pipeline (adding structure to unstructured data)
- **Output:** Markdown (feeds your knowledge lattice)
- **Feedback:** Preview shows quality, iterate if needed

## Integrating with Your Knowledge Management

### Zettelkasten Workflow

```bash
# 1. Scan your handwritten fleeting notes
# 2. Convert to markdown
./pdf_to_md.sh notebook_scan.pdf

# 3. Extract atomic ideas
vim notebook_scan.md  # Edit, split into atomic notes

# 4. Move to permanent notes with proper linking
# Create individual zettels from the OCR'd text
```

### Forever Notes Integration

```bash
# Add scanned content to today's daily note
./pdf_to_md.sh scan.pdf /tmp/scan_temp.md
cat /tmp/scan_temp.md >> ~/ObsidianVault/Journal/nov_03.md
```

### Automation Ideas

```bash
# Watch folder for new scans
# Add to your crontab or create a launchd job
*/5 * * * * find ~/Scans -name "*.pdf" -mtime -1 -exec ~/scripts/pdf_to_md.sh {} \;
```

## Troubleshooting

### OCR Quality Issues

```bash
# Check Tesseract version
tesseract --version

# Test OCR on single image
gs -dBATCH -dNOPAUSE -sDEVICE=png16m -r300 -sOutputFile=test.png input.pdf
tesseract test.png output --psm 3
cat output.txt
```

### Missing Dependencies

```bash
# Check what's installed
for cmd in gs tesseract pandoc ocrmypdf; do
    command -v $cmd && echo "$cmd: installed" || echo "$cmd: missing"
done
```

### Permission Errors

```bash
# Make scripts executable
chmod +x pdf_to_md.sh pdf_to_md_simple.sh

# Verify
ls -la pdf_to_md*.sh
```

## Advanced Usage

### Custom OCR Language

Edit the tesseract line in `pdf_to_md.sh`:

```bash
tesseract "$page" "$temp_dir/temp_ocr" -l eng+deu --psm 3
```

### Better Markdown Formatting

Add post-processing with `sed` or `awk`:

```bash
# Example: Convert "Chapter 1" to # Chapter 1
sed -i 's/^Chapter \([0-9]\+\)/# Chapter \1/g' output.md
```

### Preprocessing Images

```bash
# Add before OCR step in script
for page in "$temp_dir"/page_*.png; do
    # Deskew, increase contrast, remove noise
    convert "$page" \
        -deskew 40% \
        -contrast-stretch 0 \
        -morphology Close Diamond \
        "$page"
done
```

## Moving to Linux (Omarchy)

These scripts are 100% compatible with Linux! When you migrate:

1. **Dependencies install faster** (apt is quicker than Homebrew)
2. **Better system integration** (systemd for automation)
3. **Lower resource usage** (no macOS overhead)

No script changes needed - that's the Unix philosophy in action!

## Further Reading

- [Tesseract Documentation](https://github.com/tesseract-ocr/tesseract)
- [Ghostscript User Manual](https://www.ghostscript.com/doc/current/Use.htm)
- [Pandoc User's Guide](https://pandoc.org/MANUAL.html)
- [Unix Philosophy](https://en.wikipedia.org/wiki/Unix_philosophy)

## Contributing

These scripts follow Unix principles:
- Keep them simple
- Make them composable
- Document clearly
- Fail gracefully

Feel free to modify for your workflow!

---

**Note:** OCR accuracy depends on scan quality. For best results, use high-resolution scans (300+ DPI) with good contrast and minimal skew.
