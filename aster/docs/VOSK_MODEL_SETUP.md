# Vosk Model Setup for Audio Transcription

Aster uses Vosk for offline speech recognition. Vosk models need to be downloaded once and cached locally.

## Quick Setup

### Option 1: Automatic Download (Easiest)
The script will attempt to download the model automatically on first use. However, this may fail in some network environments.

### Option 2: Manual Download (Recommended)

Download the English model manually:

```bash
# Create cache directory
mkdir -p ~/.cache/vosk

# Download model (choose one):

# Small English model (40 MB) - Fast, good for most cases
cd ~/.cache/vosk
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
rm vosk-model-small-en-us-0.15.zip

# OR Large English model (1.8 GB) - Better accuracy
cd ~/.cache/vosk
wget https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip
unzip vosk-model-en-us-0.22.zip
rm vosk-model-en-us-0.22.zip
```

### Option 3: Using Different Models

If you need a different language or model size:

1. Browse available models: https://alphacephei.com/vosk/models
2. Download your preferred model
3. Extract to `~/.cache/vosk/`
4. Update the model name in `aster.py` line 289:
   ```python
   model_name = "vosk-model-small-en-us-0.15"  # Change this
   ```

## Available Models

### English Models:
- **vosk-model-small-en-us-0.15** (40 MB) - Fast, good quality
- **vosk-model-en-us-0.22** (1.8 GB) - Best quality, slower
- **vosk-model-en-us-0.42-gigaspeech** (2.3 GB) - Trained on diverse data

### Other Languages:
- **vosk-model-small-cn-0.22** - Chinese (42 MB)
- **vosk-model-small-ru-0.22** - Russian (45 MB)
- **vosk-model-small-fr-0.22** - French (41 MB)
- **vosk-model-small-de-0.15** - German (45 MB)
- **vosk-model-small-es-0.42** - Spanish (39 MB)
- **vosk-model-small-pt-0.3** - Portuguese (31 MB)
- **vosk-model-small-it-0.22** - Italian (48 MB)
- **vosk-model-small-nl-0.22** - Dutch (39 MB)

Full list: https://alphacephei.com/vosk/models

## Multilingual Support

For Afrikaans (South African church documents), the best approach is:

1. Use the English model (Afrikaans has many English cognates)
2. Or train a custom model (advanced)
3. Or use the Dutch model as Afrikaans is related to Dutch:
   ```bash
   cd ~/.cache/vosk
   wget https://alphacephei.com/vosk/models/vosk-model-small-nl-0.22.zip
   unzip vosk-model-small-nl-0.22.zip
   ```

## Verifying Installation

Check if model is installed:

```bash
ls -la ~/.cache/vosk/
```

You should see a folder like `vosk-model-small-en-us-0.15/` with these files:
- `am/` - Acoustic model
- `conf/` - Configuration
- `graph/` - Language model graph
- `README` - Model information

## Troubleshooting

### Error: "Vosk model not found"
- Download the model manually (see Option 2 above)
- Check the model path: `~/.cache/vosk/vosk-model-small-en-us-0.15/`

### Error: "Access denied" when downloading
- Your network may block the download
- Download on another machine and copy to `~/.cache/vosk/`
- Or use `curl` instead of `wget`:
  ```bash
  curl -LO https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
  ```

### Slow transcription
- Use the small model for faster processing
- Large files are automatically chunked and processed in parallel
- Consider using GPU-accelerated models (requires additional setup)

### Poor accuracy
- Use a larger model (e.g., vosk-model-en-us-0.22)
- Ensure audio is 16kHz mono WAV (Aster converts automatically)
- Clean audio works better than noisy recordings

## Performance Expectations

### Small English Model (vosk-model-small-en-us-0.15):
- **Size**: 40 MB
- **Speed**: ~10x realtime on CPU (1 min audio = 6 sec processing)
- **Accuracy**: 85-90% on clean speech
- **Use case**: Quick transcription, testing, batch processing

### Large English Model (vosk-model-en-us-0.22):
- **Size**: 1.8 GB
- **Speed**: ~3x realtime on CPU (1 min audio = 20 sec processing)
- **Accuracy**: 92-95% on clean speech
- **Use case**: Production, high-quality transcription

## Audio Processing Pipeline

When you process an audio file, Aster:

1. **Converts** to WAV (16kHz, mono) if needed
2. **Detects** duration with ffprobe
3. **Chunks** large files (>10 min) into 5-minute segments
4. **Transcribes** chunks in parallel (4 workers)
5. **Reassembles** with timestamps [MM:SS]
6. **Cleans** transcript with LLM (Ollama)

## Next Steps

After setting up the model:

1. Test with a small audio file:
   ```bash
   python3 aster.py path/to/audio.mp3 -o output.md
   ```

2. Run the full test suite:
   ```bash
   python3 tests/run_tests.py
   ```

3. Process training data:
   ```bash
   python3 process_training_data.py
   ```

## Alternative: Whisper

If Vosk doesn't meet your needs, consider OpenAI Whisper:
- Better accuracy (especially for accents, noise)
- Supports 99 languages (including Afrikaans)
- Requires more resources (GPU recommended)
- Installation: `pip install openai-whisper`

Aster currently uses Vosk for offline processing without GPU requirements.
