#!/usr/bin/env bash
# Setup script for Aster Inbox Watcher

set -e

echo "📦 Setting up Aster Inbox Watcher..."
echo ""

# Install watchdog if needed
echo "→ Installing Python dependencies..."
pip install watchdog

# Create iCloud Drive folder structure
echo "→ Creating iCloud Drive folders..."

ICLOUD_BASE="$HOME/Library/Mobile Documents/com~apple~CloudDocs"
ASTER_FOLDER="$ICLOUD_BASE/Aster"

mkdir -p "$ASTER_FOLDER/inbox"
mkdir -p "$ASTER_FOLDER/processing"
mkdir -p "$ASTER_FOLDER/processed"
mkdir -p "$ASTER_FOLDER/failed"
mkdir -p "$ASTER_FOLDER/.aster-watcher"
mkdir -p "$ASTER_FOLDER/.aster-watcher/logs"

# Create README in iCloud folder
cat > "$ASTER_FOLDER/README.md" << 'EOF'
# Aster Inbox

Drop files here from your iPhone to automatically process them!

## 📁 Folders

- **inbox/** - Drop files here (will be processed automatically)
- **processing/** - Files currently being processed
- **processed/** - Archive of processed originals
- **failed/** - Files that failed processing

## 📱 From iPhone

1. Take photo or save file
2. Share → Save to Files → Aster → inbox
3. Wait ~2-5 minutes
4. Open Obsidian → See processed markdown in Inbox/

## 🎯 Priority System

Name your files with prefixes for priority:

- **urgent_** - Process immediately
- **receipt_** - Process immediately (receipts)
- **meeting_** - High priority (within 5 min)
- **whiteboard_** - High priority
- **book_** - Low priority (overnight)
- **archive_** - Low priority
- **newsletter_** - Batch (scheduled time)

Examples:
- `urgent_meeting_notes.jpg` → Processed immediately
- `receipt_starbucks.jpg` → Processed immediately
- `book_chapter3.pdf` → Processed overnight

## ⚙️ Advanced

Edit `queue.md` to configure custom priorities and see processing status.

## 🔍 Troubleshooting

If files aren't processing:
1. Check if watcher is running: `./aster_watcher.py status`
2. View logs: `tail -f .aster-watcher/watcher.log`
3. Restart watcher: `./aster_watcher.py stop && ./aster_watcher.py run`

EOF

# Create empty queue.md
cat > "$ASTER_FOLDER/inbox/queue.md" << 'EOF'
# Aster Processing Queue

## Status
- **Watching**: ⏸️ Not started yet
- **Last Check**: Never
- **Queue Size**: 0 files

## How to Use

### From iPhone
1. Take photo / save file
2. Share to Files → Aster → inbox
3. File processes automatically
4. Result appears in Obsidian

### Priority Naming
- `urgent_*` - Process immediately
- `receipt_*` - Process immediately
- `meeting_*` - High priority
- `book_*` - Low priority (overnight)

## Current Queue

| File | Priority | Status | Time |
|------|----------|--------|------|
| (empty) | - | - | - |

## Completed Today

(none yet)

## Start the Watcher

Run on your Mac:
```bash
cd ~/Documents/Applications/repos/aster
./aster_watcher.py run
```
EOF

# Make watcher executable
chmod +x aster_watcher.py

# Check Obsidian vault location
OBSIDIAN_VAULT="$HOME/Library/Mobile Documents/iCloud~md~obsidian"
if [ ! -d "$OBSIDIAN_VAULT" ]; then
    echo ""
    echo "⚠️  Warning: Obsidian vault not found at:"
    echo "   $OBSIDIAN_VAULT"
    echo ""
    echo "Please update the VAULT path in aster_watcher.py to match your vault location."
    echo ""
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📁 Inbox folder created at:"
echo "   $ASTER_FOLDER/inbox"
echo ""
echo "🚀 Start the watcher:"
echo "   ./aster_watcher.py run"
echo ""
echo "📱 From iPhone:"
echo "   1. Open Files app"
echo "   2. Go to iCloud Drive → Aster → inbox"
echo "   3. Add to Favorites for quick access"
echo "   4. Drop files to process!"
echo ""
echo "📖 See docs/INBOX_WATCHER_DESIGN.md for full documentation"
echo ""
