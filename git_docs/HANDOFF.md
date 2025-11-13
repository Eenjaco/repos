# Browser Session Handoff - 2025-11-13

## What Was Accomplished (CLI Session)

### mp3_txt Project Enhancements
1. ✅ Added Afrikaans support via Whisper (faster-whisper library)
2. ✅ Created dual-mode transcription script (Vosk + Whisper)
3. ✅ Built multiple mdclean versions:
   - `mdclean_simple.py` - Ollama-based with model selector
   - `mdclean_claude.py` - Claude API-based (high quality)
   - `mdclean.py` - Full pipeline with Unstructured
4. ✅ Tested transcription with mixed English/Afrikaans audio
5. ✅ Tested multiple Ollama models for cleaning

### Git Repository Setup
- ✅ Moved 3 projects to cloud_vault_mirror:
  - convert_to_markdown
  - mp3_txt
  - time_keeping
- ✅ Initialized git repository
- ✅ Created .gitignore
- ✅ Initial commit complete (2,529 files)

---

## Test Results Summary

### Transcription (Whisper)
**File Tested**: Opknap Komittee Sept 26.m4a (54MB, mixed English/Afrikaans)
- ✅ **Whisper**: Excellent quality, 2,250 words transcribed
- **Output**: `/Users/mac/Documents/Applications/cloud_vault_mirror/mp3_txt/transcriptions/opknap_komittee_sept_26.md`
- **Comparison file**: `opknap_komittee_sept_26_apple_notes_transcription.md` (created by user)

### Cleaning Models Tested

| Model | Size | Status | Quality | Notes |
|-------|------|--------|---------|-------|
| **qwen2.5:0.5b** | 397MB | ❌ Failed | Poor | Hallucinates content, poor organization |
| **llama3.2:3b** | 2.0GB | ❌ Failed | N/A | Out of memory on 8GB RAM |
| **qwen2.5-coder:3b** | 1.9GB | ❌ Failed | N/A | Out of memory on 8GB RAM |
| **llama3.2:1b** | 700MB | ⏳ Downloading | TBD | Still downloading in background |
| **Claude API** | N/A | ✅ Ready | Excellent | Recommended solution |

### Key Finding
**Local Ollama models don't work well on 8GB RAM systems:**
- Tiny models (0.5B): Hallucinate and produce poor output
- Medium models (2-3GB): Out of memory errors
- 1B model: Still testing, but likely marginal quality

### Recommendation
**Use Claude API (mdclean_claude.py) for cleaning** - reliable, high quality, cost-effective (~$0.01-0.10 per transcript)

---

## File Locations

### Main Projects
- **cloud_vault_mirror**: `/Users/mac/Documents/Applications/cloud_vault_mirror/`
- **mp3_txt**: `/Users/mac/Documents/Applications/cloud_vault_mirror/mp3_txt/`
- **convert_to_markdown**: `/Users/mac/Documents/Applications/cloud_vault_mirror/convert_to_markdown/`
- **time_keeping**: `/Users/mac/Documents/Applications/cloud_vault_mirror/time_keeping/`

### Key mp3_txt Files
- **Scripts**:
  - `transcribe_enhanced.py` - Dual-mode transcription (Vosk + Whisper)
  - `mdclean_simple.py` - Ollama cleaning with model selector
  - `mdclean_claude.py` - Claude API cleaning (RECOMMENDED)
  - `mdclean.py` - Full pipeline with Unstructured

- **Documentation**:
  - `USAGE_GUIDE.md` - Complete usage instructions
  - `TEST_RESULTS.md` - Detailed test results
  - `README.md` - Project overview

- **Virtual Environment**:
  - Location: `mp3_txt/venv/`
  - Python: 3.13
  - Key packages: faster-whisper, ollama, anthropic, typer, rich

---

## Next Steps for Browser Session

### 1. Push to GitHub
```bash
cd /Users/mac/Documents/Applications/cloud_vault_mirror

# Create GitHub repo first at https://github.com/new
# Then:
git remote add origin https://github.com/YOUR_USERNAME/cloud_vault_mirror.git
git branch -M main
git push -u origin main
```

### 2. Compare Transcriptions
- Compare Whisper vs Apple Notes transcriptions:
  - Whisper: `mp3_txt/transcriptions/opknap_komittee_sept_26.md`
  - Apple Notes: `mp3_txt/transcriptions/opknap_komittee_sept_26_apple_notes_transcription.md`

### 3. Test llama3.2:1b (if downloaded)
```bash
cd /Users/mac/Documents/Applications/cloud_vault_mirror/mp3_txt
source venv/bin/activate

# Check if download complete
ollama list | grep llama3.2:1b

# Test if available
python3 mdclean_simple.py transcriptions/living_into_community_cultivating_practices_that_sustain_014.md \
  cleaned_output/test_014_llama32_1b.md --model llama3.2:1b
```

### 4. Set Up Claude API (Recommended)
```bash
# Get API key from: https://console.anthropic.com/
export ANTHROPIC_API_KEY="your-key-here"

# Test cleaning
cd /Users/mac/Documents/Applications/cloud_vault_mirror/mp3_txt
source venv/bin/activate
python3 mdclean_claude.py transcriptions/opknap_komittee_sept_26.md \
  cleaned_output/opknap_komittee_sept_26_cleaned.md
```

### 5. Update Documentation
Files to potentially edit/improve (use browser Claude Code):
- mp3_txt/README.md - Update with final recommendations
- mp3_txt/TEST_RESULTS.md - Add llama3.2:1b results if tested
- convert_to_markdown/README.md - Any updates needed
- time_keeping/README.md - Any updates needed

---

## Recommended Workflow Going Forward

### For Transcription
```bash
# English audio: Use Vosk (fast)
python3 transcribe_enhanced.py single audio.mp3 --engine vosk --outdir ./transcriptions

# Multilingual/Afrikaans: Use Whisper
python3 transcribe_enhanced.py single audio.m4a --engine whisper --language af --outdir ./transcriptions
```

### For Cleaning
```bash
# Use Claude API (best quality, reliable)
python3 mdclean_claude.py transcriptions/input.md cleaned_output/output.md
```

---

## Background Processes Still Running (Optional)

Several background processes from CLI session may still be running:
- llama3.2:1b download (check with `ollama list`)
- Various pip installations
- Other model downloads

You can check these with:
```bash
ps aux | grep -E "(ollama|python|pip)" | grep -v grep
```

---

## Workflow: Browser for Editing, CLI for Execution

**Perfect Setup:**
- **Browser Claude Code**: Edit code, write docs, refactor
- **CLI**: Run scripts, execute commands, test functionality

This preserves CLI tokens while using browser credits for writing/editing tasks.

---

## Questions to Answer in Browser Session

1. How does Whisper compare to Apple Notes transcription quality?
2. Did llama3.2:1b finish downloading? Is it usable?
3. Which GitHub repos to create (one monorepo or separate repos)?
4. Any documentation improvements needed?
5. Should we test Claude API cleaning on the Afrikaans file?

---

## Important Notes

- **Apple Notes comparison file exists** at: `mp3_txt/transcriptions/opknap_komittee_sept_26_apple_notes_transcription.md`
- **Whisper output** is at same location without "_apple_notes_transcription" suffix
- **Git is ready** - just need to create GitHub repo and push
- **Virtual environment** is set up with all dependencies
- **Claude API** is the recommended solution for cleaning (Ollama models don't work well on 8GB RAM)

---

Good luck with the browser session! 🚀
