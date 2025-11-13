# Session Management Scripts

Standalone shell scripts that use your **local Ollama LLM** (llama3.2:1b) to help manage git sessions in any terminal window - **no Claude Code required!**

## Scripts

### `session_end` - Smart Session Close
Analyzes your changes and generates commit messages using Ollama.

**Features**:
- 🤖 AI-generated commit messages from git diff
- 📝 Reviews all changes before committing
- ✏️ Option to edit or reject AI suggestion
- 🚀 Optional push to remote
- 📊 Shows recent commits

**Usage**:
```bash
# In any git repo
session_end
```

**Example**:
```
📊 Session End

📝 Analyzing changes...

Changes detected:
M  aster.py
A  docs/VOSK_SETUP.md

🤖 Generating commit message with llama3.2:1b...

Generated commit message:
---
Add Vosk audio transcription

- Implement speech recognition
- Add setup documentation
---

Use this message? [Y/n/e(dit)] y

✅ Committed
Push to remote? [Y/n] y
✅ Pushed to origin/main

✨ Session closed!
```

---

### `session_start` - Smart Session Start
Summarizes recent work and suggests next steps using Ollama.

**Features**:
- 📡 Checks if branch is up to date
- 📝 Summarizes recent commits
- 🎯 Suggests next priorities
- 📋 Shows pending tasks from SESSION_NOTES.md
- ⚠️ Warns about uncommitted changes

**Usage**:
```bash
# In any git repo
session_start
```

**Example**:
```
🚀 Session Start

📁 Repository: aster
🌿 Branch: main

📝 Recent Activity

a60bd7f Add session management commands
bb4e8fa Add implementation guide
cd9bb1c Add Vosk model setup docs

🤖 Generating session briefing with llama3.2:1b...

## Recent Work
- Implemented audio transcription with Vosk
- Added comprehensive documentation
- Created session management tools

## Suggested Next Steps
1. Test audio transcription on training data
2. Review and optimize batch processing
3. Consider implementing inbox watcher

⏳ Pending from last session:
  • Rename inbox watcher to "Aster Gazer"
  • Add audio priority queue

✨ Ready to work!
```

---

## Installation

### Quick Install
```bash
cd ~/Documents/Applications/repos/aster
./bin/install_session_commands.sh
```

This will:
1. Make scripts executable
2. Create symlinks in `~/bin/`
3. Check if Ollama and llama3.2:1b are available
4. Verify PATH setup

### Manual Install
```bash
# Make executable
chmod +x bin/session_end.sh
chmod +x bin/session_start.sh

# Add to PATH
mkdir -p ~/bin
ln -sf $(pwd)/bin/session_end.sh ~/bin/session_end
ln -sf $(pwd)/bin/session_start.sh ~/bin/session_start

# Add ~/bin to PATH (if not already)
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

---

## Requirements

### Ollama + llama3.2:1b
```bash
# Install Ollama (if not already installed)
# macOS: brew install ollama
# Linux: curl -fsSL https://ollama.com/install.sh | sh

# Pull the model
ollama pull llama3.2:1b
```

### Git
Already installed ✓

---

## How It Works

### session_end
1. Checks for uncommitted changes
2. Collects `git status` and `git diff`
3. Sends to Ollama with prompt to generate commit message
4. Presents message for review (can edit or reject)
5. Commits and optionally pushes

### session_start
1. Checks current branch and remote status
2. Fetches recent commits
3. Sends commit history to Ollama
4. Gets AI summary of recent work + suggested next steps
5. Shows pending tasks from SESSION_NOTES.md

---

## Use Cases

### Scenario 1: Quick File Cleanup
```bash
# You're in a terminal, unzipped some files, organized folders
cd my-project
# ...made changes...

session_end
# AI generates: "Organize project files and add documentation"
# Commits and pushes automatically
```

### Scenario 2: Resuming Work
```bash
# Morning terminal, forgot what you were doing
cd my-project
session_start

# Shows:
# - Recent commits summary
# - Suggested next steps
# - Pending tasks
```

### Scenario 3: Multiple Terminals
```bash
# Terminal 1: coding
# Terminal 2: installing dependencies
# Terminal 3: organizing files

# In each terminal when done:
session_end
```

---

## Difference from Claude Code Commands

| Feature | Shell Scripts (`session_end`) | Claude Code (`/session_end`) |
|---------|-------------------------------|------------------------------|
| **Works in any terminal** | ✅ Yes | ❌ No (only in Claude Code) |
| **Requires Claude Code** | ❌ No | ✅ Yes |
| **Uses local LLM** | ✅ Yes (Ollama) | ❌ No (uses Claude) |
| **Offline capable** | ✅ Yes | ❌ No |
| **Auto commit messages** | ✅ Yes | ✅ Yes |
| **Session documentation** | ⚠️ Basic | ✅ Comprehensive |
| **Code analysis** | ⚠️ Limited | ✅ Deep |

**Recommendation**:
- Use **shell scripts** for quick terminal work
- Use **Claude Code commands** for detailed session documentation

---

## Customization

### Change LLM Model
Edit scripts and replace `llama3.2:1b` with your preferred model:
```bash
# Use larger model for better messages
ollama run llama3.1:8b

# Or use different model
ollama run mistral
```

### Customize Prompts
Edit the `PROMPT` variable in each script to adjust:
- Commit message style
- Summary format
- Level of detail

### Add Aliases
```bash
# Add to ~/.zshrc
alias se="session_end"
alias ss="session_start"
```

---

## Troubleshooting

### "ollama: command not found"
Install Ollama:
```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh
```

### "llama3.2:1b not found"
Pull the model:
```bash
ollama pull llama3.2:1b
```

### "~/bin not in PATH"
Add to your shell config:
```bash
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### AI suggestions are poor
- Try a larger model: `llama3.1:8b`
- Edit the prompt in the script
- Use the edit option to refine messages

---

## Tips

1. **Review before committing**: Always read the AI-generated message
2. **Edit when needed**: Press `e` to edit the message
3. **Keep commits focused**: Run `session_end` frequently for smaller commits
4. **Check session notes**: `session_start` reads SESSION_NOTES.md
5. **Use in any repo**: These scripts work in all git repositories

---

## What's Next?

See `SESSION_NOTES.md` for:
- Recent accomplishments
- Pending ideas
- Next priorities

Type `session_start` to get a fresh briefing!
