---
description: Close current session with git commits, documentation, and status summary
---

Execute session closeout procedures:

1. **Git Status Check**:
   - Run `git status` to check working tree
   - List any uncommitted changes
   - Show last 5 commits with `git log --oneline -5`

2. **Commit Outstanding Changes** (if any):
   - Stage all relevant changes
   - Create meaningful commit message summarizing work
   - Push to remote branch

3. **Create Session Summary**:
   - Current date and time
   - Branch name
   - What was accomplished (list key features/fixes)
   - Files created or modified
   - Commits made (with hashes)
   - Documentation added
   - **Ideas mentioned but NOT implemented yet** (important for next session)
   - Next steps/pending tasks

4. **Verify Everything**:
   - All commits pushed to remote
   - Working tree clean
   - Documentation files present
   - Key implementation files verified

5. **Generate Status Report**:
   - Create a concise checklist-style summary
   - Mark completed items with ✅
   - Mark pending items with ⏳
   - Note any blockers or issues

6. **Save Session Notes**:
   - Offer to create/update SESSION_NOTES.md with:
     - Session date
     - Summary of work
     - Pending ideas
     - Next session priorities

Present the final status report to the user in a clean, organized format.
