# Workspace-Wide Claude Commands

These slash commands are available in **all repositories** within this workspace.

## Available Commands

### `/session_end`
Close current session with proper cleanup:
- Check git status
- Commit outstanding changes
- Create session summary
- Document pending ideas
- Verify everything pushed
- Generate status report

**Usage**: Type `/session_end` at the end of your work session

---

### `/session_start`
Start new session with context:
- Review recent commits
- Summarize recent work
- List pending tasks
- Check environment
- Present session briefing
- Suggest next priorities

**Usage**: Type `/session_start` at the beginning of your work session

---

## How It Works

Slash commands in `.claude/commands/` are workspace-wide and available in:
- `/home/user/repos/aster`
- `/home/user/repos/mp3_txt`
- `/home/user/repos/cloud_vault_mirror`
- `/home/user/repos/mdcon`
- `/home/user/repos/strudelscore`
- Any other repo in this workspace

Each command is a markdown file that defines the prompt for Claude to execute.

## Creating New Commands

To add a new workspace-wide command:

1. Create `[command-name].md` in this directory
2. Add description in frontmatter:
   ```markdown
   ---
   description: Brief description of what command does
   ---

   Your prompt instructions here...
   ```
3. Use it with `/command-name`

## Local Commands

To create repo-specific commands, add them to:
```
/path/to/repo/.claude/commands/[command-name].md
```

These will only be available in that specific repository.
