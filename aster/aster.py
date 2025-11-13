#!/usr/bin/env python3
"""
aster - Navigate your constellation of knowledge

"Lost in a night-sky of notes? Aster lights the way."

Transforms any document into structured, connected knowledge:
- Images (OCR with Tesseract/PaddleOCR)
- Audio (transcription with Vosk)
- Documents (PDF, EPUB, DOCX, PPTX, HTML)
- Data (CSV, Excel with AI analysis)
- Text (TXT, MD)

Pipeline: Extract → Structure → Clean (Ollama) → Connect → Navigate

Usage:
    aster document.pdf
    aster image.jpg --output ~/Vault/Inbox/
    aster --batch ~/Documents/to-process/
    aster --web  # Start web interface for iPhone access
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
    AUDIO_EXTENSIONS = {'.mp3', '.m4a', '.wav', '.flac', '.ogg', '.wma'}
    PDF_EXTENSIONS = {'.pdf'}
    DOCUMENT_EXTENSIONS = {'.epub', '.docx', '.odt', '.rtf', '.pptx', '.ppt'}
    WEB_EXTENSIONS = {'.html', '.htm', '.mhtml'}
    TEXT_EXTENSIONS = {'.txt', '.md', '.markdown'}
    CSV_EXTENSIONS = {'.csv', '.xlsx', '.xls'}

    @classmethod
    def detect_type(cls, file_path: Path) -> str:
        """
        Detect input type based on file extension.

        Returns: 'image', 'audio', 'pdf', 'document', 'web', 'text', or 'csv'
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
        elif extension in cls.CSV_EXTENSIONS:
            return 'csv'
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

    def convert_audio_format(self, audio_path: Path, target_format: str = 'wav') -> Path:
        """
        Convert audio to target format using ffmpeg.
        Useful for .wma and other less common formats.
        Returns: Path to converted file
        """
        try:
            # Check if ffmpeg is available
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise RuntimeError("ffmpeg not installed. Install with: brew install ffmpeg (Mac) or apt-get install ffmpeg (Linux)")

        # Create temp file for converted audio
        temp_dir = Path(tempfile.gettempdir())
        converted_path = temp_dir / f"{audio_path.stem}_converted.{target_format}"

        # Convert using ffmpeg
        subprocess.run([
            'ffmpeg', '-i', str(audio_path),
            '-ar', '16000',  # 16kHz sample rate (good for speech)
            '-ac', '1',       # Mono channel
            str(converted_path),
            '-y'              # Overwrite if exists
        ], capture_output=True, check=True)

        return converted_path

    def _get_audio_duration(self, audio_path: Path) -> float:
        """Get audio duration in seconds using ffprobe"""
        try:
            import json
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                str(audio_path)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)
            return float(data['format']['duration'])
        except Exception as e:
            print(f"  Warning: Could not get audio duration: {e}")
            return 0

    def _split_audio_into_chunks(self, audio_path: Path, chunk_minutes: int = 5) -> list:
        """Split large audio file into smaller chunks for parallel processing"""
        duration = self._get_audio_duration(audio_path)
        chunk_seconds = chunk_minutes * 60
        num_chunks = int(duration / chunk_seconds) + 1

        print(f"  Splitting {duration/60:.1f} min audio into {num_chunks} chunks...")

        chunks = []
        chunk_dir = Path(tempfile.gettempdir()) / f"{audio_path.stem}_chunks"
        chunk_dir.mkdir(exist_ok=True)

        for i in range(num_chunks):
            start_time = i * chunk_seconds
            chunk_path = chunk_dir / f"chunk_{i:03d}.wav"

            # Extract chunk with ffmpeg
            cmd = [
                'ffmpeg',
                '-i', str(audio_path),
                '-ss', str(start_time),
                '-t', str(chunk_seconds),
                '-ar', '16000',  # 16kHz for Vosk
                '-ac', '1',       # Mono
                '-y',
                str(chunk_path)
            ]

            subprocess.run(cmd, capture_output=True, check=True)
            chunks.append((chunk_path, start_time, i))
            print(f"    Chunk {i+1}/{num_chunks} created")

        return chunks

    def _transcribe_single_file(self, audio_path: Path) -> str:
        """Transcribe a single audio file with Vosk"""
        try:
            import vosk
            import wave
            import json

            # Download model if not exists
            model_name = "vosk-model-small-en-us-0.15"
            model_path = Path.home() / ".cache" / "vosk" / model_name

            if not model_path.exists():
                print(f"  Downloading Vosk model {model_name}...")
                model = vosk.Model(model_name=model_name)
            else:
                model = vosk.Model(str(model_path))

            # Open audio file
            wf = wave.open(str(audio_path), "rb")

            # Check audio format
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
                print(f"  Warning: Audio format not optimal. Expected: 16kHz, mono, 16-bit")

            # Create recognizer
            rec = vosk.KaldiRecognizer(model, wf.getframerate())
            rec.SetWords(True)

            # Transcribe
            results = []
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    if 'text' in result and result['text']:
                        results.append(result['text'])

            # Get final result
            final = json.loads(rec.FinalResult())
            if 'text' in final and final['text']:
                results.append(final['text'])

            wf.close()
            return ' '.join(results)

        except Exception as e:
            raise RuntimeError(f"Vosk transcription failed: {e}")

    def _transcribe_chunk_worker(self, chunk_info: tuple) -> dict:
        """Worker function for parallel transcription"""
        chunk_path, start_time, chunk_num = chunk_info
        try:
            text = self._transcribe_single_file(chunk_path)
            return {
                'chunk_num': chunk_num,
                'start_time': start_time,
                'text': text,
                'success': True
            }
        except Exception as e:
            return {
                'chunk_num': chunk_num,
                'start_time': start_time,
                'text': '',
                'success': False,
                'error': str(e)
            }

    def _transcribe_chunks_parallel(self, chunks: list, max_workers: int = 4) -> str:
        """Transcribe audio chunks in parallel"""
        from concurrent.futures import ProcessPoolExecutor, as_completed

        results = []
        total_chunks = len(chunks)

        print(f"  Transcribing {total_chunks} chunks with {max_workers} workers...")

        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            # Submit all chunks
            futures = {
                executor.submit(self._transcribe_single_file, chunk[0]): chunk
                for chunk in chunks
            }

            # Process as they complete
            completed = 0
            for future in as_completed(futures):
                chunk_info = futures[future]
                chunk_path, start_time, chunk_num = chunk_info

                try:
                    text = future.result()
                    completed += 1
                    results.append({
                        'chunk_num': chunk_num,
                        'start_time': start_time,
                        'text': text
                    })
                    print(f"    Chunk {completed}/{total_chunks} complete ({completed/total_chunks*100:.0f}%)")
                except Exception as e:
                    print(f"    Chunk {chunk_num} failed: {e}")
                    completed += 1

        # Sort by chunk number and reassemble
        results.sort(key=lambda x: x['chunk_num'])

        # Format with timestamps
        formatted_parts = []
        for result in results:
            minutes = int(result['start_time'] // 60)
            seconds = int(result['start_time'] % 60)
            timestamp = f"[{minutes:02d}:{seconds:02d}]"
            formatted_parts.append(f"{timestamp} {result['text']}")

        # Cleanup chunk files
        try:
            chunk_dir = chunks[0][0].parent
            for chunk_path, _, _ in chunks:
                chunk_path.unlink(missing_ok=True)
            chunk_dir.rmdir()
        except Exception as e:
            print(f"  Warning: Could not cleanup chunks: {e}")

        return '\n\n'.join(formatted_parts)

    def extract_text(self, audio_path: Path) -> str:
        """
        Transcribe audio file with Vosk.
        Automatically chunks large files for parallel processing.
        Returns: Transcribed text
        """
        # Convert to WAV format if needed
        if audio_path.suffix.lower() != '.wav':
            print(f"  Converting {audio_path.suffix} to .wav...")
            audio_path = self.convert_audio_format(audio_path, 'wav')

        # Get duration
        duration = self._get_audio_duration(audio_path)
        print(f"  Audio duration: {duration/60:.1f} minutes")

        # Decide on processing strategy
        if duration > 600:  # > 10 minutes
            print(f"  Large audio file detected, using parallel chunking...")
            chunks = self._split_audio_into_chunks(audio_path, chunk_minutes=5)
            transcript = self._transcribe_chunks_parallel(chunks, max_workers=4)
        else:
            print(f"  Transcribing with Vosk...")
            transcript = self._transcribe_single_file(audio_path)

        return transcript


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
        """Extract text from PDF using Unstructured for better structure, fallback to pdftotext"""

        # Check if scanned
        if self.is_scanned_pdf(pdf_path):
            print("  Detected scanned PDF, using OCR...")
            return self.extract_scanned_pdf(pdf_path)

        # Try Unstructured first for better structure preservation
        try:
            from unstructured.partition.pdf import partition_pdf
            print("  Using Unstructured library for better PDF structure...")

            elements = partition_pdf(filename=str(pdf_path))

            text_parts = []
            for elem in elements:
                elem_type = elem.__class__.__name__
                elem_text = str(elem).strip()

                if not elem_text:
                    continue

                # Add markers for structure detection
                if elem_type == 'Title':
                    text_parts.append(f"\n## {elem_text}\n")
                elif elem_type == 'ListItem':
                    text_parts.append(f"- {elem_text}")
                else:
                    text_parts.append(elem_text)

            return '\n\n'.join(text_parts)

        except ImportError:
            print("  Unstructured library not available, using pdftotext...")
        except Exception as e:
            print(f"  Warning: Unstructured PDF parsing failed ({e}), falling back to pdftotext...")

        # Fallback to pdftotext
        if not self.check_dependencies('pdf'):
            raise RuntimeError("pdftotext not installed. Install with: brew install poppler")

        print("  Using pdftotext for extraction...")

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
        """
        Extract text from DOCX, PPTX, EPUB using Unstructured library for better structure preservation.
        Falls back to pandoc for unsupported formats.
        """
        extension = doc_path.suffix.lower()

        # Try to use Unstructured for structured parsing (preserves document structure)
        try:
            if extension == '.docx':
                # Use Unstructured for DOCX - preserves titles, paragraphs, lists
                try:
                    from unstructured.partition.docx import partition_docx
                    print("  Using Unstructured library for better structure detection...")
                    elements = partition_docx(filename=str(doc_path))

                    # Convert elements to text with basic structure markers
                    text_parts = []
                    for elem in elements:
                        elem_type = elem.__class__.__name__
                        elem_text = str(elem).strip()

                        if not elem_text:
                            continue

                        # Add markers for structure detection
                        if elem_type == 'Title':
                            text_parts.append(f"\n## {elem_text}\n")
                        elif elem_type == 'ListItem':
                            text_parts.append(f"- {elem_text}")
                        else:
                            text_parts.append(elem_text)

                    return '\n\n'.join(text_parts)
                except ImportError:
                    print("  Unstructured library not available, falling back to pandoc...")

            elif extension == '.pptx' or extension == '.ppt':
                # Use Unstructured for PowerPoint - preserves slide structure
                try:
                    from unstructured.partition.pptx import partition_pptx
                    print("  Using Unstructured library for PowerPoint slide structure...")
                    elements = partition_pptx(filename=str(doc_path))

                    text_parts = []
                    for elem in elements:
                        elem_type = elem.__class__.__name__
                        elem_text = str(elem).strip()

                        if not elem_text:
                            continue

                        if elem_type == 'Title':
                            text_parts.append(f"\n## {elem_text}\n")
                        elif elem_type == 'ListItem':
                            text_parts.append(f"- {elem_text}")
                        else:
                            text_parts.append(elem_text)

                    return '\n\n'.join(text_parts)
                except ImportError:
                    print("  Unstructured library not available, falling back to pandoc...")

            elif extension == '.epub':
                # Use Unstructured for EPUB
                try:
                    from unstructured.partition.epub import partition_epub
                    print("  Using Unstructured library for EPUB structure...")
                    elements = partition_epub(filename=str(doc_path))

                    text_parts = []
                    for elem in elements:
                        elem_type = elem.__class__.__name__
                        elem_text = str(elem).strip()

                        if not elem_text:
                            continue

                        if elem_type == 'Title':
                            text_parts.append(f"\n## {elem_text}\n")
                        elif elem_type == 'ListItem':
                            text_parts.append(f"- {elem_text}")
                        else:
                            text_parts.append(elem_text)

                    return '\n\n'.join(text_parts)
                except ImportError:
                    print("  Unstructured library not available, falling back to pandoc...")

        except Exception as e:
            print(f"  Warning: Unstructured parsing failed ({e}), falling back to pandoc...")

        # Fallback to pandoc for compatibility
        if not self.check_dependencies('document'):
            raise RuntimeError("pandoc not installed. Install with: brew install pandoc")

        print("  Using pandoc for text extraction...")

        # Detect format for pandoc
        if extension == '.epub':
            from_format = 'epub'
        elif extension == '.docx':
            from_format = 'docx'
        elif extension == '.odt':
            from_format = 'odt'
        elif extension == '.rtf':
            from_format = 'rtf'
        elif extension in ['.pptx', '.ppt']:
            from_format = 'pptx'
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
        """Extract text from HTML using Unstructured, fallback to pandoc"""

        # Try Unstructured first for better structure
        try:
            from unstructured.partition.html import partition_html
            print("  Using Unstructured library for HTML structure...")

            elements = partition_html(filename=str(html_path))

            text_parts = []
            for elem in elements:
                elem_type = elem.__class__.__name__
                elem_text = str(elem).strip()

                if not elem_text:
                    continue

                if elem_type == 'Title':
                    text_parts.append(f"\n## {elem_text}\n")
                elif elem_type == 'ListItem':
                    text_parts.append(f"- {elem_text}")
                else:
                    text_parts.append(elem_text)

            return '\n\n'.join(text_parts)

        except ImportError:
            print("  Unstructured library not available, using pandoc...")
        except Exception as e:
            print(f"  Warning: Unstructured HTML parsing failed ({e}), falling back to pandoc...")

        # Fallback to pandoc
        if not self.check_dependencies('web'):
            raise RuntimeError("pandoc not installed. Install with: brew install pandoc")

        print("  Using pandoc for extraction...")

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
# CSV Handler
# ============================================================================

class CSVHandler:
    """Handle CSV to Markdown conversion with financial analysis"""

    def __init__(self, csv_mode='auto'):
        self.csv_mode = csv_mode
        try:
            import csv
            import re
            self.csv = csv
            self.re = re
        except ImportError:
            print("CSV support requires standard library csv module")

    def parse_amount(self, value: str) -> float:
        """Parse amount string to float"""
        if not value or value.strip() == '':
            return 0.0
        import re
        cleaned = re.sub(r'[,$€£¥]', '', value.strip())
        if cleaned.startswith('(') and cleaned.endswith(')'):
            cleaned = '-' + cleaned[1:-1]
        try:
            return float(cleaned)
        except ValueError:
            return 0.0

    def format_amount(self, amount: float) -> str:
        """Format amount for display"""
        if amount < 0:
            return f"-${abs(amount):,.2f}"
        else:
            return f"${amount:,.2f}"

    def detect_csv_type(self, headers: List[str]) -> str:
        """Auto-detect CSV type based on headers"""
        headers_lower = [h.lower() for h in headers]

        if any(x in headers_lower for x in ['amount', 'transaction', 'description', 'date']):
            return 'financial'
        elif any(x in headers_lower for x in ['budgeted', 'actual', 'variance']):
            return 'budget'
        elif any(x in headers_lower for x in ['shares', 'cost_basis', 'current_value']):
            return 'portfolio'
        return 'generic'

    def analyze_financial_transactions(self, headers: List[str], rows: List[List[str]]) -> Dict[str, Any]:
        """Analyze financial transactions"""
        headers_lower = [h.lower() for h in headers]

        date_idx = next((i for i, h in enumerate(headers_lower) if 'date' in h), 0)
        desc_idx = next((i for i, h in enumerate(headers_lower) if 'desc' in h), 1)
        amount_idx = next((i for i, h in enumerate(headers_lower) if 'amount' in h), 2)
        category_idx = next((i for i, h in enumerate(headers_lower) if 'category' in h or 'cat' in h), None)

        total_income = 0.0
        total_expenses = 0.0
        category_totals = {}
        running_balance = 0.0
        transactions = []

        for row in rows:
            if len(row) <= amount_idx:
                continue

            amount = self.parse_amount(row[amount_idx])
            category = row[category_idx] if category_idx and len(row) > category_idx else 'Uncategorized'

            if amount > 0:
                total_income += amount
            else:
                total_expenses += abs(amount)

            if category not in category_totals:
                category_totals[category] = 0.0
            category_totals[category] += amount

            running_balance += amount

            transactions.append({
                'date': row[date_idx] if len(row) > date_idx else '',
                'description': row[desc_idx] if len(row) > desc_idx else '',
                'amount': amount,
                'category': category,
                'balance': running_balance
            })

        net = total_income - total_expenses

        return {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net': net,
            'category_totals': category_totals,
            'transactions': transactions
        }

    def convert_csv_to_markdown(self, csv_path: Path) -> tuple[str, Optional[str]]:
        """Convert CSV/Excel to markdown with analysis"""
        import csv

        # Handle Excel files (.xlsx, .xls)
        if csv_path.suffix.lower() in ['.xlsx', '.xls']:
            try:
                import pandas as pd
                # Read Excel file (first sheet)
                df = pd.read_excel(csv_path)
                headers = df.columns.tolist()
                rows = df.values.tolist()
                # Convert to strings
                headers = [str(h) for h in headers]
                rows = [[str(cell) if cell is not None else '' for cell in row] for row in rows]
            except ImportError:
                raise RuntimeError("Excel support requires pandas and openpyxl. Install with: pip install pandas openpyxl")
        else:
            # Read CSV
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                headers = next(reader)
                rows = list(reader)

        # Detect type
        csv_type = self.detect_csv_type(headers) if self.csv_mode == 'auto' else self.csv_mode

        # Analyze
        analysis = None
        if csv_type == 'financial':
            analysis = self.analyze_financial_transactions(headers, rows)

        # Build markdown
        content = []
        title = csv_path.stem.replace('_', ' ').replace('-', ' ').title()
        content.append(f"# {title}\n")

        # Summary
        if analysis and csv_type == 'financial':
            content.append("## Summary\n")
            content.append(f"**Total Income:** {self.format_amount(analysis['total_income'])}")
            content.append(f"**Total Expenses:** {self.format_amount(analysis['total_expenses'])}")
            content.append(f"**Net:** {self.format_amount(analysis['net'])}\n")
            content.append("**Category Breakdown:**")
            for category, total in sorted(analysis['category_totals'].items(), key=lambda x: x[1], reverse=True):
                content.append(f"- {category}: {self.format_amount(total)}")
            content.append("")

        # Transactions table
        if analysis and csv_type == 'financial':
            content.append("## Transactions\n")
            content.append("| Date | Description | Amount | Category | Balance |")
            content.append("|---|---|---|---|---|")
            for trans in analysis['transactions']:
                content.append(f"| {trans['date']} | {trans['description']} | {self.format_amount(trans['amount'])} | {trans['category']} | {self.format_amount(trans['balance'])} |")
            content.append("")

        # AI analysis placeholder
        content.append("## AI Analysis\n")
        content.append("[Analysis will be added by Ollama...]\n")

        # Math notes
        if analysis and csv_type == 'financial':
            content.append("## Math Notes\n")
            content.append(f"Total income: `$= {analysis['total_income']:.2f}`")
            content.append(f"Total expenses: `$= {analysis['total_expenses']:.2f}`")
            content.append(f"Net: `$= {analysis['net']:.2f}`")
            content.append(f"Savings rate: `$= ({analysis['net']:.2f} / {analysis['total_income']:.2f}) * 100`%")

        # Generate AI prompt
        ai_prompt = None
        if analysis and csv_type == 'financial':
            ai_prompt = f"""Analyze this financial data and provide insights:

Total Income: {self.format_amount(analysis['total_income'])}
Total Expenses: {self.format_amount(analysis['total_expenses'])}
Net: {self.format_amount(analysis['net'])}

Category spending:
{chr(10).join([f"- {cat}: {self.format_amount(amt)}" for cat, amt in analysis['category_totals'].items()])}

Provide:
1. Key insights about spending patterns
2. Recommendations for improvement
3. Any concerning trends
4. Savings suggestions

Keep response concise and actionable."""

        return '\n'.join(content), ai_prompt


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
        self.csv_handler = CSVHandler(
            csv_mode=self.config.get('csv_mode', 'auto')
        )
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

            # CSV files use a different pipeline
            if file_type == 'csv':
                return self._process_csv_file(input_path, output_path, start_time)

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

    def _process_csv_file(self, input_path: Path, output_path: Optional[Path], start_time: datetime) -> ProcessingResult:
        """Special pipeline for CSV files with automatic AI analysis"""
        try:
            # STEP 1: Convert CSV to markdown
            print("\n1️⃣  Converting CSV to markdown...")
            markdown_content, ai_prompt = self.csv_handler.convert_csv_to_markdown(input_path)
            print(f"   ✓ Converted to markdown")

            # STEP 2: Add frontmatter
            print("\n2️⃣  Adding metadata...")
            metadata = DocumentMetadata(
                source_file=input_path.name,
                file_type='csv',
                date_processed=datetime.now().isoformat(),
                original_size=input_path.stat().st_size,
                tags=['csv', 'financial']
            )

            frontmatter = f"""---
source: {metadata.source_file}
date_processed: {metadata.date_processed}
type: {metadata.file_type}
tags: {metadata.tags}
---

"""
            markdown_content = frontmatter + markdown_content
            print(f"   ✓ Metadata added")

            # STEP 3: Automatic AI analysis (if enabled and prompt available)
            if ai_prompt and self.config.get('analyze', False):
                print("\n3️⃣  Getting AI analysis from Ollama...")
                try:
                    import ollama
                    response = ollama.generate(
                        model=self.config.get('ollama_model', 'llama3.2:1b'),
                        prompt=ai_prompt,
                        options={'temperature': 0.2}
                    )
                    ai_analysis = response['response'].strip()

                    # Replace placeholder with actual analysis
                    markdown_content = markdown_content.replace(
                        "[Analysis will be added by Ollama...]",
                        ai_analysis
                    )
                    print(f"   ✓ AI analysis complete")

                except Exception as e:
                    print(f"   ⚠️  Ollama analysis failed: {e}")
                    print(f"   Keeping placeholder - you can add analysis manually")

            # STEP 4: Save output
            if output_path is None:
                output_path = input_path.parent / f"{input_path.stem}_processed.md"

            output_path.write_text(markdown_content, encoding='utf-8')

            processing_time = (datetime.now() - start_time).total_seconds()

            print(f"\n✅ Success! Saved to: {output_path}")
            print(f"   Processing time: {processing_time:.1f}s")

            if ai_prompt and not self.config.get('analyze', False):
                print(f"\n💡 Tip: Use --analyze flag to automatically call Ollama for AI insights")

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
                       InputRouter.WEB_EXTENSIONS, InputRouter.TEXT_EXTENSIONS,
                       InputRouter.CSV_EXTENSIONS]:
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

  # CSV with automatic AI analysis
  mdclean_universal transactions.csv --analyze
  mdclean_universal budget.csv --csv-mode budget --analyze

Supported formats:
  - Images: JPG, PNG, TIFF, BMP (OCR)
  - Audio: MP3, M4A, WAV, FLAC (transcription)
  - Documents: PDF, EPUB, DOCX, ODT, RTF
  - Web: HTML, HTM
  - Text: TXT, MD
  - CSV: Financial data with AI analysis
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
    parser.add_argument('--analyze', action='store_true',
                       help='Automatically run AI analysis with Ollama (for CSV files)')
    parser.add_argument('--csv-mode', type=str, choices=['auto', 'financial', 'budget', 'portfolio', 'debt'],
                       default='auto', help='CSV type detection mode (default: auto)')
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
        'analyze': args.analyze,
        'csv_mode': args.csv_mode,
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
