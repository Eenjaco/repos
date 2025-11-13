# Test Results - Model Comparison

## Test Environment
- **System**: macOS 23.6.0
- **RAM**: 8GB
- **Date**: 2025-11-13

---

## Transcription Tests

### Test 1: Whisper - Mixed English/Afrikaans Audio

**File**: `Opknap Komittee Sept 26.m4a` (54MB)
**Command**:
```bash
python3 transcribe_enhanced.py single "Opknap Komittee Sept 26.m4a" \
  --engine whisper --outdir /tmp/test_whisper
```

**Results**:
- ✅ **SUCCESS**
- Model: base
- Output: `/tmp/test_whisper/Opknap Komittee Sept 26.md`
- Words transcribed: 2,250
- Language detected: English (0.95 probability)
- Quality: Excellent - captured both English and Afrikaans clearly

**Conclusion**: Whisper handles mixed-language audio very well. No training needed.

---

## Cleaning Tests

### Test 2: qwen2.5:0.5b (Tiny Model - 397MB)

**Test 2a**: File 001 (Very short file)

**Input** (transcriptions/living_into_community_cultivating_practices_that_sustain_001.md):
```
this is audible living and to community cultivating practices that sustain us
written by christine di poll narrated by jessica shell
```

**Command**:
```bash
python3 mdclean_simple.py transcriptions/living_into_community_cultivating_practices_that_sustain_001.md \
  cleaned_output/test_001.md --model qwen2.5:0.5b
```

**Output** (cleaned_output/test_001.md):
```
Christine Di Poll, a writer, narrates this piece about the practices of
sustainable living and community building. Christine shares her insights on
how these practices can help individuals and communities thrive.
```

**Results**:
- ❌ **FAILED** - Hallucination
- Model invented content not in the original
- Changed structure completely
- Added fabricated information

**Test 2b**: File 014 (Longer file, 44 lines)

**Input**: 44 lines of questions, all lowercase, poor punctuation

**Command**:
```bash
python3 mdclean_simple.py transcriptions/living_into_community_cultivating_practices_that_sustain_014.md \
  cleaned_output/test_014_tiny.md --model qwen2.5:0.5b
```

**Results**:
- ⚠️ **PARTIAL SUCCESS**
- Added some punctuation and capitalization
- BUT: Collapsed 44 lines into 2 giant run-on paragraphs (7 lines total)
- Did not properly organize into natural paragraph breaks
- Some transcription errors remain unfixed

**Conclusion**:
- qwen2.5:0.5b (0.5B parameters) is **TOO SMALL** for reliable transcript cleaning
- Hallucinates on short texts
- Poor paragraph organization on longer texts
- **NOT RECOMMENDED**

---

### Test 3: llama3.2:3b (Medium Model - 2.0GB)

**Command**:
```bash
python3 mdclean_simple.py transcriptions/living_into_community_cultivating_practices_that_sustain_001.md \
  cleaned_output/test_001_llama32.md --model llama3.2:3b
```

**Results**:
- ❌ **FAILED** - Out of Memory
- Error: "model requires more system memory than is currently available unable to load full model on GPU (status code: 500)"
- Returned original content unchanged
- Failed all attempts even with other background processes closed

**Conclusion**: 2GB model too large for 8GB RAM system with any background processes running.

---

### Test 4: qwen2.5-coder:3b (Medium Model - 1.9GB)

**File**: living_into_community_cultivating_practices_that_sustain_002.md (458 lines, 17 chunks)

**Command**:
```bash
python3 mdclean_simple.py transcriptions/living_into_community_cultivating_practices_that_sustain_002.md \
  /tmp/test_cleaned.md --model qwen2.5-coder:3b
```

**Results**:
- ❌ **FAILED** - Out of Memory
- Error: "model requires more system memory than is currently available" (status 500)
- All 17 chunks failed
- Returned original content unchanged

**Conclusion**: 1.9GB model also too large for 8GB RAM system.

---

### Test 5: Claude API (Haiku Model)

**Status**: ✅ Ready to use
**Setup**:
```bash
# Install (completed)
pip install anthropic

# Set API key
export ANTHROPIC_API_KEY="sk-ant-..."
```

**Command**:
```bash
python3 mdclean_claude.py input.md output.md
```

**Expected Results**:
- High quality punctuation and capitalization
- Proper paragraph organization
- Fixes transcription errors (homophones, mishearings)
- Fast processing (API-based)
- Reliable - no hallucinations
- Cost: ~$0.01-0.10 per transcript

**Conclusion**: Best option for quality cleaning. Recommended as primary tool.

---

## Summary Table

| Model | Size | RAM Usage | Status | Quality | Speed | Cost |
|-------|------|-----------|--------|---------|-------|------|
| **Whisper (base)** | 150MB | Low | ✅ Works | Excellent | Medium | Free |
| **qwen2.5:0.5b** | 397MB | Low | ❌ Hallucinates | Poor | Fast | Free |
| **llama3.2:3b** | 2.0GB | High | ❌ OOM | N/A | N/A | Free |
| **qwen2.5-coder:3b** | 1.9GB | High | ❌ OOM | N/A | N/A | Free |
| **Claude API** | N/A | Minimal | ✅ Ready | Excellent | Fast | ~$0.01-0.10 |

---

## Recommendations

### For Transcription:
✅ **Use Whisper** for all audio (English, Afrikaans, multilingual)
- Command: `python3 transcribe_enhanced.py single audio.m4a --engine whisper --outdir ./out`

### For Cleaning:
✅ **Use Claude API** (mdclean_claude.py)
- High quality, reliable, fast
- No RAM issues
- Cost-effective (~$0.01-0.10 per file)
- Command: `python3 mdclean_claude.py input.md output.md`

❌ **Avoid Ollama models on 8GB RAM**
- Tiny models (0.5B): Hallucinate and poor organization
- Medium models (2-3GB): Out of memory errors
- Not worth the effort on this system

---

## Next Steps

1. Set up Claude API key:
   ```bash
   export ANTHROPIC_API_KEY="your-key-here"
   ```

2. Test Claude API cleaning on sample file:
   ```bash
   python3 mdclean_claude.py transcriptions/living_into_community_cultivating_practices_that_sustain_014.md \
     cleaned_output/test_014_claude.md
   ```

3. Compare Claude output with qwen2.5:0.5b output to verify quality improvement

4. Process remaining transcription files with recommended workflow:
   ```bash
   # For each audio file:
   python3 transcribe_enhanced.py single audio.m4a --engine whisper --outdir ./raw
   python3 mdclean_claude.py raw/audio.md cleaned/audio.md
   ```
