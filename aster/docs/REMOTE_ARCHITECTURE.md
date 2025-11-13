# Remote Processing Architecture for docforge

## Concept: Process Anywhere, Run Anywhere

**Vision:** Drop a file on your iPhone → Processed on your Mac at home → Result appears on your iPhone

## Architecture Options

### Option 1: Simple HTTP API (Recommended)

**Simplest and most practical approach.**

```
┌──────────────┐                    ┌──────────────┐
│   iPhone     │     WiFi/LTE       │  Mac/Server  │
│              │                    │  at Home     │
│  1. Upload   ├───────────────────►│  2. Process  │
│     file     │                    │     with     │
│              │                    │   docforge   │
│  4. Download │◄───────────────────┤  3. Store    │
│     result   │                    │     result   │
└──────────────┘                    └──────────────┘
```

**How it works:**
1. iPhone uploads file to Mac via REST API
2. Mac processes with docforge + Ollama
3. Mac stores result
4. iPhone downloads result (or gets push notification)

**Implementation:**

```python
# On Mac: docforge_server.py
from fastapi import FastAPI, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import subprocess
from pathlib import Path
import uuid
import json

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# Job storage
jobs = {}

@app.post("/api/process")
async def process_file(
    file: UploadFile,
    preset: str = "auto",
    model: str = "llama3.2:1b",
    background_tasks: BackgroundTasks = None
):
    job_id = str(uuid.uuid4())
    input_file = Path(f"uploads/{job_id}_{file.filename}")

    # Save file
    input_file.parent.mkdir(exist_ok=True)
    with open(input_file, "wb") as f:
        f.write(await file.read())

    # Create job
    jobs[job_id] = {
        "status": "queued",
        "filename": file.filename,
        "preset": preset,
        "progress": 0
    }

    # Queue processing
    background_tasks.add_task(
        run_docforge, job_id, input_file, preset, model
    )

    return {
        "job_id": job_id,
        "status": "queued",
        "check_url": f"/api/status/{job_id}"
    }

async def run_docforge(job_id: str, input_file: Path, preset: str, model: str):
    """Background task to run docforge"""
    output_file = Path(f"outputs/{job_id}.md")

    jobs[job_id]["status"] = "processing"

    try:
        # Run docforge
        process = subprocess.Popen(
            [
                "docforge",
                str(input_file),
                "-o", str(output_file),
                "--preset", preset,
                "--model", model
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Monitor progress (parse docforge output)
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break

            # Update progress based on output
            if "%" in line:
                # Parse percentage from output
                try:
                    progress = int(line.split("%")[0].split()[-1])
                    jobs[job_id]["progress"] = progress
                except:
                    pass

        # Check result
        if process.returncode == 0 and output_file.exists():
            jobs[job_id]["status"] = "complete"
            jobs[job_id]["output_file"] = str(output_file)
        else:
            jobs[job_id]["status"] = "failed"
            jobs[job_id]["error"] = process.stderr.read()

    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)

@app.get("/api/status/{job_id}")
async def get_status(job_id: str):
    """Check job status"""
    if job_id not in jobs:
        return {"error": "Job not found"}, 404

    return jobs[job_id]

@app.get("/api/download/{job_id}")
async def download_result(job_id: str):
    """Download processed file"""
    if job_id not in jobs or jobs[job_id]["status"] != "complete":
        return {"error": "File not ready"}, 404

    output_file = Path(jobs[job_id]["output_file"])
    return FileResponse(output_file, filename=output_file.name)

@app.get("/api/jobs")
async def list_jobs():
    """List all jobs"""
    return {"jobs": jobs}

# Start server
# uvicorn docforge_server:app --host 0.0.0.0 --port 8000
```

**Run on Mac:**
```bash
# Install dependencies
pip install fastapi uvicorn python-multipart

# Start server
uvicorn docforge_server:app --host 0.0.0.0 --port 8000

# Or run in background
nohup uvicorn docforge_server:app --host 0.0.0.0 --port 8000 &
```

**Access from iPhone:**
```javascript
// In iOS app or web interface
const API_URL = "http://192.168.1.100:8000";  // Your Mac's IP

async function processFile(file) {
    // 1. Upload file
    const formData = new FormData();
    formData.append('file', file);
    formData.append('preset', 'auto');

    const response = await fetch(`${API_URL}/api/process`, {
        method: 'POST',
        body: formData
    });

    const {job_id} = await response.json();

    // 2. Poll for status
    const status = await pollStatus(job_id);

    // 3. Download result
    if (status.status === 'complete') {
        const result = await fetch(`${API_URL}/api/download/${job_id}`);
        const markdown = await result.text();
        return markdown;
    }
}

async function pollStatus(job_id) {
    while (true) {
        const response = await fetch(`${API_URL}/api/status/${job_id}`);
        const status = await response.json();

        if (status.status === 'complete' || status.status === 'failed') {
            return status;
        }

        // Update UI with progress
        console.log(`Progress: ${status.progress}%`);

        await new Promise(resolve => setTimeout(resolve, 1000));
    }
}
```

### Option 2: Tailscale (Easy Remote Access)

**Problem:** Your Mac is at home, you're on cellular data. How to access it?

**Solution:** [Tailscale](https://tailscale.com) - creates secure VPN between devices

**Advantages:**
- Works from anywhere (not just home WiFi)
- Encrypted connection
- No port forwarding needed
- Free for personal use
- Works on iOS, Mac, Android, etc.

**Setup:**
```bash
# 1. Install on Mac
brew install tailscale
sudo tailscale up

# 2. Install on iPhone
# Download Tailscale app from App Store
# Login with same account

# 3. Access Mac from anywhere
# Mac gets stable IP like: 100.64.0.2
# Access: http://100.64.0.2:8000
```

Now your iPhone can reach your Mac from anywhere - coffee shop, office, traveling.

### Option 3: Push Notifications (Advanced)

**User Experience:**
1. Drop file on iPhone
2. File uploads to Mac
3. Lock iPhone and go about your day
4. Get notification when processing is done
5. Tap notification → opens result

**Implementation:**

```python
# On server, add push notification support
from apns2.client import APNsClient
from apns2.payload import Payload

def send_notification(device_token: str, job_id: str, filename: str):
    """Send push notification to iPhone"""
    client = APNsClient('path/to/cert.pem')

    payload = Payload(
        alert=f"✓ {filename} processed!",
        badge=1,
        sound="default",
        custom={
            "job_id": job_id,
            "action": "download"
        }
    )

    client.send_notification(device_token, payload, 'com.yourapp.docforge')

# Call after processing completes
async def run_docforge(...):
    # ... processing ...

    if success:
        # Send notification to all registered devices
        send_notification(user.device_token, job_id, filename)
```

**In iOS app:**
```swift
// Handle notification
func userNotificationCenter(
    _ center: UNUserNotificationCenter,
    didReceive response: UNNotificationResponse
) {
    if let jobId = response.notification.request.content.userInfo["job_id"] {
        // Download result
        downloadResult(jobId: jobId)
    }
}
```

### Option 4: Cloud Queue (Scale Up)

**For multiple users or heavy workloads:**

```
┌──────────────┐                    ┌──────────────┐
│   Client     │                    │  Cloud Queue │
│  (iPhone)    ├───────────────────►│   (Redis)    │
└──────────────┘                    └──────┬───────┘
                                           │
                     ┌─────────────────────┼──────────────┐
                     │                     │              │
                ┌────▼────┐          ┌────▼────┐    ┌────▼────┐
                │ Worker 1│          │ Worker 2│    │ Worker 3│
                │  (Mac)  │          │ (Linux) │    │ (Cloud) │
                └─────────┘          └─────────┘    └─────────┘
```

**Using Celery + Redis:**

```python
# celery_app.py
from celery import Celery
import subprocess

app = Celery('docforge', broker='redis://localhost:6379')

@app.task
def process_file(input_path: str, output_path: str, preset: str):
    """Celery task to process file"""
    result = subprocess.run([
        'docforge',
        input_path,
        '-o', output_path,
        '--preset', preset
    ], capture_output=True)

    return {
        'success': result.returncode == 0,
        'output': output_path if result.returncode == 0 else None,
        'error': result.stderr if result.returncode != 0 else None
    }

# Submit job from API
@app.post("/api/process")
async def submit_job(file: UploadFile):
    # Save file
    input_path = save_upload(file)

    # Submit to queue
    task = process_file.delay(input_path, output_path, preset)

    return {"task_id": task.id}
```

**Workers can be:**
- Your Mac at home
- Linux server
- Cloud VPS
- Multiple machines for parallel processing

### Option 5: SSH Tunnel (Developer Option)

**For technical users who want direct access:**

```bash
# On Mac (server)
# Enable SSH
sudo systemsetup -setremotelogin on

# On iPhone (using SSH client app like Termius)
ssh user@home-mac.local
docforge document.pdf

# Or tunnel the API
ssh -L 8000:localhost:8000 user@home-mac.local
# Now access http://localhost:8000 from iPhone
```

## Complete System Architecture

### Recommended Production Setup

```
┌─────────────────────────────────────────────────────────┐
│                      Clients                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ iPhone   │  │  iPad    │  │  Web     │             │
│  │  App     │  │  App     │  │ Browser  │             │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘             │
└───────┼─────────────┼─────────────┼───────────────────┘
        │             │             │
        └─────────────┴─────────────┘
                      │
        ┌─────────────▼──────────────┐
        │     API Gateway            │
        │   (FastAPI + nginx)        │
        └─────────────┬──────────────┘
                      │
        ┌─────────────▼──────────────┐
        │      Job Queue             │
        │       (Redis)              │
        └─────────────┬──────────────┘
                      │
        ┌─────────────┴──────────────┐
        │                            │
   ┌────▼─────┐              ┌──────▼──────┐
   │ Worker 1 │              │  Worker 2   │
   │  (Mac)   │              │  (Server)   │
   │          │              │             │
   │ docforge │              │  docforge   │
   │ + Ollama │              │  + Ollama   │
   └──────────┘              └─────────────┘
        │                            │
        └────────────┬───────────────┘
                     │
        ┌────────────▼──────────────┐
        │   Storage (S3/Local)      │
        │   - Uploads               │
        │   - Results               │
        └───────────────────────────┘
```

### Docker Compose Setup

**Easy deployment with Docker:**

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: ./api
    ports:
      - "8000:8000"
    environment:
      - REDIS_URL=redis://redis:6379
    volumes:
      - ./uploads:/app/uploads
      - ./outputs:/app/outputs
    depends_on:
      - redis

  worker:
    build: ./worker
    environment:
      - REDIS_URL=redis://redis:6379
      - OLLAMA_HOST=http://ollama:11434
    volumes:
      - ./uploads:/app/uploads
      - ./outputs:/app/outputs
    depends_on:
      - redis
      - ollama

  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ./ollama-data:/root/.ollama

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - api
```

**Run everything:**
```bash
docker-compose up -d
```

## Security Best Practices

### For Home Network Use

```python
# Simple API key authentication
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

API_KEY = "your-secret-key-here"
api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key

@app.post("/api/process")
async def process_file(
    file: UploadFile,
    api_key: str = Depends(verify_api_key)
):
    # Process file
    ...
```

**In iOS app:**
```swift
// Store API key securely
let apiKey = KeychainWrapper.standard.string(forKey: "api_key")

// Add to requests
var request = URLRequest(url: url)
request.addValue(apiKey, forHTTPHeaderField: "X-API-Key")
```

### For Public Access

```python
# Full authentication with users
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication

# User registration
# Login/logout
# JWT tokens
# Per-user file storage
# Rate limiting
```

## iOS Shortcuts Integration (Zero Coding!)

**You can do this TODAY without building an app:**

```
Shortcut: "docforge Document"

1. Get File from [Shortcut Input]
2. Set Variable [filename] to [Shortcut Input > Name]
3. Get Contents of URL
   - URL: http://your-mac-ip:8000/api/process
   - Method: POST
   - Request Body: Form
     - file: [File]
     - preset: auto
4. Get Dictionary Value [job_id] from [Contents of URL]
5. Repeat
   - Wait 2 seconds
   - Get Contents of URL
     - URL: http://your-mac-ip:8000/api/status/[job_id]
   - Get Dictionary Value [status] from [Contents of URL]
   - If [status] is "complete"
     - Stop Repeat
6. Get Contents of URL
   - URL: http://your-mac-ip:8000/api/download/[job_id]
7. Save File [Contents of URL] to iCloud Drive
8. Show Notification: "✓ Processed [filename]"
```

**Use it:**
- Select file in Files app
- Share → Run Shortcut → docforge Document
- Done!

## Comparison of Approaches

| Approach | Complexity | Remote Access | Cost | Best For |
|----------|-----------|---------------|------|----------|
| HTTP API (local) | Low | Home WiFi only | Free | Starting out |
| Tailscale | Low | Anywhere | Free | Personal use |
| Cloud Queue | Medium | Anywhere | Server costs | Multi-user |
| Docker Setup | Medium | Anywhere | VPS costs | Production |
| iOS Shortcut | Very Low | Home WiFi | Free | Quick solution |

## Recommended Path

**Week 1: Local API**
```bash
# Start simple
uvicorn docforge_server:app --host 0.0.0.0 --port 8000

# Test from iPhone on same WiFi
curl -F "file=@document.pdf" http://192.168.1.100:8000/api/process
```

**Week 2: Add Tailscale**
```bash
# Install Tailscale
brew install tailscale
tailscale up

# Now works from anywhere!
```

**Week 3: iOS Shortcuts**
- Build Shortcut to call API
- Test with different file types
- Share with friends/family

**Week 4: Simple Web UI**
- Add drag-and-drop interface
- Pretty progress bars
- Works in Safari on iPhone

**Month 2: iOS App** (optional)
- Native Swift app
- Camera integration
- Share extension
- Push notifications

## Crazy Ideas (But Possible!)

### 1. Telegram Bot
```python
# Process files via Telegram
# Send document → Bot processes → Returns markdown
# Works from any device with Telegram
```

### 2. Email Processing
```python
# Email document to process@yourdomain.com
# Receive markdown reply
# Works from any email client
```

### 3. Watch Folder Sync
```python
# Use Dropbox/iCloud
# Drop file in "docforge-inbox" folder on iPhone
# Mac watches folder, processes automatically
# Result appears in "docforge-output" folder
```

### 4. Voice Commands
```
"Hey Siri, process my meeting notes"
→ Runs Shortcut
→ Finds today's meeting notes
→ Sends to docforge
→ Saves to Obsidian vault
```

## Next Steps?

Want me to build:
1. **The simple API server** (1-2 hours) - Works immediately on home WiFi
2. **iOS Shortcut** (30 min) - Use right away without coding
3. **Web interface** (1 day) - Pretty UI that works on iPhone
4. **Full iOS app** (1-2 weeks) - Native experience

The fastest win is #1 + #2 - you could be processing documents from your iPhone tonight!
