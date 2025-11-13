# mdclean Enhancement Pitch - Post-Transcription Cleanup

**Created:** 2025-11-12
**Status:** Proposal for future implementation
**Context:** After audio transcription with mp3_txt/Vosk, raw transcriptions need cleaning

---

## Use Case

**Problem:** Vosk transcription output is functional but has quality issues:
- No punctuation or capitalization
- Run-on sentences without paragraph breaks
- Transcription errors (homophones, mishearings)
- No structural formatting (quotes, lists, emphasis)
- Poor readability for knowledge base integration

**Solution:** Enhance `mdclean` to process raw transcriptions into clean, readable markdown suitable for Zettelkasten/knowledge base work.

**Integration Point:** Add mdclean as optional post-processing step in `transcribe` CLI workflow:
```
Audio → Vosk transcription → [Optional: mdclean] → Final markdown
```

---

## Primary Approach: Unstructured

**Does it require API?**
- **No** - Unstructured is open-source Python library that runs 100% locally
- **Optional:** They offer SaaS API for advanced features (chunking, embeddings, table enrichment)
- For our use case (text cleanup), local installation is sufficient - no API needed

**Why Unstructured:**
- Handles multiple document types (PDF, DOCX, HTML, TXT, MD, PPT)
- Extracts structure from plain text: titles, paragraphs, lists, tables, narrative text
- Built specifically for LLM preprocessing pipelines (perfect for our use case!)
- Can partition text into semantic elements (NarrativeText, Title, ListItem)
- Active development, excellent documentation
- **Useful beyond transcriptions:**
  - Extract text from complex PDFs (academic papers, scanned documents)
  - Parse DOCX/PPTX for knowledge base
  - Extract tables from PDFs as markdown
  - Clean HTML/EPUB content
  - Enhance mdcon with better structured output
- Already have core dependencies installed:
  - ✅ tesseract (OCR)
  - ✅ poppler (PDF processing)
  - ✅ LibreOffice (MS Office alternative)
  - ✅ pandoc (already in mdcon stack)

**How it works for transcriptions:**
```python
from unstructured.partition.text import partition_text
from unstructured.staging.base import elements_to_text

# Partition raw transcription into semantic elements
elements = partition_text(text=raw_transcription)

# Elements are automatically categorized:
# - Title (detected headings)
# - NarrativeText (paragraphs)
# - ListItem (detected lists)

# Clean and structure
cleaned_text = elements_to_text(elements)
```

**Why this works better than pure NLP:**
- Unstructured uses ML models + heuristics to detect structure
- Understands document semantics, not just sentence boundaries
- Already optimized for LLM preprocessing (our use case)
- Can detect quotes, attributions, lists without manual rules

---

## Alternative Tools (Text-Focused, No API)

### 1. **markdown-it (JavaScript/Node.js)**
- Markdown parser and renderer
- Extensible plugin system
- **Use:** Parse, validate, restructure markdown
- **Install:** `npm install markdown-it`

### 2. **mistune (Python)**
- Fast markdown parser in pure Python
- Can parse to AST and rebuild
- **Use:** Parse → manipulate → regenerate clean markdown
- **Install:** `pip install mistune`

### 3. **python-markdown (Python)**
- Official Python markdown implementation
- Extension system for custom processing
- **Use:** Parse → apply transformations → output
- **Install:** `pip install markdown`

### 4. **marko (Python)**
- CommonMark compliant parser
- AST manipulation
- **Use:** Parse transcription → clean AST → render
- **Install:** `pip install marko`

### 5. **LLM-based (Local) - Already Installed!**
- **Ollama 3.2** - ✅ Already installed on system
- **Use:** Pass transcription to local LLM with prompt: "Clean up this transcription: add punctuation, fix errors, structure paragraphs"
- **Pros:** Best quality, contextual understanding, no API costs
- **RAM considerations:**
  - Small models work on 8GB MacBook:
    - `llama3.2:1b` (1B params) - needs ~2GB RAM
    - `llama3.2:3b` (3B params) - needs ~4GB RAM
  - Install with: `ollama pull llama3.2:3b`
- **Cons:** Slower than rule-based (but high quality)

### 6. **Rule-based Python (Custom)**
- Use `nltk` + `textblob` + regex
- **Use:** Sentence segmentation, capitalization, punctuation inference
- **Pros:** Fast, deterministic, no external API
- **Install:** `pip install nltk textblob`

---

## Recommended Approach

**Primary: Unstructured for structure + Ollama for polish**

**Two-stage pipeline:**
1. **Structure detection (Unstructured):** Partition text into semantic elements, detect paragraphs/titles
2. **Polish (Ollama 3.2:3b):** Add punctuation, fix capitalization, correct transcription errors

**Why this combination:**
- Unstructured handles document structure (paragraphs, headings, lists)
- LLM handles linguistic nuances (punctuation, grammar, error correction)
- Both run locally (no API, no cost, no privacy concerns)
- Useful beyond transcriptions (PDF extraction, document processing)
- Ollama 3.2:3b fits in 8GB RAM

**Alternative modes:**
1. **Fast mode:** Unstructured only - good structure, basic cleanup
2. **Quality mode:** Unstructured + Ollama - excellent results, slower
3. **Future:** Enhance mdcon with Unstructured for better PDF extraction

---

## Dependencies

### Core Dependencies (Primary Approach)

**Already Installed:**
- ✅ tesseract (OCR)
- ✅ poppler (PDF processing)
- ✅ pandoc (document conversion)
- ✅ Ollama 3.2 (local LLM)

**Need to Install:**
```bash
# 1. LibreOffice (MS Office alternative + needed for Unstructured)
brew install --cask libreoffice

# 2. Unstructured with all document support
pip install "unstructured[all-docs]"

# 3. Ollama Python client
pip install ollama

# 4. Pull small Ollama model (works on 8GB RAM)
ollama pull llama3.2:3b
```

### Optional: For future PDF enhancement in mdcon
```bash
# Unstructured can extract tables, images, layout
# This complements existing mdcon tools
pip install "unstructured[pdf]"
```

---

## Suggested Coding Language

**Python** - Reasons:
- Existing mp3_txt/transcribe stack is Python
- Best NLP library ecosystem (nltk, spacy, textblob)
- Easy integration with Ollama
- Can keep mdclean as bash wrapper calling Python script

**Alternative:** Keep mdclean in bash with Python helper scripts:
```bash
./mdclean input.md output.md --mode=llm
./mdclean input.md output.md --mode=fast
```

---

## Workflow

### User Experience
```bash
# After transcription
./transcribe
# → Chooses file
# → Transcription completes
# → NEW: "Clean transcription? (y/n)"
# → If yes: "Mode: 1) Fast (Unstructured), 2) Quality (Unstructured+LLM)"
# → Processes and saves cleaned version
```

### Technical Flow

**Mode 1: Fast (Unstructured only)**
```python
from unstructured.partition.text import partition_text
from unstructured.staging.base import elements_to_text

1. Read raw transcription (preserve frontmatter)
2. Partition text into semantic elements:
   - Unstructured detects: Title, NarrativeText, ListItem
3. Clean and structure elements
4. Preserve frontmatter + combine elements
5. Write structured markdown
```

**Mode 2: Quality (Unstructured + Ollama)**
```python
import ollama
from unstructured.partition.text import partition_text

1. Read raw transcription (preserve frontmatter)
2. Partition with Unstructured (structure detection)
3. For each NarrativeText element:
   - Send to Ollama 3.2:3b with prompt:
     "Add punctuation and capitalization to this transcription.
      Fix obvious errors. Preserve all content:"
4. Combine cleaned elements
5. Preserve frontmatter + write clean markdown
```

**Why this works:**
- Unstructured handles paragraph/heading detection
- LLM adds linguistic polish (punctuation, grammar)
- Frontmatter (metadata) stays untouched
- Two-pass approach: structure first, polish second

---

## Expected Outcomes

### Before (Raw Vosk Output)
```markdown
---
source: sermon_001.mp3
author:
book title:
---

the one the question of an eternal hell alice laughed there's no use trying
she said one can't believe impossible things i daresay you haven't had much
practice said the queen when i was your age i always did it for half an hour
a day why sometimes i've believed as many as six impossible things before
breakfast lewis carroll through the looking glass framing the question one
according to a legend recounted in the apotheker martyr patron
```

### After - Mode 1: Fast (Unstructured only)
```markdown
---
source: sermon_001.mp3
author: [[David Bentley Hart]]
book title: [[That All Shall Be Saved]]
---

the one the question of an eternal hell alice laughed there's no use trying she said one can't believe impossible things i daresay you haven't had much practice said the queen when i was your age i always did it for half an hour a day why sometimes i've believed as many as six impossible things before breakfast lewis carroll through the looking glass

framing the question one according to a legend recounted in the apotheker martyr patron or sayings of the fathers a name shared in common by various ancient christian collections of anecdotes about the egyptian desert fathers of the fourth century the holy man aba makarios was walking alone in the wilderness one day...
```

**Improvements:**
- ✅ Paragraph breaks detected (structure)
- ✅ Frontmatter preserved
- ⚠️ Still needs punctuation/capitalization (that's what LLM adds)

### After - Mode 2: Quality (Unstructured + LLM)
```markdown
---
source: sermon_001.mp3
author: [[David Bentley Hart]]
book title: [[That All Shall Be Saved]]
---

## The Question of an Eternal Hell

"Alice laughed. 'There's no use trying,' she said. 'One can't believe
impossible things.'

'I daresay you haven't had much practice,' said the Queen. 'When I was your
age, I always did it for half an hour a day. Why, sometimes I've believed
as many as six impossible things before breakfast.'"

— Lewis Carroll, *Through the Looking Glass*

### Framing the Question

According to a legend recounted in the *Apophthegmata Patrum* (Sayings of
the Fathers)—a name shared in common by various ancient Christian collections
of anecdotes about the Egyptian desert fathers of the fourth century—the
holy man Abba Makarios was walking alone in the wilderness one day...
```

**Quality improvements:**
- ✅ Proper punctuation and capitalization
- ✅ Paragraph breaks at natural points
- ✅ Quote formatting with attribution
- ✅ Italics for book titles
- ✅ Heading structure detected
- ✅ Fixed transcription errors (apotheker → Apophthegmata)
- ✅ Better readability for knowledge base

---

## Implementation Phases

### Phase 1: Unstructured Integration (2-3 hours)
- Install LibreOffice + Unstructured
- Create `mdclean-unstructured.py` script
- Test structure detection on transcription samples
- Preserve frontmatter during processing

### Phase 2: LLM Polish Layer (1-2 hours)
- Install Ollama Python client
- Pull llama3.2:3b model (4GB, works on 8GB RAM)
- Create `mdclean-quality.py` combining Unstructured + Ollama
- Chunk processing for long transcriptions

### Phase 3: Integration + UX (1-2 hours)
- Add to transcribe workflow as optional step
- User can choose: Fast (Unstructured) or Quality (Unstructured+LLM)
- Progress indicators for processing
- Error handling

---

## Next Steps

1. **Install dependencies:**
   ```bash
   brew install --cask libreoffice
   pip install "unstructured[all-docs]" ollama
   ollama pull llama3.2:3b
   ```

2. **Create prototype:**
   - Simple Python script: raw transcription → Unstructured → cleaned output
   - Test structure detection quality on real transcriptions

3. **Test LLM layer:**
   - Verify llama3.2:3b quality for punctuation/grammar
   - Benchmark speed on ~10min transcription

4. **Integrate:**
   - Add to transcribe CLI as optional post-processing step
   - Keep as separate tool or integrate inline?

---

## Questions to Answer During Implementation

- [ ] How well does Unstructured detect structure in raw transcriptions?
- [ ] Which Ollama model size works best? (1b vs 3b)
- [ ] What's the optimal chunk size for LLM processing?
- [ ] How to preserve frontmatter (author, book title wikilinks)?
- [ ] Should mdclean be inline in transcribe or separate CLI tool?
- [ ] Can we auto-detect when cleanup is needed?
- [ ] Future: Use Unstructured to enhance mdcon PDF extraction?

---

## Final Decision

**Primary Approach:** Unstructured + Ollama 3.2:3b hybrid

**Why:**
- ✅ Unstructured handles document structure (already useful for PDF extraction)
- ✅ Ollama 3.2:3b fits in 8GB RAM (~4GB model)
- ✅ Both run locally (no API costs, works offline)
- ✅ Can learn Unstructured for other use cases (mdcon enhancement, document processing)
- ✅ LibreOffice needed anyway as MS Office alternative

**Implementation:**
1. **Fast mode:** Unstructured only (structure detection)
2. **Quality mode:** Unstructured + Ollama (structure + polish)
3. **Future:** Enhance mdcon with Unstructured for better PDF text extraction

**Alternative if RAM issues:** Unstructured-only mode still provides value (paragraph detection, structure).
