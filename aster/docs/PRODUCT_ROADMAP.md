# docforge Product Roadmap

## Current Status: ✅ Foundation Complete

You have:
- ✅ Universal document processor (16+ formats)
- ✅ CSV/Excel with financial analysis
- ✅ OCR for images
- ✅ Audio transcription support
- ✅ Ollama AI integration
- ✅ Comprehensive test suite
- ✅ Optimized prompts for different content types

## Vision

**"Forge any document into structured knowledge - from anywhere, on any device"**

Transform docforge from a CLI tool into a universal document processing platform accessible from iPhone, web, desktop, and CLI.

## Name Change: mdclean_universal → docforge

**Rationale:**
- Single word (CLI-friendly)
- Memorable and descriptive
- "Forge" implies transformation and craftsmanship
- Available as domain and command name

**Usage:**
```bash
# Old
./mdclean_universal.py document.pdf

# New
docforge document.pdf
```

## Roadmap Phases

### Phase 1: Enhanced CLI (Week 1) 🎯 START HERE

**Goal:** Beautiful, intuitive command-line experience

**Features:**
- ✨ Interactive mode with smart prompts
- 📊 Beautiful progress bars (rich library)
- 🎨 Colored output and emoji indicators
- ⚙️ Preset system (book, ocr, transcribe, financial)
- 📋 Config file support (~/.config/docforge/config.yaml)
- 🔍 `docforge --doctor` health check
- 📈 `docforge --stats` usage statistics

**User Experience:**
```bash
# Just works
docforge document.pdf

# Interactive when needed
docforge document.pdf
# → Detected: PDF (723 KB)
# → Pipeline: Extract → Structure → Clean with Ollama
# → Options: [Enter] Continue | [m] Change model | [o] Output...

# Presets for common tasks
docforge book.pdf --preset book
docforge notes.jpg --preset ocr
docforge lecture.mp3 --preset transcribe
docforge expenses.csv --preset financial
```

**Deliverables:**
- [ ] Rename project to docforge
- [ ] Implement rich progress bars
- [ ] Add interactive mode
- [ ] Create preset system
- [ ] Add config file support
- [ ] Build --doctor and --stats commands
- [ ] Update all documentation

**Time:** 5-7 days
**Complexity:** Low-Medium
**Dependencies:** None

---

### Phase 2: Web Interface (Week 2-3) 🌐

**Goal:** Access docforge from any device via browser

**Features:**
- 🌐 Flask/FastAPI web server
- 📤 Drag-and-drop file upload
- 🔄 Real-time progress updates
- 📥 Download processed files
- 🎛️ Preset selection UI
- 📊 Processing queue management
- 🔐 Simple authentication (API key or password)

**Architecture:**
```
Browser (iPhone/iPad/Mac) → FastAPI Server → docforge CLI → Ollama
```

**User Experience:**
1. Open http://your-mac-ip:8000 on iPhone
2. Drag/drop or select file
3. Choose preset (auto/book/ocr/etc.)
4. Watch progress bar
5. Download markdown result

**Deliverables:**
- [ ] FastAPI backend with file upload
- [ ] Background job processing
- [ ] Progress tracking with WebSockets or polling
- [ ] Clean web UI (HTML/CSS/JS)
- [ ] Download endpoint for results
- [ ] Basic authentication
- [ ] Docker support (optional)

**Time:** 7-10 days
**Complexity:** Medium
**Dependencies:** Phase 1 CLI

**Stack:**
- Backend: FastAPI + Background tasks
- Frontend: HTML/CSS/JS (vanilla or Alpine.js)
- Storage: Local filesystem
- Queue: In-memory or Redis (optional)

---

### Phase 3: Desktop GUI (Week 4-6) 🖥️

**Goal:** Native app for Mac/Windows/Linux

**Features:**
- 🖱️ Native drag-and-drop
- 📁 Watch folders (auto-process new files)
- 🔔 System notifications
- ⚙️ Preferences UI
- 📊 Statistics dashboard
- 🎨 System tray integration
- 🔄 Batch processing UI

**Technology:** Tauri (Rust + Web)

**Advantages over Electron:**
- Tiny size (~3MB vs 150MB)
- Better performance
- Native feel
- Secure by default

**User Experience:**
- Menu bar app with docforge icon
- Click icon → drop files or browse
- Shows processing queue
- Notifications when complete
- Access settings via tray menu

**Deliverables:**
- [ ] Tauri app setup
- [ ] Drag-and-drop file handling
- [ ] Integration with CLI backend
- [ ] Progress UI with queue
- [ ] Settings panel
- [ ] System tray integration
- [ ] Auto-updater
- [ ] Mac/Windows/Linux builds

**Time:** 2-3 weeks
**Complexity:** Medium-High
**Dependencies:** Phase 1 CLI

---

### Phase 4: iOS App (Month 2-3) 📱

**Goal:** Process documents from iPhone/iPad

**Features:**
- 📱 Native iOS app
- 📷 Camera integration (OCR mode)
- 🔄 Share extension ("Share to docforge")
- 📋 Clipboard support
- 🔔 Push notifications when complete
- 📂 Files app integration
- 🎙️ Shortcuts support
- 🌍 Remote processing (sends to Mac/server)

**Technology:** SwiftUI (Native iOS)

**User Experience:**
1. Open app or use share sheet
2. Select/capture document
3. Choose preset
4. File uploads to Mac/server
5. Get notification when done
6. View/download result

**Architecture:**
```
iOS App → REST API (Phase 2) → Mac/Server → docforge + Ollama
```

**Deliverables:**
- [ ] iOS app with SwiftUI
- [ ] Camera integration with document scanner
- [ ] Share extension
- [ ] API client for remote processing
- [ ] Push notifications
- [ ] Files app integration
- [ ] Shortcuts actions
- [ ] TestFlight beta

**Time:** 4-6 weeks
**Complexity:** High
**Dependencies:** Phase 2 Web API

---

### Phase 5: Advanced Features (Month 3-4) 🚀

**Goal:** Enterprise-ready and power user features

**Features:**

**Performance:**
- ⚡ Parallel processing
- 📦 Batch optimization
- 🎯 GPU acceleration for OCR (optional)
- 💾 Caching system

**Intelligence:**
- 🧠 Content-type detection (automatic prompt selection)
- 📚 Custom prompt templates
- 🔄 Model selection based on content
- 📊 Quality scoring and validation

**Integration:**
- 🗂️ Obsidian plugin
- 📓 Notion integration
- 💾 Cloud storage (Dropbox/iCloud/Google Drive)
- 📧 Email processing
- 🤖 Telegram bot
- 🔗 Zapier/Make integration

**Enterprise:**
- 👥 Multi-user support
- 🔐 Full authentication (OAuth)
- 📊 Usage analytics
- 💰 API rate limiting
- 🏢 Team/organization accounts

**Deliverables:**
- [ ] Parallel processing engine
- [ ] Content-type detection and auto-prompts
- [ ] Obsidian plugin
- [ ] Cloud storage integration
- [ ] Multi-user system with auth
- [ ] Analytics dashboard

**Time:** 4-6 weeks
**Complexity:** High
**Dependencies:** Phases 1-4

---

## Immediate Next Steps (This Week)

### Step 1: Rename Project (1-2 hours)

```bash
# File/folder renames
mv mdclean_universal docforge
mv mdclean_universal.py docforge.py

# Update imports and references
# Update README
# Update documentation

# Make executable
chmod +x docforge.py
ln -s docforge.py docforge

# Test
./docforge document.pdf
```

### Step 2: Add Rich CLI (1 day)

```python
# Install rich library
pip install rich

# Add to docforge.py
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm

console = Console()

# Beautiful progress bars
with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    console=console
) as progress:
    task = progress.add_task("Processing...", total=100)
    # Update with: progress.update(task, advance=10)

# Interactive prompts
preset = Prompt.ask(
    "Choose preset",
    choices=["auto", "book", "ocr", "transcribe"],
    default="auto"
)

# Confirmation
if Confirm.ask("Process 47 files?"):
    # Do it
```

### Step 3: Create Presets (1 day)

```python
# presets.py
PRESETS = {
    "book": {
        "model": "llama3.2:3b",
        "temperature": 0.3,
        "chunk_size": 8000,
        "detect_chapters": True,
        "preserve_references": True,
        "custom_prompt": "prompts/book.txt"
    },
    "ocr": {
        "model": "llama3.2:1b",
        "temperature": 0.2,
        "force_ocr": True,
        "handwriting_mode": True,
        "aggressive_cleanup": True,
        "custom_prompt": "prompts/ocr.txt"
    },
    "transcribe": {
        "model": "llama3.2:1b",
        "timestamps": True,
        "speaker_detection": True,
        "custom_prompt": "prompts/transcribe.txt"
    },
    "financial": {
        "model": "llama3.2:1b",
        "temperature": 0.1,
        "analyze": True,
        "math_formulas": True,
        "custom_prompt": "prompts/financial.txt"
    }
}

# Usage
docforge document.pdf --preset book
```

### Step 4: Config File Support (2 hours)

```yaml
# ~/.config/docforge/config.yaml
default_model: llama3.2:1b
default_output: ~/Documents/vault/inbox/
default_preset: auto
always_analyze_csv: true

presets:
  my-workflow:
    model: llama3.2:3b
    output_format: obsidian
    tags: ["to-review"]

ollama:
  host: localhost
  port: 11434
  timeout: 300

obsidian:
  vault_path: ~/Documents/vault/
  inbox_folder: inbox
  tags: ["docforge", "processed"]
```

```python
# Load config
import yaml
from pathlib import Path

def load_config():
    config_path = Path.home() / ".config" / "docforge" / "config.yaml"
    if config_path.exists():
        with open(config_path) as f:
            return yaml.safe_load(f)
    return {}

config = load_config()
default_model = config.get("default_model", "llama3.2:1b")
```

## Quick Wins (Can Do Today!)

### 1. iOS Shortcut (30 minutes)

Create iOS Shortcut that:
- Takes file as input
- Sends to Mac via HTTP
- Shows notification when done
- No coding required!

### 2. Alfred/Raycast Workflow (1 hour)

Quick Action for Mac:
- Select file in Finder
- Press hotkey
- docforge processes it
- Notification shows result

### 3. Hazel Automation (15 minutes)

Auto-process files in Downloads:
- Monitor ~/Downloads/
- When new .pdf appears
- Run: `docforge "$1" --output ~/vault/inbox/`
- Move original to "Processed" folder

## Platform Comparison

| Platform | Time to Build | Accessibility | Maintenance |
|----------|---------------|---------------|-------------|
| CLI | 1 week | Power users | Low |
| Web | 2 weeks | Universal (any device) | Medium |
| Desktop | 3 weeks | Non-technical users | Medium |
| iOS App | 6 weeks | iPhone/iPad users | High |

## Recommended Sequence

**For Personal Use:**
1. Enhanced CLI (Week 1)
2. Web Interface (Week 2)
3. iOS Shortcut (30 min)
4. Done! Use daily, gather feedback

**For Public Release:**
1. Enhanced CLI (Week 1)
2. Web Interface (Week 2)
3. Desktop GUI (Weeks 3-4)
4. iOS App (Weeks 5-10)
5. Marketing & documentation

**For Maximum Impact:**
1. Enhanced CLI (Week 1) ← Great for Reddit/HN
2. Open source release
3. Community feedback
4. Web Interface (Week 2-3)
5. Desktop GUI with community help
6. iOS app if there's demand

## Technology Stack Summary

| Component | Technology | Why |
|-----------|-----------|-----|
| CLI | Python + Rich | Already built, add beauty |
| Web Backend | FastAPI | Modern, async, fast |
| Web Frontend | HTML/Alpine.js | Simple, lightweight |
| Desktop | Tauri + Svelte | Small, fast, native |
| iOS | SwiftUI | Native, modern, powerful |
| Queue | Redis (optional) | Reliable job queue |
| Storage | Local FS or S3 | Simple or scalable |
| Auth | JWT or API keys | Secure, standard |

## Business Models (Optional)

**Free/Open Source:**
- CLI: Free forever
- Self-hosted web: Free
- Build community and reputation

**Freemium:**
- CLI: Free
- Web (local): Free
- Cloud hosting: $5-10/month
- iOS app: Free with limits or one-time purchase

**SaaS:**
- Free: 100 docs/month
- Pro: $10/month - Unlimited
- Team: $50/month - 5 users
- Enterprise: Custom pricing

## Success Metrics

**Phase 1 (CLI):**
- [ ] 100 GitHub stars
- [ ] 10 daily users (yourself + friends)
- [ ] 95%+ success rate on test files

**Phase 2 (Web):**
- [ ] Accessible from iPhone
- [ ] Process 100+ documents
- [ ] <2s average processing time

**Phase 3 (Desktop):**
- [ ] 1,000 downloads
- [ ] 4+ rating
- [ ] Active community

**Phase 4 (iOS):**
- [ ] App Store approval
- [ ] 10,000 downloads
- [ ] Featured by Apple (stretch goal)

## Resources Needed

**Time:**
- Solo: 3-4 months to Phase 4
- With help: 6-8 weeks to Phase 4

**Money:**
- Development: $0 (all free tools)
- Domain: $10-15/year
- iOS Developer: $99/year
- Server (optional): $5-20/month
- Total: ~$150/year maximum

**Skills:**
- Python (have it)
- FastAPI/Flask (easy to learn)
- HTML/CSS/JS (basic level fine)
- Tauri/Rust (moderate learning curve)
- Swift/SwiftUI (steep but rewarding)

## Decision Points

**Choose Your Path:**

**Path A: Personal Tool (Fastest)**
- Week 1: Enhanced CLI
- Week 2: Web interface
- Week 3: iOS Shortcut
- Result: Fully functional for you, ready to share

**Path B: Public Release (Most Impact)**
- Week 1: Enhanced CLI + docs
- Week 2: Open source launch
- Week 3-4: Community feedback + web interface
- Week 5-6: Desktop GUI
- Result: Popular open source project

**Path C: Commercial Product (Highest Effort)**
- Weeks 1-4: All platforms
- Weeks 5-8: Polish, testing, marketing
- Week 9+: Launch, support, iterate
- Result: Potential business

## My Recommendation

**Start with Path A, evolve to Path B:**

1. **This Week: Enhanced CLI**
   - Rename to docforge
   - Add rich progress bars
   - Create presets
   - Make it beautiful

2. **Next Week: Web Interface**
   - Simple FastAPI backend
   - Drag-and-drop UI
   - Works on your iPhone

3. **Week 3: Polish & Share**
   - Write great README
   - Record demo video
   - Share on Twitter/Reddit
   - Get feedback

4. **Week 4+: Based on Feedback**
   - If people love CLI → focus there
   - If people want GUI → build desktop
   - If people want mobile → build iOS
   - Let users guide the direction

## Next Action

**What do you want to tackle first?**

A. **Rename + Enhanced CLI** (most immediate value)
B. **Web interface** (works on iPhone today)
C. **iOS Shortcut** (0 coding, works in 30 min)
D. **Desktop GUI** (biggest UX improvement)
E. **All of the above** (comprehensive roadmap)

I'm excited to help you build this! The foundation is rock solid, now we just need to make it beautiful and accessible.

Which path sounds best to you?
