"""
Audio Analyzer
Main class for extracting musical information from audio files
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple
import numpy as np


class AudioAnalyzer:
    """
    Analyzes audio files to extract musical features

    Features extracted:
    - BPM (tempo)
    - Key signature
    - Chord progression
    - Main melody notes
    - Beat positions
    - Harmonic content
    """

    def __init__(self, sample_rate: int = 22050):
        """
        Initialize audio analyzer

        Args:
            sample_rate: Target sample rate for analysis (default: 22050)
        """
        self.sample_rate = sample_rate
        self.audio_data = None
        self.duration = None

    def load_audio(self, file_path: str) -> np.ndarray:
        """
        Load audio file

        Args:
            file_path: Path to audio file (mp3, wav, flac, etc.)

        Returns:
            Audio data as numpy array

        TODO: Implement using librosa
        """
        try:
            import librosa

            audio, sr = librosa.load(file_path, sr=self.sample_rate, mono=True)
            self.audio_data = audio
            self.duration = len(audio) / sr

            return audio

        except ImportError:
            raise ImportError(
                "librosa is required for audio analysis. "
                "Install with: pip install librosa"
            )
        except Exception as e:
            raise RuntimeError(f"Failed to load audio: {e}")

    def detect_bpm(self, audio: Optional[np.ndarray] = None) -> float:
        """
        Detect tempo (BPM) of audio

        Args:
            audio: Audio data (uses loaded audio if None)

        Returns:
            BPM as float

        TODO: Implement using librosa.beat.tempo or madmom
        """
        if audio is None:
            audio = self.audio_data

        if audio is None:
            raise ValueError("No audio loaded")

        try:
            import librosa

            # Detect tempo
            tempo, _ = librosa.beat.beat_track(y=audio, sr=self.sample_rate)

            # tempo can be a scalar or array, handle both
            if isinstance(tempo, np.ndarray):
                tempo = float(tempo[0])
            else:
                tempo = float(tempo)

            return tempo

        except ImportError:
            raise ImportError("librosa required for BPM detection")

    def detect_key(self, audio: Optional[np.ndarray] = None) -> Dict[str, any]:
        """
        Detect musical key of audio

        Args:
            audio: Audio data

        Returns:
            Dictionary with 'key' (e.g., 'C', 'F#') and 'mode' ('major'/'minor')

        TODO: Implement using librosa + music theory
        """
        if audio is None:
            audio = self.audio_data

        if audio is None:
            raise ValueError("No audio loaded")

        try:
            import librosa

            # Extract chroma features
            chromagram = librosa.feature.chroma_cqt(
                y=audio,
                sr=self.sample_rate
            )

            # Average over time
            chroma_avg = np.mean(chromagram, axis=1)

            # Find most prominent note
            key_idx = np.argmax(chroma_avg)

            keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
            detected_key = keys[key_idx]

            # Simple major/minor detection (would need improvement)
            # Check if minor third is prominent
            minor_third_idx = (key_idx + 3) % 12
            major_third_idx = (key_idx + 4) % 12

            if chroma_avg[minor_third_idx] > chroma_avg[major_third_idx]:
                mode = 'minor'
            else:
                mode = 'major'

            return {
                'key': detected_key,
                'mode': mode,
                'confidence': float(chroma_avg[key_idx])
            }

        except ImportError:
            raise ImportError("librosa required for key detection")

    def detect_beats(self, audio: Optional[np.ndarray] = None) -> List[float]:
        """
        Detect beat positions in audio

        Args:
            audio: Audio data

        Returns:
            List of beat times in seconds

        TODO: Implement using librosa.beat.beat_track
        """
        if audio is None:
            audio = self.audio_data

        if audio is None:
            raise ValueError("No audio loaded")

        try:
            import librosa

            # Detect beat positions
            tempo, beat_frames = librosa.beat.beat_track(
                y=audio,
                sr=self.sample_rate
            )

            # Convert frames to times
            beat_times = librosa.frames_to_time(
                beat_frames,
                sr=self.sample_rate
            )

            return beat_times.tolist()

        except ImportError:
            raise ImportError("librosa required for beat detection")

    def extract_melody(
        self,
        audio: Optional[np.ndarray] = None,
        min_frequency: float = 80,
        max_frequency: float = 800
    ) -> List[Dict]:
        """
        Extract main melody as MIDI notes

        Args:
            audio: Audio data
            min_frequency: Minimum frequency to detect (Hz)
            max_frequency: Maximum frequency to detect (Hz)

        Returns:
            List of dictionaries with 'time', 'note', 'frequency', 'confidence'

        TODO: Implement using basic-pitch or crepe
        """
        if audio is None:
            audio = self.audio_data

        if audio is None:
            raise ValueError("No audio loaded")

        # Placeholder - would use basic-pitch or crepe
        raise NotImplementedError(
            "Melody extraction requires basic-pitch or crepe. "
            "Install with: pip install basic-pitch"
        )

    def analyze_full(self, file_path: str) -> Dict:
        """
        Perform complete analysis of audio file

        Args:
            file_path: Path to audio file

        Returns:
            Dictionary with all analysis results
        """
        print(f"Loading audio: {file_path}")
        audio = self.load_audio(file_path)

        print("Analyzing BPM...")
        bpm = self.detect_bpm(audio)

        print("Detecting key...")
        key_info = self.detect_key(audio)

        print("Finding beats...")
        beats = self.detect_beats(audio)

        results = {
            'file': file_path,
            'duration': self.duration,
            'bpm': bpm,
            'key': key_info['key'],
            'mode': key_info['mode'],
            'key_confidence': key_info['confidence'],
            'beat_count': len(beats),
            'beat_positions': beats[:10]  # First 10 beats as sample
        }

        # Try melody extraction if available
        try:
            melody = self.extract_melody(audio)
            results['melody'] = melody[:20]  # First 20 notes
        except (NotImplementedError, ImportError):
            results['melody'] = "Not available - install basic-pitch"

        return results

    def to_midi(self, analysis_results: Dict, output_path: str):
        """
        Convert analysis results to MIDI file

        Args:
            analysis_results: Results from analyze_full()
            output_path: Path to save MIDI file

        TODO: Implement MIDI generation from analysis
        """
        raise NotImplementedError("MIDI conversion coming soon")

    def get_time_signature(
        self,
        audio: Optional[np.ndarray] = None
    ) -> Tuple[int, int]:
        """
        Detect time signature

        Args:
            audio: Audio data

        Returns:
            Tuple of (numerator, denominator) e.g., (4, 4) or (3, 4)

        TODO: Implement beat grouping analysis
        """
        # This is complex - would need to analyze beat patterns
        # Default to 4/4 for now
        return (4, 4)
