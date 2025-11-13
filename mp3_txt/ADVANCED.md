# Advanced Features & Model Information

**Project:** mp3_txt - Audio Transcription
**Date:** 2025-11-12

---

## 🎯 Model Options

### Current: Small English Model (vosk-model-small-en-us-0.15)

**Specifications:**
- **Size:** ~40MB
- **Accuracy:** ~85% (good for clear speech)
- **Speed:** 10min audio → 2-3min processing
- **RAM:** ~500MB per worker
- **Best for:** Quick transcriptions, clear audio, standard American English

**Download:**
```bash
cd ~/.cache
curl -LO https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
rm vosk-model-small-en-us-0.15.zip
```

---

### Upgrade: Large English Model (vosk-model-en-us-0.22)

**Specifications:**
- **Size:** ~1.8GB
- **Accuracy:** ~92% (excellent for varied conditions)
- **Speed:** 10min audio → 4-6min processing
- **RAM:** ~1.5GB per worker
- **Best for:** Better accuracy, accents, background noise, multiple speakers

**When to upgrade:**
- Transcribing sermons/lectures with multiple speakers
- Audio with background noise
- Non-standard accents
- Technical/theological terminology
- Critical content requiring high accuracy

**Download and configure:**
```bash
# Download large model
cd ~/.cache
curl -LO https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip
unzip vosk-model-en-us-0.22.zip
rm vosk-model-en-us-0.22.zip

# Update transcribe_vosk_stream.py line 20:
DEFAULT_MODEL_PATH = Path.home() / ".cache" / "vosk-model-en-us-0.22"
```

**Performance comparison:**

| Feature | Small (0.15) | Large (0.22) |
|---------|-------------|--------------|
| Size | 40MB | 1.8GB |
| Accuracy | 85% | 92% |
| Speed | Fast | Moderate |
| RAM | 500MB | 1.5GB |
| Multi-speaker | Good | Excellent |
| Accents | Fair | Very Good |
| Background noise | Fair | Good |

---

### Best Model: GigaSpeech (vosk-model-en-us-0.42-gigaspeech)

**Specifications:**
- **Size:** ~2.3GB
- **Accuracy:** ~95% (state-of-the-art)
- **Speed:** 10min audio → 6-8min processing
- **RAM:** ~2GB per worker
- **Best for:** Highest quality transcriptions, research, archival

**Download:**
```bash
cd ~/.cache
curl -LO https://alphacephei.com/vosk/models/vosk-model-en-us-0.42-gigaspeech.zip
unzip vosk-model-en-us-0.42-gigaspeech.zip
```

---

## 🌍 Supported Languages

Vosk supports **20+ languages** with varying model sizes and quality:

### Major Languages

| Language | Model Size | Code | Quality |
|----------|-----------|------|---------|
| English (US) | 40MB - 2.3GB | en-us | Excellent |
| English (UK) | 40MB - 1.8GB | en-uk | Excellent |
| Spanish | 40MB - 1GB | es | Excellent |
| French | 40MB - 1.4GB | fr | Excellent |
| German | 40MB - 1.9GB | de | Excellent |
| Russian | 40MB - 2.5GB | ru | Excellent |
| Chinese (Mandarin) | 40MB - 1.3GB | cn | Excellent |
| Portuguese | 40MB - 1.2GB | pt | Very Good |
| Italian | 40MB - 1GB | it | Very Good |
| Dutch | 40MB - 900MB | nl | Very Good |

### Additional Languages

- Arabic (ar)
- Turkish (tr)
- Vietnamese (vi)
- Hindi (hi)
- Japanese (ja)
- Korean (ko)
- Polish (pl)
- Czech (cs)
- Ukrainian (uk)
- Greek (el)
- Persian (fa)
- Hebrew (he)

**Browse all models:** https://alphacephei.com/vosk/models

### Using Different Languages

```bash
# Download model for your language
cd ~/.cache
curl -LO https://alphacephei.com/vosk/models/vosk-model-fr-0.22.zip  # French
unzip vosk-model-fr-0.22.zip

# Update transcribe_vosk_stream.py:
DEFAULT_MODEL_PATH = Path.home() / ".cache" / "vosk-model-fr-0.22"
```

---

## 🎵 Supported Audio Formats

### Native Support (via ffmpeg)

Vosk + ffmpeg can process virtually any audio/video format:

**Audio formats:**
- MP3 (.mp3)
- WAV (.wav)
- M4A (.m4a)
- AAC (.aac)
- FLAC (.flac)
- OGG (.ogg)
- WMA (.wma)
- OPUS (.opus)
- AIFF (.aiff)

**Video formats (audio extraction):**
- MP4 (.mp4)
- MKV (.mkv)
- AVI (.avi)
- MOV (.mov)
- WEBM (.webm)
- FLV (.flv)

**Streaming:**
- URLs (YouTube, podcasts via yt-dlp integration)
- Live streams (with buffering)

### Audio Quality Requirements

**Optimal:**
- Sample rate: 16kHz or higher (automatically converted)
- Channels: Mono or stereo (automatically converted to mono)
- Bitrate: 64kbps or higher
- Clear speech with minimal background noise

**Acceptable:**
- Sample rate: 8kHz+ (phone quality)
- Heavy compression (but accuracy will decrease)
- Some background noise

**Challenging:**
- Multiple overlapping speakers
- Music/noise louder than speech
- Extreme accents
- Technical jargon without training data

---

## 📈 Improving Transcription Accuracy

### 1. Audio Preprocessing

**Noise Reduction (before transcription):**
```bash
# Install sox
brew install sox

# Reduce noise
sox input.mp3 output.mp3 noisered noise_profile 0.21

# Normalize volume
ffmpeg -i input.mp3 -af "volume=1.5" output.mp3

# Remove silence
ffmpeg -i input.mp3 -af silenceremove=1:0:-50dB output.mp3
```

**Best practices:**
- Use high-quality microphones
- Record in quiet environments
- Position mic 6-12 inches from speaker
- Use pop filters for plosives
- Record in mono at 16kHz or 44.1kHz

### 2. Custom Vocabulary

Add custom words (names, technical terms) that Vosk might not recognize:

**Method 1: Custom dictionary (advanced)**
```python
# In transcribe_vosk_stream.py, after creating recognizer:
rec = KaldiRecognizer(model, 16000)
rec.SetWords(True)

# Add custom vocabulary (JSON format)
custom_vocab = '["Zettelkasten", "Obsidian", "wikilinks", "Pneumatology"]'
rec.SetGrammar(custom_vocab)
```

**Method 2: Post-processing corrections**
```python
# Add to write_markdown function:
corrections = {
    "obsidian": "Obsidian",
    "cattle cast": "Zettelkasten",
    "wiki links": "wikilinks",
}

for old, new in corrections.items():
    text = text.replace(old, new)
```

### 3. Speaker Diarization (Who Said What)

Vosk doesn't include speaker diarization, but you can integrate:

**Using pyannote.audio:**
```bash
pip install pyannote.audio

# Requires HuggingFace token
# See: https://huggingface.co/pyannote/speaker-diarization
```

**Integration approach:**
1. Transcribe audio with Vosk (text + timestamps)
2. Run pyannote for speaker detection (speaker labels + timestamps)
3. Merge results → "Speaker 1: [text]", "Speaker 2: [text]"

### 4. Model Fine-Tuning (Advanced)

**When to fine-tune:**
- Specific domain (medical, legal, theological)
- Heavy accent not in training data
- Niche vocabulary (ancient languages, technical terms)

**Requirements:**
- 10+ hours of transcribed audio in target domain
- GPU for training (cloud recommended)
- Kaldi toolkit knowledge
- Time investment: 2-4 weeks

**Resources:**
- Kaldi documentation: https://kaldi-asr.org/doc/
- Vosk training: https://alphacephei.com/vosk/adaptation
- Common Voice dataset: https://commonvoice.mozilla.org/

**Alternative: Transfer learning**
- Start with existing Vosk model
- Fine-tune on 2-5 hours of domain-specific audio
- Faster than training from scratch

### 5. Post-Processing with LLMs

Use Claude or GPT to improve transcription:

**Grammar correction:**
```python
# After transcription, pass to Claude API:
prompt = f"""
Fix grammar, punctuation, and capitalization in this transcript.
Preserve the speaker's meaning and style.

Transcript:
{raw_transcript}

Corrected:
"""
```

**Paragraph formatting:**
```python
prompt = f"""
Format this transcript into natural paragraphs.
Add section breaks where topics change.

Transcript:
{raw_transcript}
"""
```

**Summary generation:**
```python
prompt = f"""
Create a summary with:
- Main points (bullet list)
- Key quotes
- Action items

Transcript:
{transcript}
"""
```

---

## 🔬 Experimental Features

### 1. Real-Time Transcription

Modify `transcribe_vosk_stream.py` for live audio:

```python
import pyaudio

def transcribe_microphone(model):
    """Real-time mic transcription"""
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=4000)

    rec = KaldiRecognizer(model, 16000)
    rec.SetWords(True)

    print("Listening... (Ctrl+C to stop)")
    try:
        while True:
            data = stream.read(4000, exception_on_overflow=False)
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                print(result.get('text', ''))
    except KeyboardInterrupt:
        pass
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
```

### 2. GPU Acceleration

Vosk is CPU-optimized, but for batch processing you can:

**Parallel processing:**
```bash
# Process multiple files simultaneously
python3 transcribe_vosk_stream.py batch ./folder --concurrency 4
```

**Cloud processing:**
- Rent high-CPU cloud instances (AWS, GCP)
- Process 100+ files in parallel
- Cost-effective for large batches

### 3. Whisper Integration (Alternative)

For highest accuracy (but slower, needs GPU):

```bash
pip install openai-whisper

# Transcribe with Whisper
whisper audio.mp3 --model medium --language en --output_format txt

# Whisper models:
# tiny, base, small, medium, large (best accuracy)
```

**Comparison:**

| Feature | Vosk | Whisper |
|---------|------|---------|
| Accuracy | 85-92% | 95-98% |
| Speed | Fast (CPU) | Slow (needs GPU) |
| Offline | Yes | Yes |
| Languages | 20+ | 99+ |
| RAM | 0.5-2GB | 4-10GB |
| Best for | CPU, batch | GPU, highest quality |

---

## 🎓 Training Custom Models

### Data Requirements

**Minimum viable:**
- 10 hours of transcribed audio
- Clear speech
- Diverse speakers
- Domain-specific vocabulary

**Recommended:**
- 50-100 hours of transcribed audio
- Multiple speakers (10+)
- Various acoustic conditions
- Comprehensive vocabulary coverage

### Training Process Overview

1. **Prepare data:**
   - Audio files (WAV, 16kHz mono)
   - Transcriptions (text files)
   - Lexicon (word pronunciations)

2. **Feature extraction:**
   - MFCC (Mel-frequency cepstral coefficients)
   - Pitch features
   - Voice activity detection

3. **Model training:**
   - Acoustic model (DNN/TDNN)
   - Language model (n-gram or RNN)
   - Pronunciation dictionary

4. **Testing & iteration:**
   - Word Error Rate (WER) calculation
   - Confusion matrix analysis
   - Iterative improvements

### Tools & Resources

**Kaldi (backend for Vosk):**
- Installation: https://kaldi-asr.org/doc/install.html
- Recipes: https://github.com/kaldi-asr/kaldi/tree/master/egs

**Datasets:**
- LibriSpeech (1000 hours, English): https://www.openslr.org/12/
- Common Voice (Mozilla): https://commonvoice.mozilla.org/
- VoxForge: http://www.voxforge.org/

**Training services:**
- Speechmatics: https://www.speechmatics.com/
- AssemblyAI: https://www.assemblyai.com/
- Cloud providers (AWS Transcribe, GCP Speech-to-Text)

### Accent & Dialect Adaptation

**Collect domain data:**
- Record 20+ speakers with target accent
- 30-60 minutes per speaker
- Natural speech (not read text)

**Adaptation techniques:**
1. **MAP (Maximum A Posteriori):** Adapt existing model
2. **MLLR (Maximum Likelihood Linear Regression):** Transform features
3. **Fine-tuning:** Retrain last layers only

**Example use cases:**
- Scottish English accent
- Southern US dialect
- Indian English accent
- Theological terminology (sermons, biblical terms)

---

## 📊 Performance Optimization

### Hardware Recommendations

**Current setup (8GB Mac, i5):**
- Concurrency: 1-2 workers
- Model: Small (40MB) or Medium (1.8GB)
- Speed: 2-6min per 10min audio

**Optimal setup (16GB+, i7/M1):**
- Concurrency: 3-4 workers
- Model: Any size
- Speed: 1-3min per 10min audio

**Server setup (32GB+, 8+ cores):**
- Concurrency: 8-16 workers
- Process 100+ files in hours
- Cost-effective for batch jobs

### Batch Processing Tips

**Organize files:**
```bash
# Group by speaker/topic for consistent renaming
sermons/
├── pastor_john/
│   ├── 001.mp3
│   ├── 002.mp3
└── pastor_mary/
    ├── 001.mp3
```

**Monitor resources:**
```bash
# Watch CPU/RAM usage
htop

# Adjust concurrency if system lags
./transcribe
# Choose concurrency: 1 (safe)
```

**Schedule large jobs:**
```bash
# Run overnight
nohup ./transcribe batch folder ./out --concurrency 2 &

# Check progress
tail -f transcribe.log
```

---

## 🔗 Integration Options

### Obsidian Plugin

Create simple plugin to transcribe from within Obsidian:

**Features:**
- Right-click audio file → "Transcribe"
- Auto-create note with transcript
- Link back to original audio
- Progress notification

### Alfred Workflow

Quick transcription via Alfred:

**Workflow:**
1. Select audio file in Finder
2. Trigger Alfred: `transcribe`
3. Choose options (timestamps, output)
4. Done!

### Zapier/Make Integration

Automate transcription workflow:

**Example flow:**
1. New file added to Dropbox folder
2. Trigger webhook to local machine
3. Transcribe automatically
4. Upload transcript to Notion/Obsidian
5. Send notification

---

## 📚 Resources

**Official Vosk:**
- Website: https://alphacephei.com/vosk/
- GitHub: https://github.com/alphacep/vosk-api
- Models: https://alphacephei.com/vosk/models
- Documentation: https://alphacephei.com/vosk/docs

**Community:**
- Kaldi forums: https://groups.google.com/g/kaldi-help
- Vosk discussions: https://github.com/alphacep/vosk-api/discussions
- Reddit: r/speechrecognition

**Alternative Tools:**
- Whisper (OpenAI): https://github.com/openai/whisper
- DeepSpeech (Mozilla): https://github.com/mozilla/DeepSpeech
- Wav2Vec 2.0 (Facebook): https://github.com/facebookresearch/fairseq

**Training:**
- Kaldi tutorial: https://kaldi-asr.org/doc/tutorial.html
- Speech recognition course: https://www.coursera.org/learn/audio-signal-processing
- Digital signal processing: https://www.dspguide.com/

---

**Last updated:** 2025-11-12
**Version:** 1.0
**Status:** Production ready with advanced features documented
