# Quick Start Guide

Get started converting scanned PDFs to markdown in 3 minutes.

## Step 1: Setup (One-Time)

```bash
# Make scripts executable
chmod +x setup_ocr.sh pdf_to_md.sh pdf_to_md_simple.sh

# Run setup to install dependencies
./setup_ocr.sh
```

The setup script will:
- Detect your OS (macOS or Linux)
- Check for required tools
- Offer to install missing dependencies
- Verify installation

## Step 2: Basic Usage

```bash
# Convert a scanned PDF
./pdf_to_md.sh your_scan.pdf

# Output will be: your_scan.md
```

That's it! The script will:
1. Extract pages as images
2. Run OCR on each page
3. Combine into a markdown file
4. Show you a preview

## Step 3: Integration Examples

### For Zettelkasten Workflow

```bash
# Convert scan and open in your editor
./pdf_to_md.sh notebook.pdf
vim notebook.md  # Edit, create atomic notes

# Or directly into your vault
./pdf_to_md.sh scan.pdf ~/ObsidianVault/Fleeting/$(date +%Y-%m-%d)-scan.md
```

### For Forever Notes Daily Journal

```bash
# Add to today's journal entry
today="nov_03"  # or use: $(date +%b_%d | tr '[:upper:]' '[:lower:]')
./pdf_to_md.sh meeting_notes.pdf /tmp/scan.md

# Append to today's note under 2025 section
cat /tmp/scan.md >> ~/ObsidianVault/Journal/${today}.md
```

### Batch Processing

```bash
# Convert all PDFs in a folder
for pdf in ~/Scans/*.pdf; do
    ./pdf_to_md.sh "$pdf" ~/ObsidianVault/Inbox/
done
```

## Common Use Cases

### 1. Handwritten Notes → Zettelkasten

```bash
# Scan notebook pages
# Convert to markdown
./pdf_to_md.sh notebook_scan.pdf notes_raw.md

# Extract atomic ideas (manual step)
# Create individual zettel notes with proper links
```

### 2. Academic Papers

```bash
# Convert paper
./pdf_to_md.sh research_paper.pdf

# Add to literature notes with metadata
```

### 3. Meeting Notes

```bash
# Scan handwritten meeting notes
# Convert and append to daily note
./pdf_to_md.sh meeting.pdf
cat meeting.md >> ~/Journal/$(date +%b_%d).md
```

## Troubleshooting

### "Command not found"

Run the setup script:
```bash
./setup_ocr.sh
```

### OCR quality poor

1. Check your scan resolution (should be 300+ DPI)
2. Try the simple version if scan is clean:
   ```bash
   ./pdf_to_md_simple.sh scan.pdf
   ```

### Permission denied

Make scripts executable:
```bash
chmod +x *.sh
```

## Next Steps

1. **Read the full README** - `cat README.md`
2. **Explore advanced options** - Edit the scripts
3. **Integrate with your workflow** - Add to your daily automation
4. **Customize for your needs** - Modify OCR parameters

## Unix Philosophy Tips

These scripts follow Unix principles - you can compose them:

```bash
# Chain with other tools
./pdf_to_md.sh scan.pdf | grep "important" > highlights.md

# Use in pipes
find ~/Scans -name "*.pdf" | while read pdf; do
    ./pdf_to_md.sh "$pdf"
done

# Combine with sed/awk for processing
./pdf_to_md.sh scan.pdf
sed -i 's/TODO:/- [ ] /g' scan.md  # Convert TODO to checkboxes
```

## Getting Help

```bash
# Show usage
./pdf_to_md.sh --help

# Check dependencies
./setup_ocr.sh

# Test individual tools
tesseract --version
gs --version
pandoc --version
```

---

**Remember:** OCR works best with high-quality scans. If results are poor, rescan at higher resolution with better lighting.
