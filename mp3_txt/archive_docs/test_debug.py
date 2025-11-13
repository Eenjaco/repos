#!/usr/bin/env python3
"""Debug script to test Vosk transcription"""
import subprocess
import json
from pathlib import Path
from vosk import Model, KaldiRecognizer

MODEL_PATH = Path.home() / ".cache" / "vosk-model-small-en-us-0.15"
TEST_AUDIO = Path("/Users/mac/Documents/local_vault/Projects/mp3_txt/test/Living into Community Cultivating Practices That Sustain Us - 002.mp3")

print(f"Model path: {MODEL_PATH}")
print(f"Model exists: {MODEL_PATH.exists()}")
print(f"Audio file: {TEST_AUDIO}")
print(f"Audio exists: {TEST_AUDIO.exists()}")
print()

# Load model
print("Loading Vosk model...")
model = Model(str(MODEL_PATH))
print("✅ Model loaded")
print()

# Start ffmpeg stream
print("Starting ffmpeg stream...")
cmd = [
    "ffmpeg",
    "-hide_banner", "-loglevel", "error",
    "-i", str(TEST_AUDIO),
    "-ac", "1",
    "-ar", "16000",
    "-t", "60",  # Just first 60 seconds for testing
    "-f", "s16le",
    "-acodec", "pcm_s16le",
    "-"
]

proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print("✅ ffmpeg started")
print()

# Create recognizer
rec = KaldiRecognizer(model, 16000)
rec.SetWords(True)

# Process audio
print("Processing audio...")
segments = []
bytes_processed = 0
chunks_processed = 0

CHUNK_BYTES = 4000 * 2

while True:
    chunk = proc.stdout.read(CHUNK_BYTES)
    if not chunk:
        break

    bytes_processed += len(chunk)
    chunks_processed += 1

    if rec.AcceptWaveform(chunk):
        res = json.loads(rec.Result())
        if 'result' in res and res['result']:
            print(f"✅ Speech detected in chunk {chunks_processed}")
            segments.extend(res['result'])
            # Print first few words
            for w in res['result'][:5]:
                print(f"  {w['start']:.2f}s: {w['word']}")

# Get final result
final = json.loads(rec.FinalResult())
if 'result' in final and final['result']:
    print(f"✅ Final speech detected")
    segments.extend(final['result'])

proc.stdout.close()
proc.kill()

print()
print(f"Chunks processed: {chunks_processed}")
print(f"Bytes processed: {bytes_processed:,}")
print(f"Total words detected: {len(segments)}")
print()

if segments:
    print("First 20 words:")
    for w in segments[:20]:
        print(f"  [{w['start']:.2f}s - {w['end']:.2f}s] {w['word']}")
else:
    print("⚠️ No speech detected")
    print("\nPossible reasons:")
    print("1. Audio file is silent or very quiet")
    print("2. Speech is not in English")
    print("3. Audio quality is too poor")
    print("4. File starts with silence - try skipping ahead")
