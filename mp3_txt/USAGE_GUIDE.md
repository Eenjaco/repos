# mp3_txt Enhanced - Usage Guide

## 🎯 Overview

You now have a complete transcription and cleaning pipeline with multiple options:

### Tools Available:
1. **transcribe_enhanced.py** - Dual-engine transcription (Vosk + Whisper)
2. **mdclean_simple.py** - Ollama-based transcript cleaning (flexible model choice)
3. **mdclean_claude.py** - Claude API-based cleaning (highest quality)
4. **mdclean.py** - Full pipeline with Unstructured + Ollama

---

## 📝 Transcription

### Using Whisper (Multilingual, including Afrikaans)

```bash
# Auto-detect language
python3 transcribe_enhanced.py single audio.m4a --engine whisper --outdir ./out

# Specify language explicitly
python3 transcribe_enhanced.py single audio.m4a --engine whisper --language af --outdir ./out

# Use smaller/faster model
python3 transcribe_enhanced.py single audio.m4a --engine whisper --model tiny --outdir ./out

# Batch processing
python3 transcribe_enhanced.py batch ./audio_folder --engine whisper --outdir ./out
```

### Using Vosk (English only, faster)

```bash
# Single file
python3 transcribe_enhanced.py single audio.mp3 --engine vosk --outdir ./out

# Batch
python3 transcribe_enhanced.py batch ./audio_folder --engine vosk --outdir ./out
```

### Model Sizes (Whisper)
- **tiny**: Fast, lower accuracy
- **base**: Good balance (default)
- **small**: Better accuracy, slower
- **medium**: High accuracy, slow
- **large**: Best accuracy, very slow

---

## 🧹 Transcript Cleaning

### Option A: Ollama (Local, Free)

**List available models:**
```bash
python3 mdclean_simple.py --list-models
```

**Available models on your system:**
- **qwen2.5:0.5b** (397MB) ✅ Best for 8GB RAM
- llama3.2:3b (2.0GB) ⚠️ May fail on 8GB RAM
- qwen2.5-coder:3b (1.9GB) ⚠️ May fail on 8GB RAM
- qwen2.5-coder:7b (4.7GB) ❌ Too large for 8GB RAM

**Auto-select best model:**
```bash
python3 mdclean_simple.py input.md output.md
```

**Specify model explicitly:**
```bash
python3 mdclean_simple.py input.md output.md --model qwen2.5:0.5b
```

### Option B: Claude API (Highest Quality)

**Setup:**
```bash
# Set API key
export ANTHROPIC_API_KEY="sk-ant-..."

# Or pass directly
python3 mdclean_claude.py input.md output.md --api-key "sk-ant-..."
```

**Usage:**
```bash
python3 mdclean_claude.py input.md output.md
```

**Cost:** ~$0.01-0.10 per transcript (Claude 3.5 Haiku)

### Option C: Full Pipeline (Unstructured + Ollama)

**Fast mode (structure only, no LLM):**
```bash
python3 mdclean.py input.md output.md --mode fast
```

**Quality mode (structure + LLM polish):**
```bash
python3 mdclean.py input.md output.md --mode quality
```

---

## 💡 Recommended Workflow

### For English audio:
```bash
# 1. Transcribe with Vosk (fast)
python3 transcribe_enhanced.py single audio.mp3 --engine vosk --outdir ./raw

# 2. Clean with Ollama tiny model (when no other apps running)
python3 mdclean_simple.py raw/audio.md clean/audio.md

# OR use Claude API for best quality
python3 mdclean_claude.py raw/audio.md clean/audio.md
```

### For Afrikaans/multilingual audio:
```bash
# 1. Transcribe with Whisper
python3 transcribe_enhanced.py single audio.m4a --engine whisper --language af --outdir ./raw

# 2. Clean with Claude API (best for non-English)
python3 mdclean_claude.py raw/audio.md clean/audio.md
```

### For best Ollama results:
1. Close all other applications
2. Make sure only Ollama server + transcribe script are running
3. Use qwen2.5:0.5b model (397MB)
4. Process one file at a time

---

## 🔧 Tips & Tricks

### RAM Management
- **Current RAM:** 8GB
- **qwen2.5:0.5b works:** 397MB model
- **Larger models fail:** Close background apps first
- **Monitor with:** `ps aux | grep ollama`

### Comparing Model Quality
Test multiple models on same file:
```bash
# Test tiny model
python3 mdclean_simple.py input.md output_tiny.md --model qwen2.5:0.5b

# Test medium model (close other apps first!)
python3 mdclean_simple.py input.md output_medium.md --model llama3.2:3b

# Test Claude API
python3 mdclean_claude.py input.md output_claude.md
```

Compare the outputs to find best quality/speed trade-off.

### Whisper Language Codes
- `en` - English
- `af` - Afrikaans
- `nl` - Dutch
- `de` - German
- `fr` - French
- `es` - Spanish
- *(Leave blank for auto-detection)*

---

## 📊 Quality Comparison

| Tool | Speed | Quality | Cost | RAM | Offline |
|------|-------|---------|------|-----|---------|
| Vosk | Fast | Good | Free | Low | Yes |
| Whisper | Medium | Excellent | Free | Medium | Yes |
| Ollama (tiny) | Medium | Fair | Free | ~400MB | Yes |
| Ollama (3B) | Slow | Good | Free | ~2GB | Yes |
| Claude API | Fast | Excellent | $0.01-0.10 | Minimal | No |

---

## 🚀 Quick Start Examples

### Example 1: Simple English transcript
```bash
# One command, auto-selects best model
python3 mdclean_simple.py transcription.md cleaned.md
```

### Example 2: Afrikaans audio file
```bash
# Transcribe
python3 transcribe_enhanced.py single "Opknap Komittee Sept 26.m4a" \\
  --engine whisper --language af --outdir ./out

# Clean
python3 mdclean_claude.py out/opknap_komittee_sept_26.md cleaned.md
```

### Example 3: Batch English files
```bash
# Transcribe all
python3 transcribe_enhanced.py batch ./audio_files \\
  --engine vosk --outdir ./transcriptions

# Clean all
for file in transcriptions/*.md; do
  python3 mdclean_simple.py "$file" "cleaned/$(basename $file)"
done
```

---

## 🐛 Troubleshooting

### "Model requires more system memory"
- Close other applications
- Use qwen2.5:0.5b instead
- Or use Claude API version

### "No module named 'anthropic'"
```bash
source venv/bin/activate
pip install anthropic
```

### "No module named 'faster_whisper'"
Already installed in your venv!

### Whisper is slow
- Use `--model tiny` for faster processing
- Or use Vosk for English audio (much faster)

---

## 📁 File Locations

- **transcribe_enhanced.py** - `/Users/mac/Documents/Applications/mp3_txt/transcribe_enhanced.py`
- **mdclean_simple.py** - `/Users/mac/Documents/Applications/mp3_txt/mdclean_simple.py`
- **mdclean_claude.py** - `/Users/mac/Documents/Applications/mp3_txt/mdclean_claude.py`
- **mdclean.py** - `/Users/mac/Documents/Applications/mp3_txt/mdclean.py`
- **venv** - `/Users/mac/Documents/Applications/mp3_txt/venv/`

Activate venv: `source venv/bin/activate`
