# Aster iPhone Integration Guide

## Quick Start (5 Minutes) 🚀

### Step 1: Start Aster Web Server on Mac

```bash
cd /Users/mac/Documents/Applications/repos/aster

# Install web dependencies
pip3 install fastapi uvicorn python-multipart

# Start server
python3 aster_web.py
```

You'll see:
```
✨ Aster Web Server
Navigate your constellation of knowledge

Starting server on: http://0.0.0.0:8888

Access from:
  • This Mac: http://localhost:8888
  • iPhone/iPad: http://YOUR-MAC-IP:8888
```

### Step 2: Find Your Mac's IP Address

**Option A: System Settings**
- System Settings → Network → Wi-Fi → Details
- Look for "IP Address" (e.g., `192.168.1.100`)

**Option B: Terminal**
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
# Look for something like: inet 192.168.1.100
```

### Step 3: Access from iPhone

On your iPhone (same WiFi):
1. Open Safari
2. Go to: `http://192.168.1.100:8888` (use your Mac's IP)
3. Bookmark it for easy access!

**You're done!** 🎉

---

## Using Aster from iPhone

### Web Interface

**Upload Files:**
1. Tap the upload zone or drag files
2. Select preset (auto/book/ocr/etc.)
3. Watch processing progress
4. Download or view results

**Supported Files:**
- Documents: PDF, DOCX, PPTX
- Images: JPG, PNG (with OCR)
- Data: CSV, Excel
- Text: TXT, MD, HTML
- Audio: MP3, WAV, M4A
- Ebooks: EPUB

**Features:**
- ✨ Real-time progress
- 📊 Success statistics
- 💾 Download processed files
- 👁️ Preview results

---

## iOS Shortcuts Integration

### Create "Process with Aster" Shortcut

1. Open **Shortcuts** app on iPhone
2. Tap **+** to create new shortcut
3. Add these actions:

#### Action 1: Get File
```
Get File from [Shortcut Input]
```

#### Action 2: Set Variable
```
Set variable [filename] to [Shortcut Input > Name]
```

#### Action 3: Get Contents of URL (Upload)
```
Get contents of: http://YOUR-MAC-IP:8888/api/process
  Method: POST
  Headers:
    Content-Type: multipart/form-data
  Request Body: Form
    file: [File]
    preset: auto
    model: llama3.2:1b
```

#### Action 4: Get Dictionary Value
```
Get [job_id] from [Contents of URL]
Set variable [jobID] to [Dictionary Value]
```

#### Action 5: Wait and Poll
```
Repeat 60 times
  Wait 2 seconds
  Get contents of: http://YOUR-MAC-IP:8888/api/status/[jobID]
  Get [status] from [Contents of URL]
  If [status] is "complete"
    Stop this shortcut and output [Contents of URL]
  End If
End Repeat
```

#### Action 6: Download Result
```
Get contents of: http://YOUR-MAC-IP:8888/api/download/[jobID]
```

#### Action 7: Save File
```
Save [Contents of URL] to:
  iCloud Drive/Aster/
  or
  Obsidian Vault/Inbox/
```

#### Action 8: Show Notification
```
Show notification:
  Title: "Aster Complete"
  Body: "Processed [filename]"
```

### Use the Shortcut

**From Files App:**
1. Long-press a file
2. Share → **Shortcuts** → **Process with Aster**
3. Wait for notification
4. File appears in your vault!

**From Share Sheet:**
- Works in: Photos, Safari, Notes, Mail
- Share → **Process with Aster**

**Voice Command:**
- "Hey Siri, process with Aster"
- Select file
- Done!

---

## Advanced: Access from Anywhere (Tailscale)

**Problem:** Mac at home, you're on cellular data

**Solution:** [Tailscale](https://tailscale.com) - Free VPN

### Setup (One-Time)

**On Mac:**
```bash
brew install tailscale
sudo tailscale up
# Note the Tailscale IP (e.g., 100.64.0.2)
```

**On iPhone:**
1. Install Tailscale from App Store
2. Sign in with same account
3. Connect

**Access Aster:**
- Old (WiFi only): `http://192.168.1.100:8888`
- New (anywhere): `http://100.64.0.2:8888`

Update your Shortcut with the Tailscale IP!

---

## Automation Ideas

### 1. Auto-Process Downloads
**iOS Automation:**
- Trigger: File downloaded to specific folder
- Action: Run "Process with Aster"
- Result: Auto-processes PDFs you download

### 2. Meeting Notes Flow
**Shortcut:**
- Take photo of whiteboard
- Run through Aster (OCR)
- Save to: Obsidian/Meetings/[Date].md

### 3. Receipt Scanner
**Shortcut:**
- Photo receipt
- Aster OCR → Extract text
- Parse amount/vendor with Ollama
- Save to Finances folder

### 4. Book Ingestion
**Shortcut:**
- Select PDF from Files
- Process with "book" preset
- Save to Obsidian/Books/
- Create link in reading list

---

## Troubleshooting

### Can't Access from iPhone

**Check:**
1. Mac and iPhone on same WiFi?
2. Is aster_web.py running on Mac?
3. Firewall blocking port 8888?
   ```bash
   # Allow in firewall
   sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add python3
   ```
4. Try Mac's IP in Safari first (before Shortcut)

### "Connection Refused"

- Server not running on Mac
- Wrong IP address
- Port 8888 blocked

### Slow Processing

- Large file (expected)
- Ollama model still loading
- Mac is asleep (keep awake)

### "Job Not Found"

- Server restarted (jobs are in memory)
- Wait for ongoing job to complete

---

## Tips & Tricks

### Battery Life
- Keep Mac plugged in
- Or use "Energy Saver" to prevent sleep

### Speed
- Use `llama3.2:1b` for speed
- Use `llama3.2:3b` for quality
- OCR is slower than PDF extraction

### Organizing Results
**Create folder structure:**
```
Obsidian Vault/
  Inbox/          # Raw Aster outputs
  Processed/      # Reviewed and tagged
  Books/          # Book notes
  Meetings/       # Meeting notes
  Finances/       # Financial docs
```

**Use Shortcut variants:**
- "Aster → Inbox" (default)
- "Aster → Books" (with book preset)
- "Aster → Meetings" (with OCR preset)

### Privacy
- All processing on your Mac
- No cloud uploads
- Ollama runs locally
- iPhone → Mac direct connection

---

## Next Steps

### Week 1: Basic Use
- Process 10-20 documents
- Test different presets
- Build muscle memory

### Week 2: Optimize
- Create custom presets for your needs
- Set up auto-processing workflows
- Integrate with Obsidian

### Week 3: Advanced
- Add Tailscale for anywhere access
- Create specialized Shortcuts
- Share workflows with family

---

## Support

**Common Questions:**

**Q: Can I use on cellular data?**
A: Yes, with Tailscale (free)

**Q: Can I process multiple files?**
A: Yes! Select multiple in Files app

**Q: Does it work offline?**
A: Server needs to run on Mac, but Mac can be offline

**Q: Can I use different Ollama models?**
A: Yes, change in preset dropdown

**Q: How secure is this?**
A: Very - all processing local, no cloud

**Q: Can multiple people use it?**
A: Yes, anyone on same WiFi (or Tailscale network)

---

## Web Interface Features

### Dashboard
- Total documents processed
- Success rate
- Queue size

### Upload
- Drag & drop or tap to browse
- Multiple files at once
- Real-time progress bars

### Jobs List
- See all processing jobs
- Download completed files
- View results inline
- Retry failed jobs

### Settings (in web UI)
- Choose preset
- Select Ollama model
- Default output location

---

## Happy Navigating! ✨

You now have Aster accessible from your iPhone - process documents anytime, anywhere!

Questions? Issues? Let me know!
