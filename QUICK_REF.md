# 🚀 Quick Reference Card

## System
- **Python**: Use 3.13 (NOT 3.14!)
- **Location**: `~/Documents/Applications/repos/`
- **Colors**: Green #42, Grey #240

## Start Any Project
```bash
cd ~/Documents/Applications/repos/project_name
source venv/bin/activate
python --version  # Check it's 3.13!
```

## Create Files (Mac-Friendly)
```bash
# Method 1: Python (BEST)
python3 << 'EOF'
with open('file.txt', 'w') as f:
    f.write('content')
EOF

# Method 2: Direct echo
echo "content" > file.txt
```

## Fix Python Version Issues
```bash
deactivate
rm -rf venv
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Current Projects
- `strudel_sheet` - Music analysis
- `mp3_txt` - Transcription
- `convert_to_markdown` - PDF tools
- `time_keeping` - Time tracking

## Communication Style
✅ One command at a time
✅ Show expected output
✅ Step-by-step
❌ No vim/heredocs/complex syntax

See `.WORKSPACE_GUIDE.md` for full details!
