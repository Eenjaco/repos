# GUI Options for docforge

## Overview

Three approaches for making docforge accessible to non-technical users:

1. **Desktop GUI** (Mac/Windows/Linux) - Native app
2. **Web Interface** (Local or hosted) - Browser-based
3. **Mobile App** (iPhone/iPad) - With remote processing

## Option 1: Desktop GUI (Recommended Starting Point)

### Technology: Electron or Tauri

**Tauri** (Recommended):
- Rust backend + Web frontend
- Much smaller than Electron (~3MB vs 150MB)
- Better performance and security
- Native feel

**Stack:**
- Backend: Python (existing code) + Tauri Rust wrapper
- Frontend: HTML/CSS/JavaScript (or React/Vue/Svelte)

### UI Mockup

```
┌─────────────────────────────────────────────────────────┐
│  docforge                                    ⚙️  📊  ❓   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│        Drop files here or click to browse               │
│               📁 Choose Files                           │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │  📄 annual-report.pdf        (2.3 MB)    ✓    │    │
│  │  📷 meeting-notes.jpg        (854 KB)    ✓    │    │
│  │  🎵 lecture.mp3              (45 MB)     ⏳    │    │
│  │  📊 expenses.csv             (23 KB)     ⏳    │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  Processing: lecture.mp3                                │
│  ████████████░░░░░░░░ 60% (4m 32s remaining)           │
│                                                          │
│  ┌──────────────┬──────────────┬──────────────┐        │
│  │ Preset:      │ Model:       │ Output:      │        │
│  │ [Auto    ▼] │ [llama3.2:1b▼]│ [Same Folder▼]│       │
│  └──────────────┴──────────────┴──────────────┘        │
│                                                          │
│              [Process All]  [Cancel]                    │
└─────────────────────────────────────────────────────────┘
```

### Features

**Main Window:**
- Drag & drop file upload
- Live processing queue
- Progress bars with time estimates
- Quick preset selection
- Output folder selection

**Settings Panel (⚙️):**
```
┌─────────────────────────────────────────┐
│  Settings                               │
├─────────────────────────────────────────┤
│                                          │
│  General                                 │
│    Default output folder: [Browse...]   │
│    [x] Auto-process dropped files       │
│    [x] Show notifications               │
│    [x] Keep original files              │
│                                          │
│  AI/Ollama                              │
│    Default model: [llama3.2:1b ▼]       │
│    Temperature: [0.2] ───────○──        │
│    [x] Enable AI cleaning               │
│                                          │
│  Presets                                 │
│    [Edit Presets...]                    │
│                                          │
│  System                                  │
│    [Check Dependencies]                 │
│    [View Logs]                          │
│                                          │
│              [Save]  [Cancel]           │
└─────────────────────────────────────────┘
```

**Statistics Panel (📊):**
```
┌─────────────────────────────────────────┐
│  Statistics                              │
├─────────────────────────────────────────┤
│                                          │
│  Documents processed: 1,247              │
│  Total size: 8.2 GB                     │
│  Success rate: 97.3%                    │
│  Average time: 8.2s per file            │
│                                          │
│  By Type:                               │
│    PDF      █████████░ 623 (50%)       │
│    DOCX     ████░░░░░░ 234 (19%)       │
│    Images   ███░░░░░░░ 198 (16%)       │
│    Audio    ██░░░░░░░░ 112 (9%)        │
│    Other    █░░░░░░░░░ 80 (6%)         │
│                                          │
│  Recent Activity (Last 7 days)          │
│    Mon ████░░ 23 files                  │
│    Tue ██████ 34 files                  │
│    Wed ███░░░ 18 files                  │
│                                          │
└─────────────────────────────────────────┘
```

### Implementation Complexity

**Easy (Weekend project):**
- Basic drag-and-drop
- File queue
- Single file processing
- Progress bars

**Medium (1-2 weeks):**
- Batch processing
- Settings management
- Preset system
- Statistics

**Advanced (3-4 weeks):**
- Watch folders
- Real-time notifications
- Advanced error handling
- Custom themes

### Tech Stack Example (Tauri)

```bash
# Setup
npm create tauri-app
cd docforge-app

# Structure
docforge-app/
├── src-tauri/          # Rust backend
│   ├── src/
│   │   └── main.rs     # Calls Python docforge
│   └── Cargo.toml
├── src/                # Frontend
│   ├── index.html
│   ├── styles.css
│   └── app.js
└── package.json
```

**Calling Python from Rust:**
```rust
// src-tauri/src/main.rs
#[tauri::command]
fn process_file(path: String, preset: String) -> Result<String, String> {
    let output = Command::new("docforge")
        .arg(&path)
        .arg("--preset")
        .arg(&preset)
        .output()
        .map_err(|e| e.to_string())?;

    Ok(String::from_utf8_lossy(&output.stdout).to_string())
}
```

**Frontend calls:**
```javascript
// src/app.js
import { invoke } from '@tauri-apps/api/tauri'

async function processFile(filePath, preset) {
    try {
        const result = await invoke('process_file', {
            path: filePath,
            preset: preset
        });
        console.log('Success:', result);
    } catch (error) {
        console.error('Error:', error);
    }
}
```

## Option 2: Web Interface (Most Accessible)

### Technology: Flask/FastAPI + HTML/CSS/JS

**Advantages:**
- Works on any device with browser
- No installation needed
- Easy to update
- Can be local or cloud-hosted

### Architecture

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Browser   │◄───────►│ Web Server  │◄───────►│  docforge   │
│ (Frontend)  │         │ (Flask)     │         │  (Python)   │
└─────────────┘         └─────────────┘         └─────────────┘
     │                        │                        │
     │                        ▼                        ▼
     │                  ┌──────────┐             ┌──────────┐
     │                  │ Queue    │             │ Ollama   │
     └─────────────────►│ (Redis)  │             │          │
                        └──────────┘             └──────────┘
```

### UI Mockup (Web)

**Homepage:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>docforge - Document Processing</title>
</head>
<body>
    <div class="container">
        <h1>🔨 docforge</h1>
        <p>Transform any document into structured knowledge</p>

        <div class="upload-zone" id="dropZone">
            <svg>📁</svg>
            <p>Drop files here or click to browse</p>
            <input type="file" id="fileInput" multiple hidden>
        </div>

        <div class="options">
            <select id="preset">
                <option value="auto">Auto-detect</option>
                <option value="book">Book</option>
                <option value="ocr">OCR</option>
                <option value="transcribe">Transcribe</option>
                <option value="financial">Financial</option>
            </select>

            <select id="model">
                <option value="llama3.2:1b">llama3.2:1b (Fast)</option>
                <option value="llama3.2:3b">llama3.2:3b (Better)</option>
            </select>
        </div>

        <div id="queue"></div>

        <button id="processBtn">Process All</button>
    </div>

    <script src="app.js"></script>
</body>
</html>
```

### Backend (Flask)

```python
# app.py
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import subprocess
import uuid
from pathlib import Path

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = Path("uploads")
OUTPUT_FOLDER = Path("outputs")

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    file = request.files['file']
    file_id = str(uuid.uuid4())
    file_path = UPLOAD_FOLDER / f"{file_id}_{file.filename}"
    file.save(file_path)

    return jsonify({
        'file_id': file_id,
        'filename': file.filename,
        'status': 'uploaded'
    })

@app.route('/api/process', methods=['POST'])
def process_file():
    """Process file with docforge"""
    data = request.json
    file_id = data['file_id']
    preset = data.get('preset', 'auto')

    # Find uploaded file
    files = list(UPLOAD_FOLDER.glob(f"{file_id}_*"))
    if not files:
        return jsonify({'error': 'File not found'}), 404

    input_file = files[0]
    output_file = OUTPUT_FOLDER / f"{input_file.stem}.md"

    # Run docforge
    result = subprocess.run([
        'docforge',
        str(input_file),
        '--output', str(output_file),
        '--preset', preset
    ], capture_output=True, text=True)

    if result.returncode == 0:
        return jsonify({
            'status': 'success',
            'file_id': file_id,
            'output_url': f'/api/download/{file_id}'
        })
    else:
        return jsonify({
            'status': 'error',
            'error': result.stderr
        }), 500

@app.route('/api/download/<file_id>')
def download_file(file_id):
    """Download processed file"""
    files = list(OUTPUT_FOLDER.glob(f"{file_id}_*"))
    if files:
        return send_file(files[0], as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

@app.route('/api/status/<file_id>')
def get_status(file_id):
    """Get processing status"""
    # Check queue/database for status
    return jsonify({
        'file_id': file_id,
        'status': 'processing',
        'progress': 45,
        'eta_seconds': 120
    })

if __name__ == '__main__':
    UPLOAD_FOLDER.mkdir(exist_ok=True)
    OUTPUT_FOLDER.mkdir(exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### Deployment Options

**1. Local Only (No internet needed):**
```bash
# Run on localhost
python app.py
# Open: http://localhost:5000
```

**2. Home Network (Access from any device):**
```bash
# Mac/Server runs docforge backend
python app.py --host 0.0.0.0
# Access from iPhone: http://192.168.1.100:5000
```

**3. Cloud Hosted (Public or private):**
```bash
# Deploy to:
# - Heroku (easy)
# - DigitalOcean App Platform
# - Fly.io
# - Your own VPS

# With authentication and secure uploads
```

## Option 3: Mobile App (iPhone) with Remote Processing

### Architecture: Remote Execution

```
┌──────────────┐                    ┌──────────────┐
│   iPhone     │                    │  Mac/Server  │
│              │                    │              │
│  ┌────────┐  │    Upload file     │  ┌────────┐  │
│  │docforge│  ├───────────────────►│  │docforge│  │
│  │  App   │  │                    │  │ Service│  │
│  └────────┘  │◄───────────────────┤  └────────┘  │
│              │  Download result   │              │
└──────────────┘                    └──────────────┘
       │                                   │
       │                                   ▼
       │                              ┌──────────┐
       └─────────────────────────────►│  Ollama  │
            (via REST API)             └──────────┘
```

### Technology Options

**Option A: Native iOS (Swift + SwiftUI)**
- Best performance and UX
- Access to iOS features (Share Sheet, Files app)
- Apple ecosystem integration

**Option B: React Native (JavaScript)**
- Cross-platform (iOS + Android)
- Faster development
- Web devs can contribute

**Option C: Progressive Web App (PWA)**
- No App Store needed
- Works in Safari
- Limited iOS features

### iOS App UI Mockup

**Main Screen:**
```
╔═══════════════════════════════════════╗
║  ☰  docforge              🔨  ⚙️      ║
╠═══════════════════════════════════════╣
║                                        ║
║       📱 Tap to select files          ║
║          or                           ║
║       📷 Take a photo                 ║
║          or                           ║
║       📋 Paste from clipboard         ║
║                                        ║
║  ┌──────────────────────────────────┐ ║
║  │  Recent                          │ ║
║  │                                  │ ║
║  │  📄 Meeting notes    Oct 12  ✓  │ ║
║  │  📷 Whiteboard       Oct 11  ✓  │ ║
║  │  🎵 Lecture audio    Oct 10  ✓  │ ║
║  └──────────────────────────────────┘ ║
║                                        ║
║  [📤 Share]  [📂 Browse Files]        ║
╚═══════════════════════════════════════╝
```

**Processing Screen:**
```
╔═══════════════════════════════════════╗
║  ← Back                               ║
╠═══════════════════════════════════════╣
║                                        ║
║     📄 Meeting-notes.jpg              ║
║        2.3 MB                         ║
║                                        ║
║     Processing with OCR...            ║
║     ████████████░░░░░░░ 65%          ║
║                                        ║
║     Estimated: 23 seconds remaining   ║
║                                        ║
║     Status:                           ║
║     ✓ Uploaded to server              ║
║     ⏳ Extracting text with OCR       ║
║     ⏳ Cleaning with AI...            ║
║     ○ Formatting                      ║
║                                        ║
║          [Cancel Processing]          ║
╚═══════════════════════════════════════╝
```

**Result Screen:**
```
╔═══════════════════════════════════════╗
║  ← Back              ⋮                ║
╠═══════════════════════════════════════╣
║  ✓ Processing Complete!               ║
║                                        ║
║  📄 Meeting-notes.md                  ║
║     Created: Oct 12, 2025 10:34 AM   ║
║     Size: 4.2 KB                      ║
║                                        ║
║  Preview:                             ║
║  ┌──────────────────────────────────┐ ║
║  │ # Meeting Notes                  │ ║
║  │                                  │ ║
║  │ **Date:** October 12, 2025      │ ║
║  │                                  │ ║
║  │ ## Action Items                 │ ║
║  │ - Follow up with client...      │ ║
║  └──────────────────────────────────┘ ║
║                                        ║
║  [📤 Share]  [💾 Save to Files]      ║
║  [📋 Copy]   [✉️ Email]               ║
╚═══════════════════════════════════════╝
```

### iOS Features

**Share Extension:**
- Process files directly from Files app
- Share from other apps (Photos, Safari, etc.)
- "Share to docforge" option

**Shortcuts Integration:**
```
Shortcut: "Process Document"
- Get file from input
- Send to docforge API
- Save result to Obsidian folder
- Show notification when done
```

**Camera Integration:**
- Take photo → auto-process with OCR
- Document scanner mode
- Batch photo processing

**Background Processing:**
- Upload → lock phone → notification when done
- Works even when app is closed

### Backend Requirements

The Mac/server needs to run:

```python
# docforge_server.py
from fastapi import FastAPI, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse
import subprocess
from pathlib import Path
import uuid

app = FastAPI()

@app.post("/api/v1/process")
async def process_document(
    file: UploadFile,
    preset: str = "auto",
    background_tasks: BackgroundTasks
):
    """Process uploaded file"""
    file_id = str(uuid.uuid4())
    input_path = Path(f"uploads/{file_id}_{file.filename}")

    # Save upload
    with open(input_path, "wb") as f:
        f.write(await file.read())

    # Queue processing
    background_tasks.add_task(process_file, file_id, input_path, preset)

    return {
        "file_id": file_id,
        "status": "queued",
        "check_url": f"/api/v1/status/{file_id}"
    }

def process_file(file_id: str, input_path: Path, preset: str):
    """Background task to process file"""
    output_path = Path(f"outputs/{file_id}.md")

    subprocess.run([
        "docforge",
        str(input_path),
        "-o", str(output_path),
        "--preset", preset
    ])

    # Update database/cache with status

@app.get("/api/v1/status/{file_id}")
async def get_status(file_id: str):
    """Get processing status"""
    # Check status in database
    return {
        "file_id": file_id,
        "status": "complete",
        "download_url": f"/api/v1/download/{file_id}"
    }

@app.get("/api/v1/download/{file_id}")
async def download(file_id: str):
    """Download processed file"""
    file_path = Path(f"outputs/{file_id}.md")
    return FileResponse(file_path, filename=f"{file_id}.md")
```

**Run server:**
```bash
# On Mac/Server
uvicorn docforge_server:app --host 0.0.0.0 --port 8000

# Access from iPhone on same network:
# http://192.168.1.100:8000
```

### Security Considerations

**For home network use:**
```python
# Add basic authentication
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

@app.post("/api/v1/process")
async def process_document(
    credentials: HTTPBasicCredentials = Depends(security),
    ...
):
    # Verify credentials
    if credentials.username != "user" or credentials.password != "pass":
        raise HTTPException(401)
    ...
```

**For cloud hosting:**
- Use HTTPS (Let's Encrypt)
- API key authentication
- Rate limiting
- File size limits
- Virus scanning for uploads

## Comparison Matrix

| Feature | Desktop GUI | Web Interface | Mobile App |
|---------|------------|---------------|------------|
| **Ease of Development** | Medium | Easy | Hard |
| **Installation** | Required | None | App Store |
| **Cross-platform** | Mac/Win/Linux | Any browser | iOS/Android |
| **Offline Mode** | ✓ Yes | ✗ No | ✗ No (needs server) |
| **Performance** | Excellent | Good | Depends on connection |
| **File Access** | Full | Upload only | Limited (share sheet) |
| **Native Feel** | ✓ Yes | Partial | ✓ Yes |
| **Auto-update** | Manual | Automatic | App Store |
| **Cost** | Free | Hosting costs | Developer account ($99/yr) |
| **Time to MVP** | 2-3 weeks | 1 week | 4-6 weeks |

## Recommended Approach

### Phase 1: Enhanced CLI (Week 1)
- Implement beautiful CLI with progress bars
- Add interactive mode
- Create preset system
- **Result:** Fully functional for power users

### Phase 2: Web Interface (Weeks 2-3)
- Build simple Flask/FastAPI backend
- Create drag-and-drop web UI
- Add queue system
- **Result:** Accessible from any device on home network

### Phase 3: Desktop GUI (Weeks 4-6)
- Build Tauri app
- Wrap existing CLI
- Add system tray integration
- **Result:** Native app for non-technical users

### Phase 4: Mobile App (Months 2-3)
- iOS app with Swift
- Camera integration
- Share extension
- **Result:** Process documents from phone

## Quick Wins

**Easiest to implement now:**

1. **Web interface** (1-2 days):
   - Simple Flask app
   - Drag-and-drop upload
   - Shows progress
   - Download result

2. **iOS Shortcut** (30 minutes):
   - No app development needed
   - Uses Shortcuts app
   - Sends file to web interface via API
   - Shows notification when done

3. **Alfred/Raycast workflow** (1 hour):
   - Select file in Finder
   - Hotkey triggers docforge
   - Shows notification with result

## Next Steps

Want me to:
1. Build the web interface first? (Fastest path to GUI)
2. Create the enhanced CLI with beautiful UX?
3. Design a full Tauri desktop app?
4. Set up the iOS app architecture?

The web interface would give you a GUI that works everywhere (Mac, iPhone, iPad) in just a few hours of work!
