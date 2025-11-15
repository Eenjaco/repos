
---

Understood — I'll provide a compact, compatible Bash script that speaks the same "tt" language and workflow. It:

- Uses the same weekly file scheme (ISO week YYYY-Www.md) and the same section formatting you showed.
- Can be called as a tiny helper CLI (e.g., tt-local s / tt-local e) so it fits alongside your tt tool.
- Writes to your project's shared folder (default points at your Time Keeping folder; pass a different path as first arg).
- Persists an in-progress state file (so start/stop works across sessions/Shortcuts/SSH).
- Produces the exact text block format you use (———, Title, optional subtitle, Start time, until, End Time).

Save as tt-local (make executable) and place in your Time Keeping folder or call from Shortcuts.

Script (copy to tt-local):
```bash
#!/usr/bin/env bash
# tt-local: tiny start/stop helper that appends to weekly .md files (ISO week)
# Usage:
#   tt-local s [path-to-time-keeping-folder]
#   tt-local e [path-to-time-keeping-folder]

ACTION="$1"                # s or e
BASE_DIR="${2:-$HOME/Time Keeping}"   # default project folder; pass custom as arg
mkdir -p "$BASE_DIR"

WEEK_FILE="$BASE_DIR/$(date -u +%G-W%V).md"
STATE_FILE="$BASE_DIR/.tt_local_state"

timestamp(){ date +"%d %b %Y at %H:%M:%S"; }

start_cmd(){
  if [ -f "$STATE_FILE" ]; then
    echo "A timer is already running. Stop it first with: tt-local e"
    exit 1
  fi
  read -r -p "Title: " TITLE
  read -r -p "Subtitle (optional): " SUB
  START="$(timestamp)"
  printf "%s\n%s\n%s\n" "$TITLE" "$SUB" "$START" > "$STATE_FILE"
  echo "Started: $TITLE — $START"
}

end_cmd(){
  if [ ! -f "$STATE_FILE" ]; then
    echo "No running timer found."
    exit 1
  fi
  IFS=$'\n' read -r TITLE SUB START < "$STATE_FILE"
  END="$(timestamp)"
  {
    echo "———"
    echo "$TITLE"
    [ -n "$SUB" ] && echo "$SUB"
    echo "Start time: $START"
    echo "until"
    echo "End Time: $END"
  } >> "$WEEK_FILE"
  rm -f "$STATE_FILE"
  echo "Stopped: $TITLE — $END"
  echo "Appended to: $WEEK_FILE"
}

case "$ACTION" in
  s) start_cmd ;;
  e) end_cmd ;;
  *) echo "Usage: $0 s|e [path-to-time-keeping-folder]" ; exit 1 ;;
esac
```

Quick integration notes:
- To mimic your tt UX, install it as an executable named tt-local or add an alias (e.g., alias ttl='/path/to/tt-local').
- From Shortcuts, run: /path/to/tt-local s "/path/to/Time Keeping" and later /path/to/tt-local e "/path/to/Time Keeping".
- Change BASE_DIR default to your actual repository path (e.g., "/Users/mac/.../Time Keeping") if desired.

If you want I can:
- add automatic duration calculation,
- write entries into the SQLite DB instead of Markdown,
- or make it a tiny Node CLI to match your project's stack. Which would you like?

---


to make sure, i would also need a script to add to apple shortcuts:


Below are two minimal pieces you can plug into Shortcuts:

1) A tiny shell helper (tt-local) — same as before but tuned for being run from Shortcuts (no interactive prompts; accepts Title and Subtitle as arguments). Place this in your Time Keeping folder and make executable.

Save as tt-local:
```bash
#!/usr/bin/env bash
# tt-local: noninteractive start/stop helper for Shortcuts
# Usage from Shortcuts (Run Shell Script):
#   /path/to/tt-local s "Title" "Subtitle" "/path/to/Time Keeping"
#   /path/to/tt-local e "/path/to/Time Keeping"

CMD="$1"           # s or e
ARG1="$2"          # Title (on start)
ARG2="$3"          # Subtitle (on start)
BASE_DIR="${4:-$HOME/Time Keeping}"

mkdir -p "$BASE_DIR"
WEEK_FILE="$BASE_DIR/$(date -u +%G-W%V).md"
STATE_FILE="$BASE_DIR/.tt_local_state"
timestamp(){ date +"%d %b %Y at %H:%M:%S"; }

start_cmd(){
  if [ -f "$STATE_FILE" ]; then
    printf "ERROR: timer already running\n"
    exit 1
  fi
  TITLE="${ARG1:-Untitled}"
  SUB="${ARG2:-}"
  START="$(timestamp)"
  printf "%s\n%s\n%s\n" "$TITLE" "$SUB" "$START" > "$STATE_FILE"
  printf "Started: %s — %s\n" "$TITLE" "$START"
}

end_cmd(){
  if [ ! -f "$STATE_FILE" ]; then
    printf "ERROR: no running timer\n"
    exit 1
  fi
  IFS=$'\n' read -r TITLE SUB START < "$STATE_FILE"
  END="$(timestamp)"
  {
    echo "———"
    echo "$TITLE"
    [ -n "$SUB" ] && echo "$SUB"
    echo "Start time: $START"
    echo "until"
    echo "End Time: $END"
  } >> "$WEEK_FILE"
  rm -f "$STATE_FILE"
  printf "Stopped: %s — %s\nAppended to: %s\n" "$TITLE" "$END" "$WEEK_FILE"
}

case "$CMD" in
  s) start_cmd ;;
  e) end_cmd ;;
  *) printf "Usage: %s s \"Title\" \"Subtitle\" [base-dir]  OR  %s e [base-dir]\n" "$0" "$0"; exit 1 ;;
esac
```

Make it executable:
chmod +x /path/to/tt-local

2) A Shortcuts setup (steps) — how to call tt-local noninteractively
- Action 1: "Run Shell Script" (Shell: /bin/zsh or /bin/bash)
  - Pass input: "as arguments" (not needed here)
  - Script body examples:

Start action (use Shortcut input or provide text fields):
/path/to/tt-local s "Emails and whatsapp" "Admin" "/Users/mac/Documents/Terminal/Claude/Projects/Time Keeping"

End action:
/path/to/tt-local e "/Users/mac/Documents/Terminal/Claude/Projects/Time Keeping"

- If you want to prompt in Shortcuts for the Title/subtitle:
  - Action before Run Shell Script: "Ask for Input" (Text) -> use as Variable Title
  - Optional: second "Ask for Input" for Subtitle
  - In Run Shell Script, build command using those variables, e.g.:
/path/to/tt-local s "[Title]" "[Subtitle]" "/path/to/Time Keeping"

Notes / tips
- Shortcuts' Run Shell Script runs with a minimal PATH; use absolute paths for tt-local and any binaries.
- If running on Mac and calling from iOS via SSH or Shortcuts remote, ensure the BASE_DIR is the shared-drive path (Dropbox/iCloud Drive path as mounted on your Mac).
- The script returns plain text (stdout) — Shortcuts will capture and can show a notification or Quick Look.
- If you want confirmations, add "Show Result" or "Notification" actions after the Run Shell Script.

If you want, I can:
- supply a ready .shortcut export (JSON) that implements Ask for Input → Run Shell Script → Show Notification, or
- add duration calculation into the Markdown entry. Which do you prefer?