# Time Tracker Color Customization Guide

**Current Theme:** Omarchy (Green + Dark Grey-Blue)

---

## 🎨 How to Change Colors

### **Edit the `tt` file:**

```bash
cd "/Users/mac/Documents/Terminal/Claude/Projects/Time Keeping"
nano tt
```

**Or with any text editor:**
```bash
code tt        # VS Code
vim tt         # Vim
open -a TextEdit tt    # TextEdit
```

---

## 🖌️ Color Codes Section

Look for this section near the top of the `tt` file (around line 16-38):

```javascript
// Omarchy Color Theme
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  dim: '\x1b[2m',

  // Omarchy theme colors
  green: '\x1b[38;5;42m',        // Bright green (like code highlighting)
  darkBlue: '\x1b[38;5;67m',     // Dark grey-blue
  cyan: '\x1b[38;5;80m',         // Lighter blue-cyan
  orange: '\x1b[38;5;214m',      // Warm orange for warnings
  yellow: '\x1b[38;5;226m',      // Yellow for highlights
  grey: '\x1b[38;5;240m',        // Dark grey
  white: '\x1b[38;5;255m',       // Bright white

  // Semantic colors (what each color represents)
  success: '\x1b[38;5;42m',      // Green - achievements, completed
  progress: '\x1b[38;5;80m',     // Cyan - in progress
  header: '\x1b[38;5;67m',       // Dark blue - section headers
  number: '\x1b[38;5;226m',      // Yellow - numbers, percentages
  category: '\x1b[38;5;67m',     // Dark blue - category names
  time: '\x1b[38;5;42m',         // Green - time durations
  label: '\x1b[38;5;240m',       // Grey - descriptive labels
};
```

---

## 🌈 Color Code Reference

### **Current Omarchy Theme:**

| Color | Code | Where It's Used |
|-------|------|-----------------|
| **Bright Green** | `42` | Time durations, achievements, "goal achieved" |
| **Dark Grey-Blue** | `67` | Category names, section headers |
| **Cyan** | `80` | Progress bars (75%+), progress indicators |
| **Orange** | `214` | Remaining time warnings |
| **Yellow** | `226` | Numbers, percentages |
| **Dark Grey** | `240` | Labels, separators, subtle text |
| **White** | `255` | Not currently used (reserved) |

---

## 🎨 Popular Color Options

### **Greens:**
- `28` - Forest green (darker)
- `34` - Sea green
- `35` - Lime green
- `40` - Light green
- `42` - Bright green ⭐ (current)
- `46` - Neon green
- `47` - Spring green
- `48` - Mint green

### **Blues:**
- `33` - Dodger blue
- `39` - Light cyan blue
- `51` - Cyan blue
- `67` - Steel blue / Dark grey-blue ⭐ (current)
- `69` - Cornflower blue
- `75` - Light steel blue
- `81` - Sky blue

### **Purples/Magentas:**
- `93` - Light magenta
- `99` - Purple
- `135` - Orchid
- `141` - Light purple

### **Oranges/Yellows:**
- `208` - Orange
- `214` - Light orange ⭐ (current)
- `220` - Gold
- `226` - Yellow ⭐ (current)
- `228` - Light yellow

### **Greys:**
- `236` - Very dark grey
- `238` - Dark grey
- `240` - Medium dark grey ⭐ (current)
- `244` - Medium grey
- `248` - Light grey
- `252` - Very light grey

### **Reds:**
- `160` - Red
- `196` - Bright red
- `203` - Pink
- `210` - Salmon

---

## 🔧 How to Change a Color

### **Example: Change time durations from green to cyan**

**Find:**
```javascript
time: '\x1b[38;5;42m',         // Green - time durations
```

**Change to:**
```javascript
time: '\x1b[38;5;51m',         // Cyan blue - time durations
```

**Save and test:**
```bash
tt
```

---

## 🎯 Common Customizations

### **1. Make It More Vibrant**
```javascript
green: '\x1b[38;5;46m',        // Neon green (was 42)
cyan: '\x1b[38;5;51m',         // Bright cyan (was 80)
yellow: '\x1b[38;5;220m',      // Gold (was 226)
```

### **2. Make It Softer/Pastel**
```javascript
green: '\x1b[38;5;35m',        // Softer green (was 42)
darkBlue: '\x1b[38;5;75m',     // Lighter blue (was 67)
orange: '\x1b[38;5;210m',      // Salmon (was 214)
```

### **3. Purple/Pink Theme**
```javascript
green: '\x1b[38;5;141m',       // Light purple (was 42)
darkBlue: '\x1b[38;5;99m',     // Purple (was 67)
cyan: '\x1b[38;5;135m',        // Orchid (was 80)
```

### **4. Classic Blue/Green**
```javascript
green: '\x1b[38;5;40m',        // Classic green (was 42)
darkBlue: '\x1b[38;5;33m',     // Dodger blue (was 67)
cyan: '\x1b[38;5;39m',         // Light cyan (was 80)
```

### **5. Warm/Orange Theme**
```javascript
green: '\x1b[38;5;220m',       // Gold (was 42)
darkBlue: '\x1b[38;5;214m',    // Orange (was 67)
cyan: '\x1b[38;5;208m',        // Darker orange (was 80)
```

---

## 📊 What Each Color Controls

### **Headers:**
```javascript
header: '\x1b[38;5;67m',       // "📊 This Week's Progress"
```

### **Category Names:**
```javascript
category: '\x1b[38;5;67m',     // "Sermon", "Operations", etc.
```

### **Time Values:**
```javascript
time: '\x1b[38;5;42m',         // "7h 59m", "12h", etc.
```

### **Numbers/Percentages:**
```javascript
number: '\x1b[38;5;226m',      // "67%", "5.2h"
```

### **Remaining Time:**
```javascript
orange: '\x1b[38;5;214m',      // "4h remaining"
```

### **Labels:**
```javascript
label: '\x1b[38;5;240m',       // "Total Week:", "remaining", etc.
```

### **Separators:**
```javascript
grey: '\x1b[38;5;240m',        // "────────────"
```

---

## 🎨 Progress Bar Colors

Progress bars change color based on percentage:

```javascript
// In the colorProgressBar function (around line 46)

if (percentage >= 100) {
  bar = c('█'.repeat(filled), colors.success);        // 100%+ = Green
} else if (percentage >= 75) {
  bar = c('█'.repeat(filled), colors.progress) + ...; // 75%+ = Cyan
} else if (percentage >= 50) {
  bar = c('█'.repeat(filled), colors.cyan) + ...;     // 50%+ = Cyan
} else {
  bar = c('█'.repeat(filled), colors.darkBlue) + ...; // 0-49% = Dark Blue
}
```

**To change thresholds or colors, edit this section.**

---

## 🧪 Testing Your Changes

After editing colors:

```bash
# Save the file
# Then test:
tt              # See your new colors in action
tt g            # Test goal-setting colors
tt l 10         # Test list colors
```

---

## 🔍 Finding the Perfect Color

### **Method 1: Terminal Color Chart**

Run this to see all 256 colors:

```bash
for i in {0..255}; do
  printf "\x1b[38;5;${i}mColor ${i}\x1b[0m\n"
done
```

### **Method 2: Online Tools**

- **256 Color Chart:** https://www.ditig.com/256-colors-cheat-sheet
- **Terminal Color Picker:** https://jonasjacek.github.io/colors/

### **Method 3: Quick Test**

Edit `tt` temporarily:
```javascript
green: '\x1b[38;5;46m',  // Try different numbers here
```

Then run `tt` to see the result. Repeat until you like it!

---

## 💾 Backup Before Editing

**Always backup before making changes:**

```bash
cd "/Users/mac/Documents/Terminal/Claude/Projects/Time Keeping"
cp tt tt.backup
```

**If you mess up, restore:**
```bash
cp tt.backup tt
```

---

## 🎨 Special Color: Comment Green

**The bright green used in code comments** (like `# Your new colorful status!`):

- **Code:** `42`
- **Full code:** `\x1b[38;5;42m`
- **Name:** Bright Green / Lime Green
- **RGB equivalent:** Approximately `#00D787`

This is the same green used for time durations in your tracker!

---

## 📝 Quick Reference Card

| Element | Current Color | Code | Easy to Change? |
|---------|---------------|------|-----------------|
| Time durations | Bright green | `42` | ✅ Line ~22 |
| Categories | Dark grey-blue | `67` | ✅ Line ~23 |
| Progress bars | Cyan/Green | `80`/`42` | ⚠️ Function ~46 |
| Percentages | Yellow | `226` | ✅ Line ~26 |
| Warnings | Orange | `214` | ✅ Line ~25 |
| Labels | Dark grey | `240` | ✅ Line ~27 |

---

## 🚀 Recommended Tweaks

### **For Better Readability:**
- Keep `grey` darker for contrast: `238` or `240`
- Keep `yellow` bright for numbers: `226` or `220`

### **For Personal Style:**
- Change `green` to your favorite color
- Change `darkBlue` to match
- Keep `orange` for warnings (good contrast)

### **For Consistency:**
- Use same color for `success` and `time`
- Use same color for `header` and `category`
- Keep `label` and `grey` the same

---

## 🎯 Pro Tips

1. **Test in your actual terminal** - Colors look different in different terminals
2. **Keep contrast high** - Dark colors for labels, bright for data
3. **Limit your palette** - 3-4 main colors max
4. **Save your theme** - Document your custom codes here!

---

## 📋 Your Custom Theme

**Document your changes here:**

```javascript
// MY CUSTOM THEME
// Date: _______
// Name: _______

const colors = {
  green: '\x1b[38;5;___m',       // Changed from 42 to ___
  darkBlue: '\x1b[38;5;___m',    // Changed from 67 to ___
  cyan: '\x1b[38;5;___m',        // Changed from 80 to ___
  orange: '\x1b[38;5;___m',      // Changed from 214 to ___
  yellow: '\x1b[38;5;___m',      // Changed from 226 to ___
  grey: '\x1b[38;5;___m',        // Changed from 240 to ___
};
```

---

**Location of this guide:**
`~/Documents/Terminal/Claude/Projects/Time Keeping/COLOR-GUIDE.md`

**Edit colors here:**
`~/Documents/Terminal/Claude/Projects/Time Keeping/tt` (lines 16-38)

**Quick test:**
```bash
tt
```

---

**Happy customizing!** 🎨✨
