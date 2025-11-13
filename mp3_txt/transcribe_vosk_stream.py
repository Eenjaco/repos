#!/usr/bin/env python3
"""
Streaming MP3 -> timestamped Markdown using Vosk (minimal memory).
Usage:
  python transcribe_vosk_stream.py single input.mp3 --outdir ./out
  python transcribe_vosk_stream.py batch /path/to/mp3_dir --outdir ./out --concurrency 1
"""
from pathlib import Path
import subprocess
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import typer
from vosk import Model, KaldiRecognizer
from rich.progress import Progress

app = typer.Typer()

# Adjust to where you unpack the Vosk model
# Using large model (vosk-model-en-us-0.22) for better accuracy
DEFAULT_MODEL_PATH = Path.home() / ".cache" / "vosk-model-en-us-0.22"

# ffmpeg parameters to output raw PCM 16bit LE mono 16kHz
FFMPEG_CMD = [
    "ffmpeg",
    "-hide_banner", "-loglevel", "error",
    "-i", "-",           # replace with input file later
    "-ac", "1",
    "-ar", "16000",
    "-f", "s16le",
    "-acodec", "pcm_s16le",
    "-"
]

def ffmpeg_stream(mp3_path: Path):
    """Spawn ffmpeg to output raw PCM to stdout and return the process."""
    # Resolve path and ensure it's a proper string without newlines
    resolved_path = mp3_path.resolve()
    path_str = str(resolved_path).replace('\n', '').replace('\r', '').strip()

    # Verify file exists
    if not Path(path_str).exists():
        raise FileNotFoundError(f"Audio file not found: {path_str}")

    print(f"Input file: {path_str}")
    print(f"File exists: {Path(path_str).exists()}")

    cmd = [
        "ffmpeg",
        "-hide_banner", "-loglevel", "warning",
        "-i", path_str,
        "-ac", "1",
        "-ar", "16000",
        "-f", "s16le",
        "-acodec", "pcm_s16le",
        "-"
    ]
    print(f"Starting ffmpeg...")
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Check if process started successfully
    import time
    time.sleep(0.1)
    if proc.poll() is not None:
        stderr = proc.stderr.read().decode('utf-8')
        raise RuntimeError(f"ffmpeg failed to start: {stderr}")

    return proc

def transcribe_stream(model: Model, mp3_path: Path):
    """
    Stream audio through ffmpeg into Vosk recognizer.
    Returns list of (start, end, text) lines grouped by window.
    """
    proc = ffmpeg_stream(mp3_path)
    if proc.stdout is None:
        raise RuntimeError("ffmpeg stdout not available")
    rec = KaldiRecognizer(model, 16000)  # Integer sample rate
    rec.SetWords(True)
    segments = []
    CHUNK_BYTES = 4000 * 2  # 4000 samples * 2 bytes/sample ~ 4000/16000 = 0.25s per chunk
    chunks_read = 0
    bytes_read = 0

    try:
        while True:
            chunk = proc.stdout.read(CHUNK_BYTES)
            if not chunk:
                break

            chunks_read += 1
            bytes_read += len(chunk)

            if rec.AcceptWaveform(chunk):
                res = json.loads(rec.Result())
                if 'result' in res and res['result']:
                    print(f"  Speech in chunk {chunks_read}: {len(res['result'])} words")
                    segments.extend(res['result'])
            else:
                # partial result available via rec.PartialResult() if desired
                pass

        # Get final result
        final = json.loads(rec.FinalResult())
        if 'result' in final and final['result']:
            print(f"  Final result: {len(final['result'])} words")
            segments.extend(final['result'])

        print(f"Total: {chunks_read} chunks, {bytes_read:,} bytes, {len(segments)} words")

    except Exception as e:
        print(f"Error during transcription: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        try:
            # Check if ffmpeg had any errors
            if proc.stderr:
                stderr_output = proc.stderr.read().decode('utf-8')
                if stderr_output:
                    print(f"ffmpeg stderr: {stderr_output}")

            proc.stdout.close()
            proc.kill()
        except Exception as ex:
            print(f"Error closing ffmpeg: {ex}")

    # Group words into ~10s blocks (configurable)
    if not segments:
        print("  WARNING: No segments detected")
        return []
    lines = []
    window = 10.0
    current_start = segments[0]['start']
    current_end = segments[0]['end']
    current_text = [segments[0]['word']]
    for w in segments[1:]:
        if w['start'] - current_start <= window:
            current_end = w['end']
            current_text.append(w['word'])
        else:
            lines.append((current_start, current_end, " ".join(current_text)))
            current_start = w['start']
            current_end = w['end']
            current_text = [w['word']]
    lines.append((current_start, current_end, " ".join(current_text)))
    return lines

def format_timestamp(t: float) -> str:
    hrs = int(t // 3600)
    mins = int((t % 3600) // 60)
    secs = t % 60
    if hrs:
        return f"{hrs:02d}:{mins:02d}:{secs:06.3f}"
    else:
        return f"{mins:02d}:{secs:06.3f}"

def extract_metadata(audio_path: Path) -> dict:
    """
    Extract metadata from audio file using ffprobe.
    Returns dict with: title, artist, album, date, etc.
    """
    try:
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            str(audio_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            tags = data.get('format', {}).get('tags', {})

            # Normalize tag keys (ffprobe can return different cases)
            normalized_tags = {}
            for k, v in tags.items():
                normalized_tags[k.lower()] = v

            return {
                'title': normalized_tags.get('title', ''),
                'artist': normalized_tags.get('artist', normalized_tags.get('author', '')),
                'album': normalized_tags.get('album', normalized_tags.get('album_artist', '')),
                'date': normalized_tags.get('date', normalized_tags.get('year', '')),
                'genre': normalized_tags.get('genre', ''),
                'comment': normalized_tags.get('comment', ''),
                'track': normalized_tags.get('track', ''),
            }
    except Exception as e:
        print(f"Warning: Could not extract metadata: {e}")

    return {}

def write_markdown(out_path: Path, src_audio: Path, lines, metadata=None, include_timestamps=False):
    """
    Write transcription to markdown with enhanced frontmatter.
    Metadata dict can include: title, artist, album, date, genre, comment, track
    """
    with out_path.open("w", encoding="utf-8") as f:
        # Write frontmatter
        f.write("---\n")
        f.write(f"source: {src_audio.name}\n")

        if metadata:
            # Author with wikilink if available
            author = metadata.get('artist', '')
            if author:
                f.write(f"author: [[{author}]]\n")
            else:
                f.write("author:\n")

            # Book title (album) with wikilink if available
            book_title = metadata.get('album', '')
            if book_title:
                f.write(f"book title: [[{book_title}]]\n")
            else:
                f.write("book title:\n")

            # Title (if different from filename)
            title = metadata.get('title', '')
            if title:
                f.write(f"title: {title}\n")

            # Date/Year
            date = metadata.get('date', '')
            if date:
                f.write(f"date: {date}\n")

            # Genre
            genre = metadata.get('genre', '')
            if genre:
                f.write(f"genre: {genre}\n")

            # Track number
            track = metadata.get('track', '')
            if track:
                f.write(f"track: {track}\n")

        else:
            # No metadata, use simple format with empty fields for manual filling
            f.write("author:\n")
            f.write("book title:\n")

        f.write("---\n\n")

        if not lines:
            f.write("*(no speech detected)*\n")
            return

        if include_timestamps:
            # Use double parentheses to avoid markdown link interpretation
            for start, end, text in lines:
                f.write(f"**({format_timestamp(start)} - {format_timestamp(end)})** {text}\n\n")
        else:
            # No timestamps, just text with paragraph breaks
            for start, end, text in lines:
                f.write(f"{text}\n\n")

@app.command()
def single(
    input: Path = typer.Argument(...),
    outdir: Path = typer.Option(Path(".")),
    model: Path = typer.Option(DEFAULT_MODEL_PATH, "--model", help="Path to Vosk model directory"),
    timestamps: bool = typer.Option(False, "--timestamps", help="Include timestamps in output")
):
    # Clean input path - remove any newlines from terminal wrapping
    input_str = str(input).replace('\n', '').replace('\r', '').strip()
    input = Path(input_str)

    model_path = Path(model)
    if not model_path.exists():
        typer.echo(f"Vosk model not found at {model_path}. Download and set model path.")
        raise typer.Exit(code=1)
    outdir.mkdir(parents=True, exist_ok=True)

    # Extract metadata from audio file
    print("Extracting metadata...")
    metadata = extract_metadata(input)
    if metadata:
        print(f"  Found metadata: {', '.join(k for k, v in metadata.items() if v)}")

    # Transcribe
    vosk_model = Model(str(model_path))
    lines = transcribe_stream(vosk_model, input)
    out_md = outdir / (input.stem + ".md")
    write_markdown(out_md, input, lines, metadata=metadata, include_timestamps=timestamps)
    typer.echo(f"Wrote {out_md}")

@app.command()
def batch(
    indir: Path = typer.Argument(...),
    outdir: Path = typer.Option(Path("./out")),
    concurrency: int = typer.Option(1),
    model: Path = typer.Option(DEFAULT_MODEL_PATH, "--model", help="Path to Vosk model directory"),
    timestamps: bool = typer.Option(False, "--timestamps", help="Include timestamps in output")
):
    # Clean input path - remove any newlines from terminal wrapping
    indir_str = str(indir).replace('\n', '').replace('\r', '').strip()
    indir = Path(indir_str)

    model_path = Path(model)
    if not model_path.exists():
        typer.echo(f"Vosk model not found at {model_path}. Download and set model path.")
        raise typer.Exit(code=1)
    outdir.mkdir(parents=True, exist_ok=True)
    files = list(indir.glob("*.mp3"))
    if not files:
        typer.echo("No mp3 files found.")
        raise typer.Exit()
    vosk_model = Model(str(model_path))
    with Progress() as progress:
        task = progress.add_task("[green]Transcribing...", total=len(files))
        with ThreadPoolExecutor(max_workers=concurrency) as ex:
            futures = {ex.submit(process_file, vosk_model, f, outdir, timestamps): f for f in files}
            for fut in as_completed(futures):
                f = futures[fut]
                try:
                    md = fut.result()
                    progress.update(task, advance=1)
                except Exception as e:
                    typer.echo(f"Failed {f}: {e}")
                    progress.update(task, advance=1)

def process_file(model, mp3_path: Path, outdir: Path, include_timestamps: bool = False):
    # Extract metadata
    metadata = extract_metadata(mp3_path)

    # Transcribe
    lines = transcribe_stream(model, mp3_path)
    out_md = outdir / (mp3_path.stem + ".md")
    write_markdown(out_md, mp3_path, lines, metadata=metadata, include_timestamps=include_timestamps)
    return out_md

if __name__ == "__main__":
    app()
