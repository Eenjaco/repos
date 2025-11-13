# CLI UX Proposal for docforge

## Name: `docforge`

**Tagline:** "Forge any document into structured knowledge"

## Command Structure

### Basic Usage (Smart Defaults)

```bash
# Single file - auto-detect everything
docforge document.pdf

# Auto-detects:
# - File type (PDF)
# - Best processing pipeline
# - Output location (same folder, .md extension)
# - Whether AI cleaning is beneficial

# Batch processing
docforge --batch ~/Documents/inbox/

# From clipboard
docforge --clipboard

# From URL
docforge https://example.com/article.html
```

### Interactive Mode

When ambiguity exists or user wants control:

```bash
$ docforge document.pdf

📄 document.pdf (723 KB)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Detected: PDF with text layer

Pipeline:
  1. Extract text with pdftotext
  2. Structure with Unstructured
  3. Clean with Ollama (llama3.2:1b)
  4. Format for Obsidian

Output: document.md (same folder)

Options:
  [Enter]  Continue with defaults
  [m]      Choose different model
  [o]      Change output location
  [s]      Skip AI cleaning (faster)
  [p]      Change preset
  [a]      Advanced options
  [q]      Quit

> _
```

### Preset System

```bash
# Optimized workflows for common tasks
docforge book.pdf --preset book
docforge notes.jpg --preset ocr
docforge lecture.mp3 --preset transcribe
docforge transactions.csv --preset financial
docforge recipe.html --preset web-clip
```

**Preset Definitions:**

```yaml
presets:
  book:
    model: llama3.2:3b
    chunk_size: 8000
    detect_chapters: true
    preserve_references: true
    output_format: obsidian

  ocr:
    force_ocr: true
    handwriting_mode: true
    model: llama3.2:1b
    cleanup_aggressive: true

  transcribe:
    audio_quality: high
    timestamps: true
    speaker_detection: true
    model: llama3.2:1b

  financial:
    csv_mode: auto
    analyze: true
    model: llama3.2:1b
    math_formulas: true
    charts: true

  web-clip:
    extract_main_content: true
    remove_navigation: true
    preserve_links: true
    model: llama3.2:1b
```

### Flags and Options

```bash
# Input
docforge <file>                    # Single file
docforge --batch <folder>          # Batch process
docforge --watch <folder>          # Watch mode (auto-process new files)
docforge --clipboard               # Process clipboard content
docforge --url <url>               # Download and process

# Output
-o, --output <path>                # Output location
--format <obsidian|notion|plain>   # Output format
--name <pattern>                   # Naming pattern (date, original, custom)

# Processing
--preset <name>                    # Use preset configuration
--model <name>                     # Ollama model
--no-llm                          # Skip AI cleaning
--analyze                         # Deep analysis (for CSV/data)
--ocr                             # Force OCR (even if text layer exists)
--language <code>                 # Hint for language detection

# Behavior
--interactive                     # Always show interactive prompt
--yes                            # Auto-accept all defaults (CI mode)
--dry-run                        # Show what would happen
--verbose                        # Detailed logging
--quiet                          # Minimal output

# Advanced
--chunk-size <n>                 # Token chunk size for long docs
--temperature <n>                # Ollama temperature
--context <path>                 # Additional context file for AI
```

### Configuration File

```bash
# ~/.config/docforge/config.yaml
default_model: llama3.2:1b
default_output: ~/Documents/vault/inbox/
always_analyze_csv: true
obsidian_vault: ~/Documents/vault/

presets:
  my-workflow:
    model: llama3.2:3b
    output_format: obsidian
    custom_prompt: "path/to/prompt.txt"

# Override with CLI flags
docforge file.pdf  # uses config.yaml defaults
docforge file.pdf --model llama3.2:3b  # overrides model
```

## Progress Indicators

### Single File

```bash
$ docforge large-book.pdf

📚 large-book.pdf (2.1 MB)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣  Extracting text...          ✓ Done (2.3s)
2️⃣  Structuring content...      ✓ Done (0.8s)
3️⃣  Cleaning with Ollama...     ⏳ Processing...
    └─ Page 47/234 (20%)        [████████░░░░░░░░░░░░]

4️⃣  Formatting for Obsidian...  ⏳ Waiting...

Estimated time remaining: 3m 12s
```

### Batch Processing

```bash
$ docforge --batch ~/Documents/inbox/

🔍 Scanning ~/Documents/inbox/
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Found 47 files:
  • 23 PDFs (18.4 MB)
  • 12 Images (5.2 MB)
  • 8 DOCX (3.1 MB)
  • 4 MP3 (156 MB)

Total size: 182.7 MB
Estimated time: ~18 minutes

Continue? [Y/n]: y

Processing...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
████████████████████████████░░░░░ 85% (40/47)

✓ annual-report.pdf (12s)
✓ meeting-notes.jpg (8s)
✓ presentation.pptx (5s)
⏳ lecture-recording.mp3 (2m 34s remaining)

Success: 39 | Failed: 1 | Remaining: 7
```

## Error Handling

```bash
$ docforge corrupted.pdf

❌ Error processing corrupted.pdf
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Problem: File appears to be corrupted or encrypted

Suggestions:
  1. Try opening in Preview/Acrobat to verify
  2. If encrypted, use --password flag
  3. If scanned PDF, try --force-ocr

Need help? Run: docforge --help
Report issues: https://github.com/user/docforge/issues
```

## Help System

```bash
$ docforge --help

docforge - Forge any document into structured knowledge
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Usage:
  docforge <file>              Process single file
  docforge --batch <folder>    Process folder
  docforge --help <topic>      Detailed help

Common Commands:
  docforge book.pdf                    # Process with auto-detection
  docforge --batch ~/Documents/        # Batch process folder
  docforge notes.jpg --preset ocr      # OCR with optimization
  docforge audio.mp3 --preset transcribe  # Transcribe audio

Examples:
  # Basic usage
  docforge document.pdf

  # With options
  docforge report.docx --output ~/vault/ --model llama3.2:3b

  # Financial analysis
  docforge expenses.csv --analyze

  # Batch processing
  docforge --batch ~/Downloads/ --yes --quiet

Topics:
  presets      Learn about preset workflows
  formats      Supported file formats
  models       Available Ollama models
  config       Configuration file
  advanced     Advanced options

Version: 1.0.0
Docs: https://docforge.dev
```

## Status/Info Commands

```bash
# Check system
docforge --doctor
# ✓ pandoc installed (v3.1.2)
# ✓ poppler installed (v24.0)
# ✓ tesseract installed (v5.3.0)
# ✓ ffmpeg installed (v6.0)
# ✓ Ollama running
# ✓ Model llama3.2:1b available
# ✗ Model llama3.2:3b not found
#   → Run: ollama pull llama3.2:3b

# List presets
docforge --list-presets
# Available presets:
#   book             Optimized for books and long documents
#   ocr              OCR with handwriting support
#   transcribe       Audio transcription with timestamps
#   financial        Financial analysis with calculations
#   web-clip         Web page content extraction

# Show statistics
docforge --stats
# Documents processed: 1,247
# Total size: 8.2 GB
# Success rate: 97.3%
# Average time: 8.2s per file
# Most used: PDF (623), DOCX (234), Images (198)
```

## Integration Examples

### Shell Aliases

```bash
# ~/.zshrc or ~/.bashrc
alias forge="docforge"
alias forgebatch="docforge --batch"
alias forgeocr="docforge --preset ocr"
```

### Alfred/Raycast Workflow

```bash
# Quick Action: Select file(s) in Finder → Cmd+Opt+D → docforge
```

### Obsidian Integration

```bash
# Auto-process files dropped in Obsidian inbox
docforge --watch ~/Documents/vault/inbox/ --output ~/Documents/vault/processed/
```

### Hazel Rule (Mac Automation)

```bash
# Hazel: Monitor ~/Downloads/
# If file matches: *.pdf, *.docx, *.jpg
# Run: docforge "$1" --output ~/vault/inbox/ --quiet
```

## Watch Mode

```bash
$ docforge --watch ~/Downloads/

👁️  Watching ~/Downloads/
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Waiting for files... (Press Ctrl+C to stop)

[10:23:45] New file detected: meeting-notes.pdf
[10:23:45]   → Processing...
[10:23:58]   ✓ Done → output/meeting-notes.md

[10:24:12] New file detected: receipt.jpg
[10:24:12]   → Processing with OCR...
[10:24:19]   ✓ Done → output/receipt.md

Processed: 2 files | Errors: 0
```

## Design Principles

1. **Smart Defaults**: Works without flags 90% of the time
2. **Progressive Disclosure**: Simple by default, powerful when needed
3. **Fast Feedback**: Show progress immediately
4. **Helpful Errors**: Tell user what to do, not just what went wrong
5. **Consistent UX**: Same patterns throughout
6. **Respectful**: Ask permission for batch operations
7. **Offline-First**: Works without internet
8. **Composable**: Plays well with other Unix tools

## Example Sessions

### Beginner User

```bash
$ docforge book.pdf
✓ Done! Created book.md (in same folder)
```

### Intermediate User

```bash
$ docforge --batch ~/Documents/
Found 47 files. Continue? [Y/n]: y
Processing... ████████████████████ 100%
✓ 46 files processed | 1 failed
Failed: corrupted.pdf (file encrypted)
```

### Power User

```bash
$ docforge *.pdf --batch \
  --output ~/vault/books/ \
  --preset book \
  --model llama3.2:3b \
  --parallel 4 \
  --format obsidian \
  --tag "to-review" \
  --frontmatter "status: inbox" \
  --yes \
  | tee process.log
```

## Future: Voice Commands (with Siri Shortcuts)

```bash
"Hey Siri, docforge the document I just downloaded"
"Hey Siri, forge all my meeting notes"
```

This CLI design balances simplicity for beginners with power for advanced users.
