# Apple Shortcuts Setup for Obsidian Timer

Complete guide to create Apple Shortcuts that replicate your Apple Notes timer workflow in Obsidian.

## Timer File Location

```
/Users/mac/Library/Mobile Documents/iCloud~md~obsidian/Documents/Shared Vault/time_keeping/current_task_timer.md
```

---

## Shortcut 1: Start Timer

**Name:** Time Tracker Start

### Actions:

1. **Ask for Input**
   - Question: "Category?"
   - Input Type: Choose from Menu
   - Menu items:
     - Pastoral & Community
     - Communication
     - Sermon
     - Admin
     - Operations
     - Prayer
     - Sinod

2. **Set Variable** `category` = Chosen Item

3. **Ask for Input**
   - Question: "Subcategory?"
   - Input Type: Text
   - Default answer: (leave empty)

4. **Set Variable** `subcategory` = Provided Input

5. **Get Current Date**
   - Date Format: Custom
   - Custom Format: `d MMM yyyy 'at' HH:mm:ss`

6. **Set Variable** `startTime` = Formatted Date

7. **Text** (compose the entry):
```
———
{category}
{subcategory}
Start time: {startTime}
until
```

8. **Get File**
   - Service: iCloud Drive (Obsidian)
   - Path: `Obsidian/Shared Vault/time_keeping/current_task_timer.md`
   - Error: If Doesn't Exist → Continue

9. **Append to File**
   - File: current_task_timer.md
   - Text: {composed text from step 7}
   - Make New Line: Yes

10. **Show Notification**
    - Title: "Timer Started"
    - Body: "{category} - {subcategory}"

---

## Shortcut 2: Stop Timer

**Name:** Time Tracker Stop

### Actions:

1. **Get File**
   - Service: iCloud Drive (Obsidian)
   - Path: `Obsidian/Shared Vault/time_keeping/current_task_timer.md`

2. **Get Text from File**
   - Variable: `fileContent`

3. **If** `fileContent` contains "until"
   - Then: Continue
   - Otherwise:
     - Show Alert "No active timer found"
     - Stop shortcut

4. **Get Current Date**
   - Date Format: Custom
   - Custom Format: `d MMM yyyy 'at' HH:mm:ss`

5. **Set Variable** `endTime` = Formatted Date

6. **Replace Text**
   - Find: `until`
   - Replace with: `End Time: {endTime}`
   - In: `fileContent`

7. **Save File**
   - File: current_task_timer.md
   - Content: {replaced text}
   - Overwrite: Yes

8. **Show Notification**
   - Title: "Timer Stopped"
   - Body: "Entry saved at {endTime}"

---

## Shortcut 3: Check Active Timer

**Name:** Time Tracker Status

### Actions:

1. **Get File**
   - Path: `current_task_timer.md`

2. **Get Text from File**

3. **If** contains "until"
   - Then:
     - Split text by "———"
     - Get Last Item
     - Extract lines
     - Show notification:
       - Title: "⏱️ Timer Running"
       - Body: "{category}\n{subcategory}\nStarted: {startTime}"
   - Otherwise:
     - Show notification:
       - Title: "No Active Timer"
       - Body: "Start a new timer?"

---

## iOS Shortcuts App Instructions

### Creating the Shortcuts:

1. Open **Shortcuts** app on iPhone
2. Tap **+** to create new shortcut
3. Follow the actions listed above
4. Name the shortcut
5. Add to Home Screen for quick access

### Adding iCloud Drive Access:

When you run the shortcut for the first time, it will ask for permission to access:
- iCloud Drive
- Obsidian folder

**Grant these permissions**

### Accessing Obsidian Files:

The path in shortcuts should be:
```
iCloud Drive/Obsidian/Shared Vault/time_keeping/current_task_timer.md
```

Or use the file picker to navigate:
1. iCloud Drive
2. Obsidian
3. Shared Vault
4. time_keeping
5. current_task_timer.md

---

## Alternative: Using Obsidian URI

If you have Obsidian mobile app, you can use Obsidian URIs:

### Start Timer with URI:

```
obsidian://vault/Shared%20Vault/time_keeping/current_task_timer.md?mode=append&content=———%0A{category}%0A{subcategory}%0AStart%20time:%20{timestamp}%0Auntil%0A
```

### Actions:

1. Ask for category
2. Ask for subcategory
3. Get current date
4. URL Encode the content
5. Open URL: `obsidian://vault/...`

---

## Siri Integration

Add Siri phrases to your shortcuts:

**For Start Timer:**
- "Start tracking time"
- "Begin timer"
- "Track my time"

**For Stop Timer:**
- "Stop timer"
- "End tracking"
- "Stop time"

**For Status:**
- "Timer status"
- "What am I tracking"
- "Check my timer"

---

## Home Screen Widgets

Create home screen buttons:

1. Long press shortcut
2. Tap **Details**
3. Tap **Add to Home Screen**
4. Choose icon and color
5. Name it (e.g., "⏱️ Start" or "⏹️ Stop")

---

## Testing

1. Run "Time Tracker Start"
2. Choose: Sermon → Writing
3. Check Obsidian file - should see:
```
———
Sermon
Writing
Start time: 15 Nov 2025 at 14:30:45
until
```

4. Run "Time Tracker Stop"
5. Check file - should see:
```
———
Sermon
Writing
Start time: 15 Nov 2025 at 14:30:45
End Time: 15 Nov 2025 at 16:15:20
```

6. Check on Mac:
```bash
ttwatch  # Watchdog should detect and sync to SQLite
tt       # CLI should show the new entry
```

---

## Troubleshooting

**Issue:** File not found
- Create the file manually in Obsidian first
- Or let the watchdog script create it

**Issue:** Permission denied
- Grant Shortcuts app access to iCloud Drive
- Grant Shortcuts app access to Obsidian folder

**Issue:** Doesn't append properly
- Check file path is correct
- Try using absolute path
- Check file isn't corrupted

**Issue:** Watchdog doesn't detect changes
- Ensure iCloud is syncing (check status bar)
- Run manual sync: `python3 parse_timer_format.py /path/to/file`

---

## Sample Output Format

Your timer file will look like this:

```markdown
———
Pastoral & Community
besoek
Start time: 13 Nov 2025 at 11:04:13
End Time: 14 Nov 2025 at 13:08:33

———
Communication
newsletter
Start time: 14 Nov 2025 at 13:08:50
End Time: 14 Nov 2025 at 15:22:10

———
Sermon
research
Start time: 14 Nov 2025 at 16:00:00
until
```

Last entry is still running (ends with "until").

---

## Next Steps

1. Create the three shortcuts
2. Test start/stop on phone
3. Run watchdog on Mac: `ttwatch`
4. Verify sync: `tt`
5. Set up weekly archive (see `weekly_archive.sh`)

Happy time tracking! 🎉
