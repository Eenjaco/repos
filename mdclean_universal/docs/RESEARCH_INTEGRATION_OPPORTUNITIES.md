# Research: Document Processing Tools & Integration Opportunities

## Current Status

**Unstructured Integration:** ✅ Partially implemented
- Currently used: `partition_text()` for basic text structuring
- Location: `StructureDetector` class (line 597)
- Status: Optional dependency with graceful fallback

**Gap:** Only uses text partitioning - not leveraging Unstructured's full document-specific partitioners

## 🔥 Hot New Tools (2025)

### 1. **MinerU** ⭐ Highly Recommended
**GitHub:** https://github.com/opendatalab/MinerU
**Stars:** Very active (2025)
**What it does:**
- Transforms PDFs into LLM-ready markdown/JSON
- OCR supports 109 languages
- PP-OCRv5 backend with 30% accuracy improvement
- Specifically designed for AI/LLM workflows

**Integration Opportunity:**
```python
# Instead of pdfplumber for PDFs
from mineru import process_pdf

def extract_pdf_text_advanced(self, pdf_path: Path) -> str:
    """Use MinerU for better PDF extraction"""
    result = process_pdf(pdf_path, output_format='markdown')
    return result
```

**Why integrate:**
- ✅ Much better table extraction than pdfplumber
- ✅ Handles complex layouts (multi-column)
- ✅ Better formula/equation detection
- ✅ Optimized for LLM consumption

---

### 2. **Microsoft MarkItDown** ⭐ Very Promising
**GitHub:** https://github.com/microsoft/markitdown
**Stars:** Growing rapidly
**What it does:**
- Lightweight Python utility for file → Markdown
- Azure Document Intelligence integration
- Built by Microsoft for LLM pipelines

**Integration Opportunity:**
```python
from markitdown import MarkItDown

def convert_office_document(self, file_path: Path) -> str:
    """Use Microsoft's MarkItDown for Office docs"""
    md = MarkItDown()
    result = md.convert(file_path)
    return result.text_content
```

**Why integrate:**
- ✅ Better DOCX/PPTX handling than pandoc
- ✅ Preserves formatting and tables
- ✅ Microsoft-backed (reliable)
- ✅ Can use Azure AI for enhanced extraction

---

### 3. **Docling** ⭐ IBM Research Project
**GitHub:** https://github.com/docling-project/docling
**Stars:** Active development
**What it does:**
- Extensive OCR with Visual Language Models
- ASR (Automatic Speech Recognition) for audio
- GraniteDocling VLM support

**Integration Opportunity:**
```python
from docling import DocumentConverter

def process_with_docling(self, file_path: Path) -> dict:
    """Use Docling for multi-modal processing"""
    converter = DocumentConverter()
    result = converter.convert(file_path)
    return {
        'text': result.document.export_to_markdown(),
        'tables': result.tables,
        'images': result.images
    }
```

**Why integrate:**
- ✅ Handles scanned PDFs better
- ✅ Audio transcription (alternative to Vosk)
- ✅ IBM Research quality
- ✅ VLM support for complex layouts

---

### 4. **NanoNets docext**
**GitHub:** https://github.com/NanoNets/docext
**Stars:** Active
**What it does:**
- OCR-free unstructured data extraction
- PDF & Image → Markdown with intelligent recognition
- LaTeX equations, tables, semantic tagging

**Integration Opportunity:**
```python
from docext import extract_document

def extract_with_docext(self, file_path: Path) -> str:
    """Use docext for intelligent extraction"""
    result = extract_document(
        file_path,
        features=['tables', 'equations', 'signatures']
    )
    return result.to_markdown()
```

**Why integrate:**
- ✅ No OCR needed (uses vision models)
- ✅ LaTeX equation support
- ✅ Signature/watermark detection
- ✅ Semantic tagging

---

### 5. **DeepSeek-OCR** 🆕 Latest (2025)
**GitHub:** https://github.com/deepseek-ai/DeepSeek-OCR
**Stars:** New but promising
**What it does:**
- 3B parameter vision-language model
- Converts documents to Markdown
- Layout parsing and GPU acceleration
- MIT license (permissive)

**Integration Opportunity:**
```python
from deepseek_ocr import DeepSeekOCR

def ocr_with_deepseek(self, image_path: Path) -> str:
    """Use DeepSeek-OCR for images"""
    model = DeepSeekOCR()
    result = model.process(image_path, output_format='markdown')
    return result
```

**Why integrate:**
- ✅ Better OCR than Tesseract
- ✅ Layout-aware (preserves structure)
- ✅ Markdown-first output
- ✅ GPU support (fast)

---

### 6. **PaddleOCR v3.0**
**GitHub:** https://github.com/PaddlePaddle/PaddleOCR
**Stars:** 45k+ ⭐⭐⭐ Very Popular
**What it does:**
- 100+ language OCR
- Extremely lightweight
- Mobile-optimized
- Best-in-class for multilingual

**Integration Opportunity:**
```python
from paddleocr import PaddleOCR

def ocr_with_paddle(self, image_path: Path, lang: str = 'en') -> str:
    """Use PaddleOCR for multilingual support"""
    ocr = PaddleOCR(lang=lang)
    result = ocr.ocr(str(image_path), cls=True)
    return '\n'.join([line[1][0] for line in result[0]])
```

**Why integrate:**
- ✅ Better multilingual than Tesseract
- ✅ Perfect for Afrikaans content
- ✅ Very lightweight
- ✅ Production-ready

---

## Full Unstructured.io Capabilities (Not Currently Used)

### What We're Missing:

**Document-Specific Partitioners:**
```python
# PDF (better than our current pdfplumber)
from unstructured.partition.pdf import partition_pdf
elements = partition_pdf("document.pdf")

# DOCX (better than pandoc)
from unstructured.partition.docx import partition_docx
elements = partition_docx("document.docx")

# PPTX (new!)
from unstructured.partition.pptx import partition_pptx
elements = partition_pptx("slides.pptx")

# HTML (better than BeautifulSoup)
from unstructured.partition.html import partition_html
elements = partition_html(filename="page.html")

# EPUB
from unstructured.partition.epub import partition_epub
elements = partition_epub("book.epub")

# Images with OCR
from unstructured.partition.image import partition_image
elements = partition_image("scan.jpg")

# Email
from unstructured.partition.email import partition_email
elements = partition_email("message.eml")
```

**Advanced Features:**
- **Chunking:** Smart chunking for LLM context windows
- **Embeddings:** Direct integration with embedding models
- **Tables:** Better table extraction than current approach
- **Metadata:** Rich metadata extraction
- **Staging:** Clean/transform elements before output

### Current vs Enhanced Unstructured

**Current (Basic):**
```python
# We only use this
from unstructured.partition.text import partition_text
elements = partition_text(text=text)
```

**Enhanced (Full Power):**
```python
# Document-aware partitioning
from unstructured.partition.auto import partition
elements = partition("any-document.pdf")  # Auto-detects type

# With chunking for long documents
from unstructured.chunking.title import chunk_by_title
chunks = chunk_by_title(elements, max_characters=2000)

# With table extraction
from unstructured.partition.pdf import partition_pdf
elements = partition_pdf(
    "document.pdf",
    strategy="hi_res",  # High resolution for tables
    extract_images_in_pdf=True,
    infer_table_structure=True
)
```

---

## Recommended Integration Plan

### Phase 1: Quick Wins (1-2 days)

**1. Enable Full Unstructured (Easy)**
Replace custom parsers with Unstructured's document-specific partitioners:

```python
class EnhancedDocumentParser:
    """Use Unstructured's full capabilities"""

    def parse_document(self, file_path: Path) -> List[Any]:
        from unstructured.partition.auto import partition

        # Auto-detects PDF, DOCX, PPTX, HTML, etc.
        elements = partition(
            filename=str(file_path),
            strategy="hi_res",  # Better quality
            extract_images_in_pdf=True,
            infer_table_structure=True,
            languages=["eng", "afr"]  # English + Afrikaans
        )

        return elements
```

**Benefits:**
- ✅ Better PDF extraction (replaces pdfplumber)
- ✅ Better DOCX parsing (replaces pandoc)
- ✅ PPTX support (new!)
- ✅ Better table extraction
- ✅ Image extraction from PDFs

---

### Phase 2: Add MinerU for PDFs (2-3 days)

**Why:** MinerU is specifically optimized for AI/LLM workflows

```python
class HybridPDFParser:
    """Best-of-breed PDF parsing"""

    def parse_pdf(self, pdf_path: Path, method='auto') -> str:
        if method == 'auto':
            # Try MinerU first (best for AI)
            try:
                from mineru import process_pdf
                result = process_pdf(pdf_path, output_format='markdown')
                if self._quality_check(result):
                    return result
            except:
                pass

            # Fall back to Unstructured (good balance)
            try:
                from unstructured.partition.pdf import partition_pdf
                elements = partition_pdf(
                    str(pdf_path),
                    strategy="hi_res",
                    extract_images_in_pdf=True
                )
                return self._elements_to_markdown(elements)
            except:
                pass

            # Last resort: pdfplumber (reliable but basic)
            return self._pdfplumber_extract(pdf_path)
```

**Benefits:**
- ✅ Best possible PDF extraction
- ✅ Graceful fallback chain
- ✅ Quality validation

---

### Phase 3: Add PaddleOCR for Multilingual (1-2 days)

**Why:** Much better for Afrikaans and multilingual documents

```python
class EnhancedOCR:
    """Best-in-class OCR with language detection"""

    def __init__(self):
        try:
            from paddleocr import PaddleOCR
            self.paddle_ocr = PaddleOCR(
                use_angle_cls=True,
                lang='en',  # Can switch to 'af' for Afrikaans
                show_log=False
            )
        except:
            self.paddle_ocr = None

        # Keep Tesseract as fallback
        self.tesseract_available = self._check_tesseract()

    def extract_text(self, image_path: Path, language='auto') -> str:
        # Detect language if auto
        if language == 'auto':
            language = self.detect_language(image_path)

        # Try PaddleOCR first (better quality)
        if self.paddle_ocr:
            try:
                result = self.paddle_ocr.ocr(str(image_path), cls=True)
                text = self._paddle_to_markdown(result)
                if text and len(text) > 50:  # Quality check
                    return text
            except:
                pass

        # Fall back to Tesseract
        if self.tesseract_available:
            return self._tesseract_extract(image_path, language)

        raise RuntimeError("No OCR engine available")
```

**Benefits:**
- ✅ Better accuracy for Afrikaans
- ✅ 100+ languages supported
- ✅ Better layout preservation
- ✅ Fallback to Tesseract

---

### Phase 4: Add Docling for Audio (Optional, 3-4 days)

**Why:** Better than Vosk for speech recognition

```python
class EnhancedAudioHandler:
    """Modern ASR with Docling"""

    def transcribe(self, audio_path: Path) -> str:
        try:
            from docling import AudioConverter
            converter = AudioConverter()
            result = converter.convert_audio(
                str(audio_path),
                language='auto',
                timestamps=True
            )
            return result.text
        except:
            # Fall back to Vosk
            return self._vosk_transcribe(audio_path)
```

---

## Tool Comparison Matrix

| Tool | PDF | DOCX | Images | Audio | Multi-lang | LLM-Ready | Stars | Active |
|------|-----|------|--------|-------|------------|-----------|-------|--------|
| **Unstructured** | ✅ | ✅ | ✅ | ❌ | ⚠️ | ✅✅ | High | ✅ 2025 |
| **MinerU** | ✅✅ | ❌ | ⚠️ | ❌ | ✅ | ✅✅✅ | High | ✅ 2025 |
| **MarkItDown** | ✅ | ✅✅ | ❌ | ❌ | ⚠️ | ✅✅ | Growing | ✅ 2025 |
| **Docling** | ✅ | ✅ | ✅✅ | ✅✅ | ✅ | ✅✅ | Medium | ✅ 2025 |
| **PaddleOCR** | ❌ | ❌ | ✅✅✅ | ❌ | ✅✅✅ | ✅ | 45k | ✅ 2025 |
| **DeepSeek-OCR** | ❌ | ❌ | ✅✅ | ❌ | ✅ | ✅✅ | New | ✅ 2025 |
| **docext** | ✅ | ❌ | ✅✅ | ❌ | ⚠️ | ✅✅ | Medium | ✅ 2025 |

**Legend:**
- ✅✅✅ = Best in class
- ✅✅ = Excellent
- ✅ = Good
- ⚠️ = Limited/Basic
- ❌ = Not supported

---

## Recommended Stack (Best of Breed)

```python
# PDF Processing
- Primary: MinerU (best for AI/LLM)
- Fallback: Unstructured partition_pdf (good balance)
- Last resort: pdfplumber (reliable but basic)

# Office Documents (DOCX, PPTX)
- Primary: Unstructured (handles both well)
- Alternative: Microsoft MarkItDown (if needed)

# Images/OCR
- Primary: PaddleOCR (multilingual, Afrikaans)
- Alternative: DeepSeek-OCR (better layout)
- Fallback: Tesseract (reliable)

# Audio
- Primary: Docling ASR (modern, accurate)
- Fallback: Vosk (offline, reliable)

# Web/HTML
- Primary: Unstructured partition_html
- Fallback: Current BeautifulSoup approach
```

---

## Implementation Priority

### Must Have (Week 1):
1. **Full Unstructured integration** - Replace current parsers
2. **PaddleOCR** - Better multilingual support

### Should Have (Week 2):
3. **MinerU** - Better PDF extraction
4. **Content-type detection** - Smart prompt selection

### Nice to Have (Week 3+):
5. **Docling** - Audio transcription alternative
6. **MarkItDown** - Microsoft Office docs alternative

---

## Installation

```bash
# Current (what you have)
pip install 'unstructured[all-docs]' ollama pytesseract

# Enhanced (recommended)
pip install 'unstructured[all-docs]' ollama pytesseract paddlepaddle paddleocr mineru

# Full stack (everything)
pip install 'unstructured[all-docs]' ollama pytesseract \
            paddlepaddle paddleocr mineru markitdown docling
```

---

## Next Steps

1. ✅ Run current test suite to establish baseline
2. 🔄 Integrate full Unstructured capabilities
3. 🔄 Add PaddleOCR for better multilingual
4. 🔄 Optionally add MinerU for PDFs
5. 📊 Re-run tests and compare results
6. 📈 Measure quality improvements

---

## Questions to Answer with Testing

1. **PDF Quality:** Does MinerU extract better than pdfplumber?
2. **Table Extraction:** Does Unstructured handle tables better?
3. **Afrikaans OCR:** Is PaddleOCR better than Tesseract?
4. **PPTX:** Does Unstructured handle PowerPoint well?
5. **Performance:** What's the speed/quality tradeoff?

Let's run the tests to find out!
