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
    <title>Aster - Navigate your constellation of knowledge</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1e3a5f 0%, #0f1c2e 100%);
            color: #e0e6ed;
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            margin-bottom: 40px;
            padding: 20px 0;
        }

        h1 {
            font-size: 2.5em;
            font-weight: 300;
            margin-bottom: 10px;
            color: #f5c469;
        }

        .tagline {
            font-size: 1.1em;
            color: #9daab8;
            font-style: italic;
        }

        .upload-zone {
            background: rgba(255, 255, 255, 0.05);
            border: 2px dashed #4a5f7f;
            border-radius: 12px;
            padding: 60px 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            margin-bottom: 30px;
        }

        .upload-zone:hover, .upload-zone.dragover {
            background: rgba(245, 196, 105, 0.1);
            border-color: #f5c469;
        }

        .upload-icon {
            font-size: 4em;
            margin-bottom: 20px;
        }

        .upload-text {
            font-size: 1.2em;
            color: #9daab8;
        }

        input[type="file"] {
            display: none;
        }

        .options {
            display: flex;
            gap: 15px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }

        .options select {
            flex: 1;
            min-width: 150px;
            padding: 12px;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid #4a5f7f;
            border-radius: 8px;
            color: #e0e6ed;
            font-size: 1em;
        }

        .job {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            border-left: 4px solid #4a5f7f;
        }

        .job.processing {
            border-left-color: #f5c469;
        }

        .job.complete {
            border-left-color: #6ec98c;
        }

        .job.failed {
            border-left-color: #e76f51;
        }

        .job-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }

        .job-name {
            font-weight: 600;
            font-size: 1.1em;
        }

        .job-status {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.9em;
            background: rgba(255, 255, 255, 0.1);
        }

        .progress-bar {
            height: 8px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
            overflow: hidden;
            margin: 10px 0;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #f5c469, #f5a269);
            transition: width 0.3s;
        }

        .job-actions {
            margin-top: 15px;
            display: flex;
            gap: 10px;
        }

        button {
            padding: 10px 20px;
            background: #f5c469;
            color: #0f1c2e;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }

        button:hover {
            background: #f5a269;
            transform: translateY(-2px);
        }

        button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }

        .secondary {
            background: rgba(255, 255, 255, 0.1);
            color: #e0e6ed;
        }

        .secondary:hover {
            background: rgba(255, 255, 255, 0.15);
        }

        .empty-state {
            text-align: center;
            padding: 40px;
            color: #9daab8;
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }

        .stat {
            background: rgba(255, 255, 255, 0.05);
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }

        .stat-value {
            font-size: 2em;
            font-weight: 600;
            color: #f5c469;
        }

        .stat-label {
            font-size: 0.9em;
            color: #9daab8;
            margin-top: 5px;
        }

        @media (max-width: 600px) {
            h1 {
                font-size: 2em;
            }

            .options {
                flex-direction: column;
            }

            .job-header {
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>✨ Aster</h1>
            <p class="tagline">"Lost in a night-sky of notes? Aster lights the way."</p>
        </header>

        <div class="stats">
            <div class="stat">
                <div class="stat-value" id="totalJobs">0</div>
                <div class="stat-label">Processed</div>
            </div>
            <div class="stat">
                <div class="stat-value" id="successRate">-</div>
                <div class="stat-label">Success Rate</div>
            </div>
            <div class="stat">
                <div class="stat-value" id="queueSize">0</div>
                <div class="stat-label">In Queue</div>
            </div>
        </div>

        <div class="upload-zone" id="dropZone">
            <div class="upload-icon">📁</div>
            <div class="upload-text">Drop files here or tap to browse</div>
            <input type="file" id="fileInput" multiple accept=".pdf,.docx,.pptx,.jpg,.jpeg,.png,.html,.txt,.md,.csv,.xlsx,.epub,.mp3,.wav,.m4a,.wma">
        </div>

        <div class="options">
            <select id="preset">
                <option value="auto">Auto-detect</option>
                <option value="book">Book</option>
                <option value="ocr">OCR</option>
                <option value="transcribe">Transcribe</option>
                <option value="financial">Financial</option>
                <option value="afrikaans_religious">Afrikaans Religious</option>
            </select>

            <select id="model">
                <option value="llama3.2:1b">llama3.2:1b (Fast)</option>
                <option value="llama3.2:3b">llama3.2:3b (Better)</option>
            </select>
        </div>

        <div id="jobs"></div>

        <div class="empty-state" id="emptyState">
            <p>No documents processed yet</p>
            <p style="margin-top: 10px; font-size: 0.9em;">Drop a file above to start</p>
        </div>
    </div>

    <script>
        const dropZone = document.getElementById('dropZone');
        const fileInput = document.getElementById('fileInput');
        const jobsContainer = document.getElementById('jobs');
        const emptyState = document.getElementById('emptyState');

        let jobs = {};
        let stats = { total: 0, success: 0, queue: 0 };

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
            const preset = document.getElementById('preset').value;
            const model = document.getElementById('model').value;

            const formData = new FormData();
            formData.append('file', file);
            formData.append('preset', preset);
            formData.append('model', model);

            try {
                const response = await fetch('/api/process', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (response.ok) {
                    addJob(data.job_id, file.name, preset);
                    pollJob(data.job_id);
                } else {
                    alert('Upload failed: ' + data.error);
                }
            } catch (error) {
                alert('Upload failed: ' + error.message);
            }
        }

        function addJob(jobId, filename, preset) {
            emptyState.style.display = 'none';

            const jobEl = document.createElement('div');
            jobEl.className = 'job processing';
            jobEl.id = 'job-' + jobId;
            jobEl.innerHTML = `
                <div class="job-header">
                    <div class="job-name">${filename}</div>
                    <div class="job-status">Processing...</div>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: 10%"></div>
                </div>
                <div style="font-size: 0.9em; color: #9daab8; margin-top: 10px;">
                    Preset: ${preset}
                </div>
            `;

            jobsContainer.prepend(jobEl);
            jobs[jobId] = { filename, preset, el: jobEl };

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
                        } else {
                            stats.queue--;
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
                el.querySelector('.job-status').textContent = '✓ Complete';
                el.querySelector('.progress-fill').style.width = '100%';

                const actions = document.createElement('div');
                actions.className = 'job-actions';
                actions.innerHTML = `
                    <button onclick="downloadFile('${jobId}')">Download</button>
                    <button class="secondary" onclick="viewFile('${jobId}')">View</button>
                `;
                el.appendChild(actions);
            } else if (data.status === 'failed') {
                el.className = 'job failed';
                el.querySelector('.job-status').textContent = '✗ Failed';
                el.innerHTML += `<div style="color: #e76f51; margin-top: 10px;">${data.error || 'Unknown error'}</div>`;
            } else {
                const progress = data.progress || 50;
                el.querySelector('.progress-fill').style.width = progress + '%';
                el.querySelector('.job-status').textContent = 'Processing ' + progress + '%...';
            }
        }

        function updateStats() {
            document.getElementById('totalJobs').textContent = stats.total;
            document.getElementById('queueSize').textContent = stats.queue;

            const rate = stats.total > 0 ? Math.round((stats.success / stats.total) * 100) + '%' : '-';
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
    """Generate ASCII QR code for terminal display"""
    qr = qrcode.QRCode(border=1, box_size=1)
    qr.add_data(url)
    qr.make()

    # Generate compact ASCII QR code (single characters)
    output = []
    matrix = qr.get_matrix()
    for row in matrix:
        line = ""
        for cell in row:
            line += "█" if cell else " "
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
