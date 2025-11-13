# Apple Shortcuts Setup for tt-local

**Quick Summary:** Create two Shortcuts (Start Timer & Stop Timer) that run the tt-local-shortcuts script

---

## Prerequisites

- ✅ `tt-local-shortcuts` script installed and executable
- ✅ Located at: `/Users/mac/Documents/Local Vault/Projects/Time Keeping/tt-local-shortcuts`
- ✅ iOS Shortcuts app installed
- ✅ (Optional) SSH access from iPhone to Mac for remote use

---

## Shortcut 1: Start Timer

### Setup Steps

1. **Open Shortcuts app** on iPhone or Mac
2. **Create New Shortcut** (+ button)
3. **Name it:** "Start Timer" or "tt start"

### Actions to Add

#### Action 1: Ask for Input (Text)
- **Prompt:** "Task Title"
- **Variable Name:** Title

#### Action 2: Ask for Input (Text) [Optional]
- **Prompt:** "Subtitle (optional)"
- **Variable Name:** Subtitle
- **Default Value:** (leave blank)

#### Action 3: Run Shell Script
- **Shell:** /bin/bash
- **Input:** (none)
- **Script:**
```bash
/Users/mac/Documents/Local\ Vault/Projects/Time\ Keeping/tt-local-shortcuts s "Title" "Subtitle" "/Users/mac/Documents/Local Vault/Projects/Time Keeping"
```

**Replace Variables:**
- Click on "Title" in the script → Select "Title" from variables
- Click on "Subtitle" → Select "Subtitle" from variables

#### Action 4: Show Notification [Optional]
- **Title:** "Timer Started"
- **Body:** Use the output from "Shell Script"

### Final Script Should Look Like:
```bash
/Users/mac/Documents/Local\ Vault/Projects/Time\ Keeping/tt-local-shortcuts s "[Title variable]" "[Subtitle variable]" "/Users/mac/Documents/Local Vault/Projects/Time Keeping"
```

---

## Shortcut 2: Stop Timer

### Setup Steps

1. **Open Shortcuts app**
2. **Create New Shortcut** (+ button)
3. **Name it:** "Stop Timer" or "tt stop"

### Actions to Add

#### Action 1: Run Shell Script
- **Shell:** /bin/bash
- **Input:** (none)
- **Script:**
```bash
/Users/mac/Documents/Local\ Vault/Projects/Time\ Keeping/tt-local-shortcuts e "/Users/mac/Documents/Local Vault/Projects/Time Keeping"
```

#### Action 2: Show Notification [Optional]
- **Title:** "Timer Stopped"
- **Body:** Use the output from "Shell Script"

---

## Usage

### On Mac

**Start Timer:**
1. Run "Start Timer" shortcut
2. Enter task title (e.g., "Email and admin work")
3. Enter subtitle (optional, e.g., "Morning tasks")
4. Timer starts

**Stop Timer:**
1. Run "Stop Timer" shortcut
2. Timer stops and appends to weekly file

### On iPhone (with SSH)

**Prerequisites:**
- SSH access to Mac configured (see `/Projects/ssh/README.md`)
- Mac must be awake and on same network

**Start Timer:**
1. Run "Start Timer" shortcut
2. If prompted, allow SSH connection
3. Enter task details
4. Timer starts on Mac

**Stop Timer:**
1. Run "Stop Timer" shortcut
2. Timer stops and saves to Mac

---

## Troubleshooting

### Error: "timer already running"
**Problem:** You started a timer but didn't stop it
**Solution:** Run "Stop Timer" first, then start a new one

### Error: "no running timer"
**Problem:** Trying to stop when no timer is active
**Solution:** Make sure you started a timer first

### Error: "command not found" or "permission denied"
**Problem:** Path is wrong or script not executable
**Solutions:**
1. Check path is correct (use absolute path)
2. Verify executable: `ls -l /Users/mac/Documents/Local\ Vault/Projects/Time\ Keeping/tt-local-shortcuts`
3. Make executable if needed: `chmod +x /path/to/tt-local-shortcuts`

### Error on iPhone: "Connection refused"
**Problem:** Mac is asleep or SSH not working
**Solutions:**
1. Wake Mac
2. Verify SSH connection: `ssh mac@192.168.68.58`
3. Check SSH setup: see `/Projects/ssh/README.md`

### Shortcuts runs but nothing saved
**Problem:** Output directory might not exist
**Solution:** Check that `/Users/mac/Documents/Local Vault/Projects/Time Keeping/` exists

---

## Advanced Usage

### Add to Home Screen (iPhone)

1. Open Shortcuts app
2. Long-press on "Start Timer" shortcut
3. Select "Add to Home Screen"
4. Repeat for "Stop Timer"

**Result:** One-tap timer start/stop from iPhone home screen

### Siri Integration

Both shortcuts automatically work with Siri:

- "Hey Siri, Start Timer"
- "Hey Siri, Stop Timer"

You'll be prompted for task details when starting.

### Widget Support

Add Shortcuts widget to home screen for quick access:
1. Long-press home screen → Add Widget
2. Find Shortcuts widget
3. Add "Start Timer" and "Stop Timer"

---

## Example Workflow

### Morning Work Session

**9:00 AM - Start:**
- Run "Start Timer"
- Title: "Morning planning"
- Subtitle: "Review goals and priorities"

**10:30 AM - Stop & Start New:**
- Run "Stop Timer"
- Run "Start Timer"
- Title: "Code implementation"
- Subtitle: "tt-local feature"

**12:00 PM - Stop:**
- Run "Stop Timer"

**Result in `2025-W45.md`:**
```
———
Morning planning
Review goals and priorities
Start time: 07 Nov 2025 at 09:00:00
until
End Time: 07 Nov 2025 at 10:30:00

———
Code implementation
tt-local feature
Start time: 07 Nov 2025 at 10:30:30
until
End Time: 07 Nov 2025 at 12:00:00
```

---

## Tips

### Keep It Simple
- Use clear, descriptive titles
- Subtitle is optional - only use if needed
- Don't overthink it

### Consistent Naming
Use similar patterns for similar work:
- "Email and admin" (not "emails" or "admin work")
- "Code: [feature name]"
- "Meeting: [topic]"

### Quick Capture
When in doubt:
- Start timer with simple title
- Add details in subtitle if needed
- Can always edit the markdown file later

---

## Alternative: Terminal Usage

If you prefer terminal over Shortcuts:

**Interactive version (Mac terminal):**
```bash
# Start
/Users/mac/Documents/Local\ Vault/Projects/Time\ Keeping/tt-local s

# Prompts for Title and Subtitle
# Timer starts

# Stop
/Users/mac/Documents/Local\ Vault/Projects/Time\ Keeping/tt-local e
```

**Non-interactive version (scripts/automation):**
```bash
# Start
/Users/mac/Documents/Local\ Vault/Projects/Time\ Keeping/tt-local-shortcuts s "Task Title" "Subtitle" "/Users/mac/Documents/Local Vault/Projects/Time Keeping"

# Stop
/Users/mac/Documents/Local\ Vault/Projects/Time\ Keeping/tt-local-shortcuts e "/Users/mac/Documents/Local Vault/Projects/Time Keeping"
```

---

## Files Reference

- **Interactive script:** `tt-local` (for terminal use)
- **Shortcuts script:** `tt-local-shortcuts` (for Shortcuts app)
- **Weekly files:** `2025-W[XX].md` (ISO week format)
- **State file:** `.tt_local_state` (temporary, tracks active timer)

---

## Next Steps

1. ✅ Create "Start Timer" Shortcut
2. ✅ Create "Stop Timer" Shortcut
3. ✅ Test on Mac
4. ✅ (Optional) Test from iPhone via SSH
5. ✅ Add to Home Screen
6. ✅ Start tracking your time!

---

**Questions?** Check `/Projects/Time Keeping/tt_update.md` for technical details.
