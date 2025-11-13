#!/usr/bin/env python3
"""
Enhanced transcription with dual-mode support:
  - Vosk for English (fast, CPU-efficient)
  - Whisper for multilingual (accurate, includes Afrikaans)

Usage:
  # English with Vosk (fast)
  python transcribe_enhanced.py single input.mp3 --engine vosk --outdir ./out

  # Afrikaans with Whisper
  python transcribe_enhanced.py single input.m4a --engine whisper --language af --outdir ./out

  # Auto-detect and use best engine
  python transcribe_enhanced.py single input.mp3 --engine auto --outdir ./out

  # Batch processing
  python transcribe_enhanced.py batch /path/to/files --engine whisper --outdir ./out
"""
from pathlib import Path
import subprocess
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, List, Tuple
import typer
from rich.progress import Progress
from rich.console import Console

app = typer.Typer()
console = Console()

# ============================================================================
# VOSK ENGINE
# ============================================================================

def transcribe_vosk(
    mp3_path: Path,
    model_path: Optional[Path] = None,
    timestamps: bool = False
) -> List[dict]:
    """
    Transcribe using Vosk (English only, fast, CPU-friendly).

    Returns list of segments with {text, start, end} fields.
    """
    try:
        from vosk import Model, KaldiRecognizer
    except ImportError:
        console.print("[red]Error: vosk not installed. Run: pip install vosk[/red]")
        sys.exit(1)

    if model_path is None:
        model_path = Path.home() / ".cache" / "vosk-model-en-us-0.22"

    if not model_path.exists():
        console.print(f"[red]Error: Vosk model not found at {model_path}[/red]")
        console.print("[yellow]Download from: https://alphacephei.com/vosk/models[/yellow]")
        sys.exit(1)

    console.print(f"[blue]Loading Vosk model from {model_path}...[/blue]")
    model = Model(str(model_path))

    # Stream through ffmpeg
    console.print("[blue]Starting ffmpeg stream...[/blue]")
    proc = subprocess.Popen([
        "ffmpeg",
        "-hide_banner", "-loglevel", "warning",
        "-i", str(mp3_path),
        "-ac", "1",
        "-ar", "16000",
        "-f", "s16le",
        "-acodec", "pcm_s16le",
        "-"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    rec = KaldiRecognizer(model, 16000)
    rec.SetWords(True)

    segments = []
    CHUNK_BYTES = 4000 * 2  # ~0.25s per chunk

    while True:
        chunk = proc.stdout.read(CHUNK_BYTES)
        if not chunk:
            break

        if rec.AcceptWaveform(chunk):
            res = json.loads(rec.Result())
            if 'result' in res and res['result']:
                segments.extend(res['result'])

    # Get final result
    final_res = json.loads(rec.FinalResult())
    if 'result' in final_res and final_res['result']:
        segments.extend(final_res['result'])

    proc.wait()

    return segments


# ============================================================================
# WHISPER ENGINE
# ============================================================================

def transcribe_whisper(
    audio_path: Path,
    language: Optional[str] = None,
    model_size: str = "base",
    timestamps: bool = False
) -> List[dict]:
    """
    Transcribe using faster-whisper (multilingual, optimized, accurate).

    Args:
        audio_path: Path to audio file (mp3, m4a, wav, etc.)
        language: Language code (en, af, nl, etc.) or None for auto-detect
        model_size: tiny, base, small, medium, large (larger = better quality but slower)
        timestamps: Whether to include word-level timestamps

    Returns list of segments with {text, start, end} fields.
    """
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        console.print("[red]Error: faster-whisper not installed. Run: pip install faster-whisper[/red]")
        sys.exit(1)

    console.print(f"[blue]Loading Whisper model ({model_size})...[/blue]")
    # Use CPU for 8GB RAM systems
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    console.print(f"[blue]Transcribing with Whisper (language: {language or 'auto-detect'})...[/blue]")

    # Transcribe
    segments_iter, info = model.transcribe(
        str(audio_path),
        language=language,
        word_timestamps=timestamps,
        vad_filter=True,  # Voice activity detection for better accuracy
    )

    console.print(f"[yellow]Detected language: {info.language} (probability: {info.language_probability:.2f})[/yellow]")

    # Convert to our format
    segments = []

    for seg in segments_iter:
        if timestamps and hasattr(seg, 'words') and seg.words:
            # Word-level timestamps
            for word in seg.words:
                segments.append({
                    'word': word.word.strip(),
                    'start': word.start,
                    'end': word.end
                })
        else:
            # Segment-level only
            segments.append({
                'word': seg.text.strip(),
                'start': seg.start,
                'end': seg.end
            })

    return segments


# ============================================================================
# OUTPUT FORMATTING
# ============================================================================

def format_timestamp(seconds: float) -> str:
    """Convert seconds to HH:MM:SS format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def segments_to_markdown(
    segments: List[dict],
    source_file: str,
    timestamps: bool = False,
    window_seconds: int = 30
) -> str:
    """
    Convert segments to formatted markdown.

    Groups text into time-based windows and creates paragraphs.
    """
    # Build frontmatter
    frontmatter = f"---\nsource: {source_file}\n---\n\n"

    if not segments:
        return frontmatter + "(no transcription generated)"

    # Group into time windows
    lines = []
    current_window_start = 0
    current_window_text = []

    for seg in segments:
        word = seg.get('word', '')
        if not word:
            continue

        start = seg.get('start', 0)

        # Check if we should start a new window
        if timestamps and start - current_window_start >= window_seconds:
            if current_window_text:
                timestamp = format_timestamp(current_window_start)
                text = ' '.join(current_window_text)
                lines.append(f"[{timestamp}] {text}\n")
                current_window_text = []
            current_window_start = start

        current_window_text.append(word)

    # Add final window
    if current_window_text:
        if timestamps:
            timestamp = format_timestamp(current_window_start)
            text = ' '.join(current_window_text)
            lines.append(f"[{timestamp}] {text}\n")
        else:
            text = ' '.join(current_window_text)
            lines.append(f"{text}\n")

    return frontmatter + ''.join(lines)


# ============================================================================
# MAIN COMMANDS
# ============================================================================

@app.command()
def single(
    input_file: Path = typer.Argument(..., help="Audio file to transcribe"),
    outdir: Path = typer.Option("./transcriptions", help="Output directory"),
    engine: str = typer.Option("auto", help="Engine: vosk, whisper, or auto"),
    language: Optional[str] = typer.Option(None, help="Language code (e.g., en, af, nl) - Whisper only"),
    model: Optional[str] = typer.Option(None, help="Model: Vosk path or Whisper size (tiny/base/small/medium/large)"),
    timestamps: bool = typer.Option(False, help="Include timestamps in output"),
):
    """Transcribe a single audio file."""

    if not input_file.exists():
        console.print(f"[red]Error: File not found: {input_file}[/red]")
        sys.exit(1)

    outdir.mkdir(parents=True, exist_ok=True)

    # Determine engine
    if engine == "auto":
        # If language is specified and not English, use Whisper
        if language and language != "en":
            engine = "whisper"
            console.print(f"[yellow]Auto-selected Whisper for language: {language}[/yellow]")
        else:
            # Default to Vosk for English
            engine = "vosk"
            console.print("[yellow]Auto-selected Vosk for English[/yellow]")

    # Transcribe
    if engine == "vosk":
        model_path = Path(model) if model else None
        segments = transcribe_vosk(input_file, model_path, timestamps)
    elif engine == "whisper":
        model_size = model or "base"
        segments = transcribe_whisper(input_file, language, model_size, timestamps)
    else:
        console.print(f"[red]Error: Unknown engine: {engine}[/red]")
        sys.exit(1)

    # Format output
    output_file = outdir / f"{input_file.stem}.md"
    markdown = segments_to_markdown(
        segments,
        input_file.name,
        timestamps=timestamps
    )

    output_file.write_text(markdown)

    console.print(f"[green]✅ Transcription saved to: {output_file}[/green]")
    console.print(f"   Words: {len([s for s in segments if s.get('word')])}")


@app.command()
def batch(
    input_dir: Path = typer.Argument(..., help="Directory containing audio files"),
    outdir: Path = typer.Option("./transcriptions", help="Output directory"),
    engine: str = typer.Option("auto", help="Engine: vosk, whisper, or auto"),
    language: Optional[str] = typer.Option(None, help="Language code - Whisper only"),
    model: Optional[str] = typer.Option(None, help="Model path or size"),
    timestamps: bool = typer.Option(False, help="Include timestamps"),
    concurrency: int = typer.Option(1, help="Number of files to process in parallel"),
):
    """Transcribe multiple audio files in a directory."""

    if not input_dir.exists():
        console.print(f"[red]Error: Directory not found: {input_dir}[/red]")
        sys.exit(1)

    # Find audio files
    audio_files = []
    for ext in ['*.mp3', '*.m4a', '*.wav', '*.flac']:
        audio_files.extend(input_dir.glob(ext))

    if not audio_files:
        console.print(f"[yellow]No audio files found in {input_dir}[/yellow]")
        sys.exit(0)

    console.print(f"[blue]Found {len(audio_files)} audio files[/blue]")
    outdir.mkdir(parents=True, exist_ok=True)

    # Process in parallel
    with Progress() as progress:
        task = progress.add_task(f"[blue]Transcribing...", total=len(audio_files))

        def process_file(audio_file: Path):
            # Determine engine
            selected_engine = engine
            if selected_engine == "auto":
                selected_engine = "whisper" if language and language != "en" else "vosk"

            # Transcribe
            try:
                if selected_engine == "vosk":
                    model_path = Path(model) if model else None
                    segments = transcribe_vosk(audio_file, model_path, timestamps)
                else:
                    model_size = model or "base"
                    segments = transcribe_whisper(audio_file, language, model_size, timestamps)

                # Save
                output_file = outdir / f"{audio_file.stem}.md"
                markdown = segments_to_markdown(segments, audio_file.name, timestamps)
                output_file.write_text(markdown)

                return (audio_file.name, True, None)
            except Exception as e:
                return (audio_file.name, False, str(e))

        with ThreadPoolExecutor(max_workers=concurrency) as executor:
            futures = [executor.submit(process_file, f) for f in audio_files]

            success_count = 0
            for future in as_completed(futures):
                filename, success, error = future.result()
                if success:
                    success_count += 1
                else:
                    console.print(f"[red]Failed: {filename} - {error}[/red]")
                progress.advance(task)

    console.print(f"[green]✅ Completed: {success_count}/{len(audio_files)} files[/green]")


if __name__ == "__main__":
    app()
