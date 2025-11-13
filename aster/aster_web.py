#!/usr/bin/env python3
"""
Aster Web Server - Process documents from anywhere

Run this on your Mac to access Aster from your iPhone, iPad, or browser.

Usage:
    python3 aster_web.py
    # Access from iPhone: http://your-mac-ip:8888

Features:
- Drag & drop file upload
- Real-time processing progress
- Download processed files
- Works on home WiFi or with Tailscale
"""

from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import asyncio
from pathlib import Path
import uuid
import json
from datetime import datetime
from typing import Optional, Dict
import shutil
import socket
import qrcode

# Configuration
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Job tracking
jobs: Dict[str, dict] = {}

# FastAPI app
app = FastAPI(title="Aster", description="Navigate your constellation of knowledge")

# Enable CORS for iPhone access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# Web Interface HTML
# =============================================================================

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASTER - 8-Bit Document Processing</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            image-rendering: pixelated;
            image-rendering: -moz-crisp-edges;
            image-rendering: crisp-edges;
        }

        body {
            font-family: 'Press Start 2P', 'Courier New', monospace;
            background: #000000;
            color: #f5f5f5;
            min-height: 100vh;
            padding: 20px;
            font-size: 12px;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
        }

        header {
            display: flex;
            align-items: center;
            gap: 20px;
            margin-bottom: 30px;
            padding: 20px 0;
        }

        .logo {
            font-size: 48px;
            line-height: 1;
        }

        .header-text {
            flex: 1;
            text-align: center;
        }

        h1 {
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #ffffff;
            letter-spacing: 2px;
        }

        .tagline {
            font-size: 10px;
            color: #888888;
            font-style: italic;
            line-height: 1.6;
        }

        .stats {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
            justify-content: center;
        }

        .stat {
            background: #2a3f5f;
            width: 150px;
            height: 75px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            border: 3px solid #1a2f4f;
            box-shadow: inset 0 0 0 1px #3a5f7f;
        }

        .stat-value {
            font-size: 36px;
            color: #ffffff;
            line-height: 1;
            margin-bottom: 5px;
        }

        .stat-label {
            font-size: 8px;
            color: #aaaaaa;
            text-transform: lowercase;
        }

        .upload-zone {
            background: #2a3f5f;
            border: 3px solid #1a2f4f;
            padding: 40px 20px;
            text-align: center;
            cursor: pointer;
            margin-bottom: 20px;
            box-shadow: inset 0 0 0 1px #3a5f7f;
        }

        .upload-zone:hover {
            background: #3a4f6f;
            border-color: #2a4f6f;
        }

        .upload-text {
            font-size: 10px;
            color: #cccccc;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        input[type="file"] {
            display: none;
        }

        .options {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
            justify-content: center;
        }

        select, button {
            font-family: 'Press Start 2P', 'Courier New', monospace;
            font-size: 10px;
            padding: 10px 15px;
            background: #2a3f5f;
            border: 3px solid #1a2f4f;
            color: #ffffff;
            cursor: pointer;
            text-transform: lowercase;
        }

        select {
            width: 200px;
        }

        select:hover, button:hover {
            background: #3a4f6f;
            border-color: #2a4f6f;
        }

        button {
            width: 150px;
            height: 40px;
        }

        button:active {
            background: #1a2f4f;
        }

        button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }

        .job {
            background: #2a3f5f;
            border: 3px solid #1a2f4f;
            padding: 15px;
            margin-bottom: 10px;
            box-shadow: inset 0 0 0 1px #3a5f7f;
        }

        .job.processing {
            border-left: 5px solid #ffaa00;
        }

        .job.complete {
            border-left: 5px solid #00ff00;
        }

        .job.failed {
            border-left: 5px solid #ff0000;
        }

        .job-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            font-size: 10px;
        }

        .job-name {
            color: #ffffff;
        }

        .job-status {
            color: #aaaaaa;
        }

        .progress-bar {
            height: 12px;
            background: #1a2f4f;
            border: 2px solid #0a1f3f;
            margin: 10px 0;
        }

        .progress-fill {
            height: 100%;
            background: repeating-linear-gradient(
                90deg,
                #ffaa00,
                #ffaa00 4px,
                #ff8800 4px,
                #ff8800 8px
            );
            transition: width 0.3s;
        }

        .job-actions {
            margin-top: 15px;
            display: flex;
            gap: 10px;
        }

        .empty-state {
            text-align: center;
            padding: 40px;
            color: #555555;
            font-size: 10px;
        }

        .feedback {
            background: #1a2f4f;
            border: 2px solid #0a1f3f;
            padding: 15px;
            margin-top: 20px;
            min-height: 100px;
            font-size: 9px;
            color: #00ff00;
            font-family: 'Courier New', monospace;
            overflow-y: auto;
            max-height: 200px;
        }

        .feedback-line {
            margin-bottom: 5px;
        }

        @media (max-width: 600px) {
            h1 {
                font-size: 20px;
            }

            .stats {
                flex-direction: column;
                align-items: center;
            }

            .options {
                flex-direction: column;
                align-items: center;
            }

            select {
                width: 100%;
                max-width: 300px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo">✦</div>
            <div class="header-text">
                <h1>ASTER</h1>
                <p class="tagline">Navigate your<br>constellation of knowledge</p>
            </div>
            <div class="logo">✦</div>
        </header>

        <div class="stats">
            <div class="stat">
                <div class="stat-value" id="totalJobs">0</div>
                <div class="stat-label">processed</div>
            </div>
            <div class="stat">
                <div class="stat-value" id="queueSize">0</div>
                <div class="stat-label">in queue</div>
            </div>
            <div class="stat">
                <div class="stat-value" id="successRate">--</div>
                <div class="stat-label">success rate</div>
            </div>
        </div>

        <div class="upload-zone" id="dropZone">
            <div class="upload-text">▼ drop files here ▼</div>
            <input type="file" id="fileInput" multiple accept=".pdf,.docx,.pptx,.jpg,.jpeg,.png,.html,.txt,.md,.csv,.xlsx,.epub,.mp3,.wav,.m4a,.wma">
        </div>

        <div class="options">
            <select id="model">
                <option value="llama3.2:1b">llama 3.2: 1B (fast)</option>
                <option value="llama3.2:3b">llama 3.2: 3B (faster)</option>
                <option value="qwen2.5:0.5b">qwen 2.5: 0.5B (fastest)</option>
            </select>
        </div>

        <div id="jobs"></div>

        <div class="empty-state" id="emptyState">
            <p>▶ NO DOCUMENTS PROCESSED YET ◀</p>
            <p style="margin-top: 10px;">DROP A FILE TO START</p>
        </div>

        <div class="feedback" id="feedback">
            <div class="feedback-line">> ASTER v1.0 INITIALIZED</div>
            <div class="feedback-line">> READY TO PROCESS DOCUMENTS</div>
        </div>
    </div>

    <script>
        const dropZone = document.getElementById('dropZone');
        const fileInput = document.getElementById('fileInput');
        const jobsContainer = document.getElementById('jobs');
        const emptyState = document.getElementById('emptyState');
        const feedbackEl = document.getElementById('feedback');

        let jobs = {};
        let stats = { total: 0, success: 0, queue: 0 };

        function addFeedback(message) {
            const line = document.createElement('div');
            line.className = 'feedback-line';
            line.textContent = '> ' + message;
            feedbackEl.appendChild(line);
            feedbackEl.scrollTop = feedbackEl.scrollHeight;

            // Keep only last 20 lines
            while (feedbackEl.children.length > 20) {
                feedbackEl.removeChild(feedbackEl.firstChild);
            }
        }

        // Drag and drop
        dropZone.addEventListener('click', () => fileInput.click());

        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('dragover');
        });

        dropZone.addEventListener('dragleave', () => {
            dropZone.classList.remove('dragover');
        });

        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('dragover');
            handleFiles(e.dataTransfer.files);
        });

        fileInput.addEventListener('change', (e) => {
            handleFiles(e.target.files);
        });

        async function handleFiles(files) {
            for (const file of files) {
                await uploadFile(file);
            }
        }

        async function uploadFile(file) {
            const model = document.getElementById('model').value;
            addFeedback(`UPLOADING: ${file.name}`);

            const formData = new FormData();
            formData.append('file', file);
            formData.append('preset', 'auto');
            formData.append('model', model);

            try {
                const response = await fetch('/api/process', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (response.ok) {
                    addFeedback(`JOB CREATED: ${data.job_id}`);
                    addJob(data.job_id, file.name, model);
                    pollJob(data.job_id);
                } else {
                    addFeedback(`ERROR: ${data.error}`);
                    alert('Upload failed: ' + data.error);
                }
            } catch (error) {
                addFeedback(`ERROR: ${error.message}`);
                alert('Upload failed: ' + error.message);
            }
        }

        function addJob(jobId, filename, model) {
            emptyState.style.display = 'none';

            const jobEl = document.createElement('div');
            jobEl.className = 'job processing';
            jobEl.id = 'job-' + jobId;
            jobEl.innerHTML = `
                <div class="job-header">
                    <div class="job-name">${filename}</div>
                    <div class="job-status">PROCESSING...</div>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: 10%"></div>
                </div>
                <div style="font-size: 8px; color: #888888; margin-top: 10px;">
                    model: ${model}
                </div>
            `;

            jobsContainer.prepend(jobEl);
            jobs[jobId] = { filename, model, el: jobEl };

            stats.queue++;
            updateStats();
        }

        async function pollJob(jobId) {
            const interval = setInterval(async () => {
                try {
                    const response = await fetch(`/api/status/${jobId}`);
                    const data = await response.json();

                    updateJob(jobId, data);

                    if (data.status === 'complete' || data.status === 'failed') {
                        clearInterval(interval);

                        if (data.status === 'complete') {
                            stats.success++;
                            stats.queue--;
                            addFeedback(`COMPLETE: ${jobs[jobId].filename}`);
                        } else {
                            stats.queue--;
                            addFeedback(`FAILED: ${jobs[jobId].filename}`);
                        }
                        stats.total++;
                        updateStats();
                    }
                } catch (error) {
                    console.error('Poll error:', error);
                }
            }, 1000);
        }

        function updateJob(jobId, data) {
            const job = jobs[jobId];
            if (!job) return;

            const el = job.el;

            if (data.status === 'complete') {
                el.className = 'job complete';
                el.querySelector('.job-status').textContent = '✓ COMPLETE';
                el.querySelector('.progress-fill').style.width = '100%';

                const actions = document.createElement('div');
                actions.className = 'job-actions';
                actions.innerHTML = `
                    <button onclick="downloadFile('${jobId}')">download</button>
                    <button onclick="viewFile('${jobId}')">view</button>
                `;
                el.appendChild(actions);
            } else if (data.status === 'failed') {
                el.className = 'job failed';
                el.querySelector('.job-status').textContent = '✗ FAILED';
                el.innerHTML += `<div style="color: #ff0000; margin-top: 10px; font-size: 9px;">${data.error || 'UNKNOWN ERROR'}</div>`;
            } else {
                const progress = data.progress || 50;
                el.querySelector('.progress-fill').style.width = progress + '%';
                el.querySelector('.job-status').textContent = progress + '%';
            }
        }

        function updateStats() {
            document.getElementById('totalJobs').textContent = stats.total;
            document.getElementById('queueSize').textContent = stats.queue;

            const rate = stats.total > 0 ? Math.round((stats.success / stats.total) * 100) + '%' : '--';
            document.getElementById('successRate').textContent = rate;
        }

        async function downloadFile(jobId) {
            window.location.href = `/api/download/${jobId}`;
        }

        async function viewFile(jobId) {
            const response = await fetch(`/api/download/${jobId}`);
            const text = await response.text();

            const modal = document.createElement('div');
            modal.style.cssText = 'position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.9); padding: 20px; overflow: auto; z-index: 1000;';
            modal.innerHTML = `
                <div style="max-width: 800px; margin: 0 auto; background: #1e3a5f; padding: 30px; border-radius: 12px; position: relative;">
                    <button onclick="this.parentElement.parentElement.remove()" style="position: absolute; top: 10px; right: 10px;">Close</button>
                    <pre style="white-space: pre-wrap; word-wrap: break-word; color: #e0e6ed;">${text}</pre>
                </div>
            `;
            document.body.appendChild(modal);
        }

        // Load existing jobs on page load
        async function loadJobs() {
            try {
                const response = await fetch('/api/jobs');
                const data = await response.json();

                Object.entries(data.jobs || {}).forEach(([jobId, job]) => {
                    if (job.status !== 'complete' && job.status !== 'failed') {
                        addJob(jobId, job.filename, job.preset || 'auto');
                        pollJob(jobId);
                    }
                });
            } catch (error) {
                console.error('Failed to load jobs:', error);
            }
        }

        loadJobs();
    </script>
</body>
</html>
"""

# =============================================================================
# API Endpoints
# =============================================================================

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the web interface"""
    return HTML_PAGE

@app.post("/api/process")
async def process_file(
    file: UploadFile = File(...),
    preset: str = "auto",
    model: str = "llama3.2:1b",
    background_tasks: BackgroundTasks = None
):
    """Upload and process a file"""

    # Generate job ID
    job_id = str(uuid.uuid4())[:8]

    # Save uploaded file
    input_path = UPLOAD_DIR / f"{job_id}_{file.filename}"
    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Create job
    jobs[job_id] = {
        "job_id": job_id,
        "filename": file.filename,
        "input_path": str(input_path),
        "preset": preset,
        "model": model,
        "status": "queued",
        "progress": 0,
        "created_at": datetime.now().isoformat()
    }

    # Queue processing
    background_tasks.add_task(process_job, job_id)

    return {
        "job_id": job_id,
        "status": "queued",
        "check_url": f"/api/status/{job_id}"
    }

async def process_job(job_id: str):
    """Background task to process file"""
    job = jobs[job_id]
    job["status"] = "processing"
    job["progress"] = 10

    input_path = Path(job["input_path"])
    output_path = OUTPUT_DIR / f"{job_id}.md"

    try:
        # Build command
        cmd = [
            "python3",
            "aster.py",
            str(input_path),
            "-o", str(output_path),
            "--model", job["model"]
        ]

        if job["preset"] != "auto":
            cmd.extend(["--preset", job["preset"]])

        # Run aster
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Monitor progress
        job["progress"] = 50

        # Wait for completion
        stdout, stderr = process.communicate(timeout=300)

        job["progress"] = 90

        # Check result
        if process.returncode == 0 and output_path.exists():
            job["status"] = "complete"
            job["output_path"] = str(output_path)
            job["output_size"] = output_path.stat().st_size
            job["progress"] = 100
        else:
            job["status"] = "failed"
            job["error"] = stderr or "Processing failed"

    except subprocess.TimeoutExpired:
        job["status"] = "failed"
        job["error"] = "Processing timeout (5 minutes)"
    except Exception as e:
        job["status"] = "failed"
        job["error"] = str(e)

@app.get("/api/status/{job_id}")
async def get_status(job_id: str):
    """Get job status"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    return jobs[job_id]

@app.get("/api/download/{job_id}")
async def download_file(job_id: str):
    """Download processed file"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    job = jobs[job_id]

    if job["status"] != "complete":
        raise HTTPException(status_code=400, detail="Job not complete")

    output_path = Path(job["output_path"])

    if not output_path.exists():
        raise HTTPException(status_code=404, detail="Output file not found")

    return FileResponse(
        output_path,
        filename=f"{job['filename'].rsplit('.', 1)[0]}.md",
        media_type="text/markdown"
    )

@app.get("/api/jobs")
async def list_jobs():
    """List all jobs"""
    return {"jobs": jobs}

@app.delete("/api/jobs/{job_id}")
async def delete_job(job_id: str):
    """Delete a job"""
    if job_id in jobs:
        job = jobs[job_id]

        # Clean up files
        if "input_path" in job:
            Path(job["input_path"]).unlink(missing_ok=True)
        if "output_path" in job:
            Path(job["output_path"]).unlink(missing_ok=True)

        del jobs[job_id]

        return {"status": "deleted"}

    raise HTTPException(status_code=404, detail="Job not found")

# =============================================================================
# Main
# =============================================================================

def get_local_ip():
    """Get local IP address for WiFi connection"""
    try:
        # Create a socket to find local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def generate_qr_code(url):
    """Generate ASCII QR code for terminal display (50% width and height)"""
    qr = qrcode.QRCode(border=1, box_size=1)
    qr.add_data(url)
    qr.make()

    # Generate compact QR code using half-block characters (50% height)
    output = []
    matrix = qr.get_matrix()

    # Process two rows at a time
    for i in range(0, len(matrix), 2):
        line = ""
        top_row = matrix[i]
        bottom_row = matrix[i + 1] if i + 1 < len(matrix) else [False] * len(top_row)

        for j in range(len(top_row)):
            top = top_row[j]
            bottom = bottom_row[j]

            if top and bottom:
                line += "█"  # Both black
            elif top and not bottom:
                line += "▀"  # Top black, bottom white
            elif not top and bottom:
                line += "▄"  # Top white, bottom black
            else:
                line += " "  # Both white

        output.append(line)
    return "\n".join(output)

if __name__ == "__main__":
    import uvicorn

    # Get local IP and generate QR code
    local_ip = get_local_ip()
    url = f"http://{local_ip}:8888"
    qr_code = generate_qr_code(url)

    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                    ✨ Aster Web Server                   ║
    ║         Navigate your constellation of knowledge         ║
    ╚═══════════════════════════════════════════════════════════╝
    """)

    print(f"    📱 Scan this QR code with your iPhone:\n")
    print("    " + "\n    ".join(qr_code.split("\n")))

    print(f"""
    🌐 Access from:
      • This Mac: http://localhost:8888
      • iPhone/iPad: {url}
      • Or scan the QR code above ☝️

    💡 Tip: Bookmark on iPhone home screen for quick access!

    Press Ctrl+C to stop
    """)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8888,
        log_level="info"
    )
