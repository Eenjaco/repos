---
template: Quick Time Entry
description: Fast time entry template for Obsidian/Shortcuts
---

## Quick Entry Template

Use this in Obsidian with Templater plugin or Apple Shortcuts.

### For Manual Entry (Copy to weekly file):

```
| {{date:YYYY-MM-DD}} | [Category] | [Subcategory] | [HH:MM] | [HH:MM] | [duration] | [description] |
```

### Example:

```
| 2025-11-14 | Sermon | Writing | 14:30 | 16:00 | 1h 30m | Draft introduction |
```

### Apple Shortcuts Version:

**Variables to prompt:**
- Category (Choice menu: Sermon, Admin, Study, etc.)
- Subcategory (Text input)
- Start Time (Time picker)
- End Time (Time picker)

**Calculate duration:**
```javascript
hours = (endTime - startTime) / 3600
minutes = ((endTime - startTime) % 3600) / 60
duration = hours + "h " + minutes + "m"
```

**Append to file:**
```
{{current_week_file}}
| {{date}} | {{category}} | {{subcategory}} | {{start}} | {{end}} | {{duration}} | {{description}} |
```

**File path:**
```
/path/to/tt_standalone/time_logs/{{year}}_W{{week}}_time.md
```
