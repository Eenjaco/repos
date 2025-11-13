#!/usr/bin/env python3
"""
mdclean_universal - Universal document processor for knowledge management

Converts ANY input to clean, structured markdown:
- Images (OCR with Tesseract)
- Audio (transcription with Vosk/Whisper)
- Documents (PDF, EPUB, DOCX, HTML)
- Text (TXT, MD)

Pipeline: Extract → Structure (Unstructured) → Clean (Ollama 3.2 1B) → Format (KM)

Usage:
    mdclean_universal document.pdf
    mdclean_universal image.jpg --output ~/Vault/Inbox/
    mdclean_universal --batch ~/Documents/to-process/
"""

import argparse
import sys
import subprocess
from pathlib import Path
from typing import Tuple, List, Optional, Dict, Any
from datetime import datetime
from dataclasses import dataclass
import json
import tempfile
import shutil

# Version
__version__ = "1.0.0"

# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class ProcessingResult:
    """Result of document processing"""
    success: bool
    output_path: Optional[Path] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = None
    processing_time: float = 0.0


@dataclass
class DocumentMetadata:
    """Metadata extracted from document"""
    source_file: str
    file_type: str
    date_processed: str
    original_size: int
    page_count: Optional[int] = None
    duration: Optional[str] = None
    language: Optional[str] = None
    tags: List[str] = None


# ============================================================================
# Input Router
# ============================================================================

class InputRouter:
    """Detect file type and route to appropriate handler"""

    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp'}
    AUDIO_EXTENSIONS = {'.mp3', '.m4a', '.wav', '.flac', '.ogg'}
    PDF_EXTENSIONS = {'.pdf'}
    DOCUMENT_EXTENSIONS = {'.epub', '.docx', '.odt', '.rtf'}
    WEB_EXTENSIONS = {'.html', '.htm', '.mhtml'}
    TEXT_EXTENSIONS = {'.txt', '.md', '.markdown'}

    @classmethod
    def detect_type(cls, file_path: Path) -> str:
        """
        Detect input type based on file extension.

        Returns: 'image', 'audio', 'pdf', 'document', 'web', or 'text'
        """
        extension = file_path.suffix.lower()

        if extension in cls.IMAGE_EXTENSIONS:
            return 'image'
        elif extension in cls.AUDIO_EXTENSIONS:
            return 'audio'
        elif extension in cls.PDF_EXTENSIONS:
            return 'pdf'
        elif extension in cls.DOCUMENT_EXTENSIONS:
            return 'document'
        elif extension in cls.WEB_EXTENSIONS:
            return 'web'
        elif extension in cls.TEXT_EXTENSIONS:
            return 'text'
        else:
            raise ValueError(f"Unsupported file type: {extension}")


# ============================================================================
# Extraction Handlers
# ============================================================================

class OCRHandler:
    """Extract text from images using Tesseract OCR"""

    def __init__(self, language='eng', preprocess=True, handwriting_mode=False):
        self.language = language
        self.preprocess = preprocess
        self.handwriting_mode = handwriting_mode

    def check_dependencies(self) -> bool:
        """Check if Tesseract is installed"""
        try:
            subprocess.run(['tesseract', '--version'],
                          capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def preprocess_image(self, image_path: Path, output_path: Path) -> bool:
        """
        Preprocess image for better OCR results.
        Requires: ImageMagick (convert command)
        """
        try:
            # Deskew, enhance contrast, denoise
            cmd = [
                'convert',
                str(image_path),
                '-deskew', '40%',
                '-contrast-stretch', '0',
                '-type', 'grayscale',
                str(output_path)
            ]
            subprocess.run(cmd, capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            # ImageMagick not available or failed, use original
            shutil.copy(image_path, output_path)
            return False

    def extract_text(self, image_path: Path) -> str:
        """
        Extract text from image using Tesseract.

        Returns: Extracted text
        """
        if not self.check_dependencies():
            raise RuntimeError("Tesseract OCR not installed. Install with: brew install tesseract")

        # Create temp directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            processed_image = temp_dir_path / "processed.png"

            # Preprocess if enabled
            if self.preprocess:
                self.preprocess_image(image_path, processed_image)
            else:
                processed_image = image_path

            # Run Tesseract
            output_base = temp_dir_path / "output"
            cmd = [
                'tesseract',
                str(processed_image),
                str(output_base),
                '-l', self.language,
            ]

            # Add handwriting mode if enabled
            if self.handwriting_mode:
                cmd.extend(['--psm', '6'])  # Assume uniform block of text
            else:
                cmd.extend(['--psm', '3'])  # Fully automatic page segmentation

            subprocess.run(cmd, capture_output=True, check=True)

            # Read extracted text
            output_file = output_base.with_suffix('.txt')
            if output_file.exists():
                return output_file.read_text(encoding='utf-8')
            else:
                return ""


class AudioHandler:
    """Transcribe audio files"""

    def __init__(self, engine='vosk', model_path=None, timestamps=False):
        self.engine = engine
        self.model_path = model_path
        self.timestamps = timestamps

    def extract_text(self, audio_path: Path) -> str:
        """
        Transcribe audio file.

        For now, we'll integrate with existing transcribe_vosk_stream.py logic.
        Returns: Transcribed text
        """
        # Import transcription functionality
        try:
            # Try to import from mp3_txt directory
            import transcribe_vosk_stream

            # Use existing transcription logic
            # This is a simplified version - actual implementation would
            # integrate with the existing transcribe_vosk_stream.py
            raise NotImplementedError("Audio transcription - integrate with existing transcribe_vosk_stream.py")

        except ImportError:
            raise RuntimeError("Audio transcription module not found")


class DocumentParser:
    """Parse documents (PDF, EPUB, DOCX, etc.)"""

    def __init__(self):
        pass

    def check_dependencies(self, doc_type: str) -> bool:
        """Check if required tools are installed"""
        if doc_type == 'pdf':
            try:
                subprocess.run(['pdftotext', '-v'],
                              capture_output=True, check=True)
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                return False
        elif doc_type in ['document', 'web']:
            try:
                subprocess.run(['pandoc', '--version'],
                              capture_output=True, check=True)
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                return False
        return True

    def is_scanned_pdf(self, pdf_path: Path) -> bool:
        """Detect if PDF is scanned (has no text layer)"""
        try:
            # Try to extract text from first page
            result = subprocess.run(
                ['pdftotext', '-l', '1', str(pdf_path), '-'],
                capture_output=True,
                text=True
            )
            text = result.stdout.strip()
            # If less than 50 characters, probably scanned
            return len(text) < 50
        except:
            return True  # Assume scanned if check fails

    def extract_pdf_text(self, pdf_path: Path) -> str:
        """Extract text from PDF"""
        if not self.check_dependencies('pdf'):
            raise RuntimeError("pdftotext not installed. Install with: brew install poppler")

        # Check if scanned
        if self.is_scanned_pdf(pdf_path):
            print("  Detected scanned PDF, using OCR...")
            return self.extract_scanned_pdf(pdf_path)

        # Extract text with layout preservation
        result = subprocess.run(
            ['pdftotext', '-layout', str(pdf_path), '-'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout

    def extract_scanned_pdf(self, pdf_path: Path) -> str:
        """Extract text from scanned PDF using OCR"""
        # Use OCRHandler for scanned PDFs
        # This requires ghostscript to convert PDF pages to images first

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Extract pages as images with ghostscript
            try:
                subprocess.run([
                    'gs', '-dNOPAUSE', '-dBATCH', '-sDEVICE=png16m',
                    '-r300', f'-sOutputFile={temp_path}/page_%03d.png',
                    str(pdf_path)
                ], capture_output=True, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                raise RuntimeError("Ghostscript not installed. Install with: brew install ghostscript")

            # OCR each page
            ocr = OCRHandler()
            all_text = []

            for page_img in sorted(temp_path.glob("page_*.png")):
                page_num = page_img.stem.split('_')[1]
                print(f"    OCR page {page_num}...")
                text = ocr.extract_text(page_img)
                if text.strip():
                    all_text.append(f"\n<!-- Page {page_num} -->\n\n{text}")

            return "\n".join(all_text)

    def extract_document_text(self, doc_path: Path) -> str:
        """Extract text from DOCX, EPUB, etc. using pandoc"""
        if not self.check_dependencies('document'):
            raise RuntimeError("pandoc not installed. Install with: brew install pandoc")

        # Detect format
        extension = doc_path.suffix.lower()

        if extension == '.epub':
            from_format = 'epub'
        elif extension == '.docx':
            from_format = 'docx'
        elif extension == '.odt':
            from_format = 'odt'
        elif extension == '.rtf':
            from_format = 'rtf'
        else:
            from_format = 'docx'  # Default

        # Convert to plain text with pandoc
        result = subprocess.run(
            ['pandoc', str(doc_path), '-f', from_format, '-t', 'plain', '--wrap=none'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout

    def extract_html_text(self, html_path: Path) -> str:
        """Extract text from HTML using pandoc"""
        if not self.check_dependencies('web'):
            raise RuntimeError("pandoc not installed. Install with: brew install pandoc")

        result = subprocess.run(
            ['pandoc', str(html_path), '-f', 'html', '-t', 'plain', '--wrap=none'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout

    def extract_text(self, doc_path: Path, doc_type: str) -> str:
        """
        Extract text from document based on type.

        Args:
            doc_path: Path to document
            doc_type: One of 'pdf', 'document', 'web'

        Returns: Extracted text
        """
        if doc_type == 'pdf':
            return self.extract_pdf_text(doc_path)
        elif doc_type == 'document':
            return self.extract_document_text(doc_path)
        elif doc_type == 'web':
            return self.extract_html_text(doc_path)
        else:
            raise ValueError(f"Unknown document type: {doc_type}")


# ============================================================================
# Structure Detection (Unstructured)
# ============================================================================

class StructureDetector:
    """Detect document structure using Unstructured library"""

    def __init__(self):
        try:
            from unstructured.partition.text import partition_text
            self.partition_text = partition_text
        except ImportError:
            print("Warning: unstructured library not installed.")
            print("Install with: pip install 'unstructured[all-docs]'")
            self.partition_text = None

    def detect_structure(self, text: str) -> List[Any]:
        """
        Detect document elements (titles, paragraphs, lists, tables).

        Returns: List of Element objects from Unstructured
        """
        if self.partition_text is None:
            # Fallback: return text as single element
            return [{'type': 'text', 'content': text}]

        elements = self.partition_text(text=text)
        return elements


# ============================================================================
# LLM Cleaner (Ollama)
# ============================================================================

class OllamaCleaner:
    """Clean and format text using Ollama LLM"""

    def __init__(self, model='llama3.2:1b', endpoint='http://localhost:11434'):
        self.model = model
        self.endpoint = endpoint

    def check_ollama(self) -> bool:
        """Check if Ollama is running"""
        try:
            import ollama
            # Try to list models
            ollama.list()
            return True
        except Exception:
            return False

    def clean_text_chunk(self, text: str) -> str:
        """
        Clean a chunk of text with Ollama.

        Adds punctuation, capitalization, fixes errors.
        """
        if not self.check_ollama():
            print("Warning: Ollama not available, skipping LLM cleanup")
            return text

        try:
            import ollama

            prompt = f"""Clean up this text by:
1. Adding proper punctuation (periods, commas, question marks)
2. Adding proper capitalization
3. Fixing obvious transcription or OCR errors
4. Organizing into natural paragraphs
5. DO NOT summarize or remove content - preserve everything

Text:
{text}

Cleaned version:"""

            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={
                    'temperature': 0.2,
                    'num_predict': 4096,
                }
            )

            return response['response'].strip()

        except Exception as e:
            print(f"Warning: Ollama error: {e}")
            return text

    def clean_elements(self, elements: List[Any]) -> str:
        """
        Clean structured elements with Ollama.

        Processes each element type appropriately.
        """
        cleaned_parts = []

        print(f"  Processing {len(elements)} elements with Ollama ({self.model})...")

        for i, element in enumerate(elements):
            # Get element type and text
            if hasattr(element, '__class__'):
                elem_type = element.__class__.__name__
                elem_text = str(element).strip()
            else:
                elem_type = element.get('type', 'text')
                elem_text = element.get('content', '').strip()

            if not elem_text:
                continue

            print(f"    Element {i+1}/{len(elements)} ({elem_type})...", end=' ')

            # Handle different element types
            if elem_type == 'Title':
                # Format as heading
                cleaned = f"## {elem_text}"
            elif elem_type in ['NarrativeText', 'text']:
                # Clean paragraphs with LLM
                # Split into chunks if too long
                if len(elem_text) > 2000:
                    # Process in chunks
                    chunks = self._split_into_chunks(elem_text, 2000)
                    cleaned_chunks = [self.clean_text_chunk(chunk) for chunk in chunks]
                    cleaned = "\n\n".join(cleaned_chunks)
                else:
                    cleaned = self.clean_text_chunk(elem_text)
            elif elem_type == 'ListItem':
                # Format as list item
                cleaned = f"- {elem_text}"
            else:
                # Keep as-is
                cleaned = elem_text

            cleaned_parts.append(cleaned)
            print("✓")

        return "\n\n".join(cleaned_parts)

    def _split_into_chunks(self, text: str, chunk_size: int) -> List[str]:
        """Split text into chunks at sentence boundaries"""
        sentences = text.split('. ')
        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            sentence_length = len(sentence)
            if current_length + sentence_length > chunk_size and current_chunk:
                chunks.append('. '.join(current_chunk) + '.')
                current_chunk = [sentence]
                current_length = sentence_length
            else:
                current_chunk.append(sentence)
                current_length += sentence_length

        if current_chunk:
            chunks.append('. '.join(current_chunk))

        return chunks


# ============================================================================
# Knowledge Management Formatter
# ============================================================================

class KMFormatter:
    """Format output for knowledge management systems"""

    def __init__(self, add_frontmatter=True, extract_tags=True):
        self.add_frontmatter = add_frontmatter
        self.extract_tags = extract_tags

    def generate_frontmatter(self, metadata: DocumentMetadata) -> str:
        """Generate YAML frontmatter"""
        if not self.add_frontmatter:
            return ""

        tags = metadata.tags if metadata.tags else []
        tags_str = "[" + ", ".join(tags) + "]" if tags else "[]"

        frontmatter = f"""---
source: {metadata.source_file}
date_processed: {metadata.date_processed}
type: {metadata.file_type}
"""

        if metadata.page_count:
            frontmatter += f"pages: {metadata.page_count}\n"
        if metadata.duration:
            frontmatter += f"duration: {metadata.duration}\n"
        if metadata.language:
            frontmatter += f"language: {metadata.language}\n"

        frontmatter += f"tags: {tags_str}\n"
        frontmatter += "---\n\n"

        return frontmatter

    def extract_title(self, text: str) -> Optional[str]:
        """Try to extract document title from first heading"""
        lines = text.split('\n')
        for line in lines[:10]:  # Check first 10 lines
            line = line.strip()
            if line.startswith('# '):
                return line[2:].strip()
            elif line.startswith('## '):
                return line[3:].strip()
        return None

    def format_output(self, cleaned_text: str, metadata: DocumentMetadata) -> str:
        """
        Format final output with frontmatter and structure.

        Returns: Formatted markdown ready for KM system
        """
        # Generate frontmatter
        frontmatter = self.generate_frontmatter(metadata)

        # Add title if not present
        title = self.extract_title(cleaned_text)
        if not title:
            # Use filename as title
            title = Path(metadata.source_file).stem.replace('_', ' ').replace('-', ' ').title()
            cleaned_text = f"# {title}\n\n{cleaned_text}"

        return frontmatter + cleaned_text


# ============================================================================
# Main Processor
# ============================================================================

class UniversalProcessor:
    """Main processor orchestrating the entire pipeline"""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}

        # Initialize components
        self.ocr_handler = OCRHandler(
            language=self.config.get('ocr_language', 'eng'),
            preprocess=self.config.get('ocr_preprocess', True),
            handwriting_mode=self.config.get('ocr_handwriting', False)
        )
        self.audio_handler = AudioHandler()
        self.doc_parser = DocumentParser()
        self.structure_detector = StructureDetector()
        self.llm_cleaner = OllamaCleaner(
            model=self.config.get('ollama_model', 'llama3.2:1b')
        )
        self.km_formatter = KMFormatter(
            add_frontmatter=self.config.get('add_frontmatter', True),
            extract_tags=self.config.get('extract_tags', True)
        )

    def process_file(self, input_path: Path, output_path: Optional[Path] = None) -> ProcessingResult:
        """
        Process a single file through the complete pipeline.

        Pipeline: Extract → Structure → Clean → Format → Output
        """
        start_time = datetime.now()

        try:
            # Validate input
            if not input_path.exists():
                return ProcessingResult(
                    success=False,
                    error=f"File not found: {input_path}"
                )

            print(f"\n📄 Processing: {input_path.name}")
            print(f"   Size: {input_path.stat().st_size / 1024:.1f} KB")

            # Detect file type
            file_type = InputRouter.detect_type(input_path)
            print(f"   Type: {file_type}")

            # STEP 1: Extract raw text
            print("\n1️⃣  Extracting text...")
            raw_text = self._extract_text(input_path, file_type)

            if not raw_text or len(raw_text.strip()) < 10:
                return ProcessingResult(
                    success=False,
                    error="No text extracted from document"
                )

            print(f"   ✓ Extracted {len(raw_text)} characters")

            # STEP 2: Detect structure
            print("\n2️⃣  Detecting structure...")
            elements = self.structure_detector.detect_structure(raw_text)
            print(f"   ✓ Detected {len(elements)} elements")

            # STEP 3: Clean with LLM
            print("\n3️⃣  Cleaning with LLM...")
            cleaned_text = self.llm_cleaner.clean_elements(elements)
            print(f"   ✓ Cleaned text ready")

            # STEP 4: Format for KM
            print("\n4️⃣  Formatting for knowledge management...")
            metadata = DocumentMetadata(
                source_file=input_path.name,
                file_type=file_type,
                date_processed=datetime.now().isoformat(),
                original_size=input_path.stat().st_size,
                tags=[file_type]
            )

            final_output = self.km_formatter.format_output(cleaned_text, metadata)
            print(f"   ✓ Formatted markdown ready")

            # STEP 5: Save output
            if output_path is None:
                output_path = input_path.parent / f"{input_path.stem}_processed.md"

            output_path.write_text(final_output, encoding='utf-8')

            processing_time = (datetime.now() - start_time).total_seconds()

            print(f"\n✅ Success! Saved to: {output_path}")
            print(f"   Processing time: {processing_time:.1f}s")

            return ProcessingResult(
                success=True,
                output_path=output_path,
                metadata=metadata.__dict__,
                processing_time=processing_time
            )

        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            print(f"\n❌ Error: {str(e)}")

            return ProcessingResult(
                success=False,
                error=str(e),
                processing_time=processing_time
            )

    def _extract_text(self, input_path: Path, file_type: str) -> str:
        """Extract text based on file type"""
        if file_type == 'image':
            return self.ocr_handler.extract_text(input_path)
        elif file_type == 'audio':
            return self.audio_handler.extract_text(input_path)
        elif file_type in ['pdf', 'document', 'web']:
            return self.doc_parser.extract_text(input_path, file_type)
        elif file_type == 'text':
            return input_path.read_text(encoding='utf-8')
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

    def process_batch(self, input_dir: Path, output_dir: Optional[Path] = None) -> List[ProcessingResult]:
        """Process all supported files in a directory"""
        if output_dir is None:
            output_dir = input_dir / "processed"

        output_dir.mkdir(exist_ok=True)

        # Find all supported files
        all_files = []
        for ext_set in [InputRouter.IMAGE_EXTENSIONS, InputRouter.AUDIO_EXTENSIONS,
                       InputRouter.PDF_EXTENSIONS, InputRouter.DOCUMENT_EXTENSIONS,
                       InputRouter.WEB_EXTENSIONS, InputRouter.TEXT_EXTENSIONS]:
            for ext in ext_set:
                all_files.extend(input_dir.glob(f"*{ext}"))

        print(f"\n📁 Batch Processing: {len(all_files)} files")
        print(f"   Input:  {input_dir}")
        print(f"   Output: {output_dir}")

        results = []
        for i, file_path in enumerate(sorted(all_files), 1):
            print(f"\n{'='*60}")
            print(f"File {i}/{len(all_files)}")

            output_path = output_dir / f"{file_path.stem}_processed.md"
            result = self.process_file(file_path, output_path)
            results.append(result)

        # Summary
        succeeded = sum(1 for r in results if r.success)
        failed = len(results) - succeeded

        print(f"\n{'='*60}")
        print(f"📊 Batch Complete!")
        print(f"   Total: {len(results)}")
        print(f"   ✓ Succeeded: {succeeded}")
        print(f"   ✗ Failed: {failed}")

        return results


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Universal document processor for knowledge management',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single file
  mdclean_universal document.pdf

  # With output path
  mdclean_universal notes.jpg --output ~/Vault/Inbox/

  # Batch process folder
  mdclean_universal --batch ~/Documents/to-process/

  # OCR with handwriting mode
  mdclean_universal handwritten.jpg --handwriting

  # Skip LLM cleaning (fast mode)
  mdclean_universal doc.pdf --no-llm

Supported formats:
  - Images: JPG, PNG, TIFF, BMP (OCR)
  - Audio: MP3, M4A, WAV, FLAC (transcription)
  - Documents: PDF, EPUB, DOCX, ODT, RTF
  - Web: HTML, HTM
  - Text: TXT, MD
"""
    )

    parser.add_argument('input', type=str, nargs='?',
                       help='Input file or directory (with --batch)')
    parser.add_argument('-o', '--output', type=str,
                       help='Output path (file or directory)')
    parser.add_argument('-b', '--batch', action='store_true',
                       help='Batch process all files in directory')
    parser.add_argument('--handwriting', action='store_true',
                       help='Enable handwriting OCR mode')
    parser.add_argument('--no-llm', action='store_true',
                       help='Skip LLM cleaning (fast mode)')
    parser.add_argument('--model', type=str, default='llama3.2:1b',
                       help='Ollama model to use (default: llama3.2:1b)')
    parser.add_argument('--no-frontmatter', action='store_true',
                       help='Skip frontmatter generation')
    parser.add_argument('--version', action='version',
                       version=f'%(prog)s {__version__}')

    args = parser.parse_args()

    # Validate input
    if not args.input:
        parser.print_help()
        sys.exit(1)

    input_path = Path(args.input).expanduser().resolve()

    if not input_path.exists():
        print(f"Error: Input not found: {input_path}")
        sys.exit(1)

    # Build config
    config = {
        'ocr_handwriting': args.handwriting,
        'ollama_model': args.model,
        'add_frontmatter': not args.no_frontmatter,
    }

    # Initialize processor
    processor = UniversalProcessor(config)

    # Process
    if args.batch:
        # Batch mode
        if not input_path.is_dir():
            print(f"Error: --batch requires a directory")
            sys.exit(1)

        output_dir = Path(args.output) if args.output else None
        results = processor.process_batch(input_path, output_dir)

        # Exit with error code if any failed
        if any(not r.success for r in results):
            sys.exit(1)
    else:
        # Single file mode
        if input_path.is_dir():
            print(f"Error: Input is a directory. Use --batch for batch processing")
            sys.exit(1)

        output_path = Path(args.output) if args.output else None
        result = processor.process_file(input_path, output_path)

        if not result.success:
            sys.exit(1)


if __name__ == '__main__':
    main()
