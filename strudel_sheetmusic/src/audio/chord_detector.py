"""
Chord Detection
Identifies chords and chord progressions from audio
"""

import numpy as np
from typing import List, Dict, Optional


class ChordDetector:
    """
    Detects chords from audio using chroma features
    """

    # Common chord templates (1 = root, 0 = not in chord)
    CHORD_TEMPLATES = {
        'maj': [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],  # Major (root, major 3rd, perfect 5th)
        'min': [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],  # Minor (root, minor 3rd, perfect 5th)
        '7': [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],    # Dominant 7th
        'maj7': [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1], # Major 7th
        'min7': [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0], # Minor 7th
        'dim': [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],  # Diminished
        'aug': [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],  # Augmented
        'sus2': [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0], # Suspended 2nd
        'sus4': [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0], # Suspended 4th
    }

    NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    def __init__(self, sample_rate: int = 22050):
        """
        Initialize chord detector

        Args:
            sample_rate: Audio sample rate
        """
        self.sample_rate = sample_rate

    def extract_chroma(self, audio: np.ndarray) -> np.ndarray:
        """
        Extract chromagram from audio

        Args:
            audio: Audio data

        Returns:
            Chromagram (12 x time_frames)
        """
        try:
            import librosa

            # Use CQT-based chromagram for better accuracy
            chroma = librosa.feature.chroma_cqt(
                y=audio,
                sr=self.sample_rate,
                hop_length=512
            )

            return chroma

        except ImportError:
            raise ImportError("librosa required for chroma extraction")

    def detect_chord_from_chroma(
        self,
        chroma: np.ndarray,
        frame_idx: Optional[int] = None
    ) -> Dict:
        """
        Detect chord from chroma features

        Args:
            chroma: Chromagram (12 x time) or single frame (12,)
            frame_idx: Frame index if using full chromagram

        Returns:
            Dictionary with 'root', 'quality', 'name', 'confidence'
        """
        # Get single frame if needed
        if chroma.ndim == 2:
            if frame_idx is None:
                # Average over time if no frame specified
                chroma_frame = np.mean(chroma, axis=1)
            else:
                chroma_frame = chroma[:, frame_idx]
        else:
            chroma_frame = chroma

        # Normalize
        chroma_frame = chroma_frame / (np.sum(chroma_frame) + 1e-6)

        best_match = None
        best_score = -1

        # Try each root note
        for root_idx in range(12):
            # Try each chord quality
            for quality, template in self.CHORD_TEMPLATES.items():
                # Rotate template to match root
                rotated_template = np.roll(template, root_idx)

                # Calculate correlation
                score = np.dot(chroma_frame, rotated_template)

                if score > best_score:
                    best_score = score
                    best_match = {
                        'root': self.NOTE_NAMES[root_idx],
                        'quality': quality,
                        'name': f"{self.NOTE_NAMES[root_idx]}{quality}",
                        'confidence': float(score)
                    }

        return best_match

    def detect_chord_progression(
        self,
        audio: np.ndarray,
        segment_length: float = 2.0,
        min_confidence: float = 0.5
    ) -> List[Dict]:
        """
        Detect chord progression over time

        Args:
            audio: Audio data
            segment_length: Length of each segment in seconds
            min_confidence: Minimum confidence to include chord

        Returns:
            List of chord dictionaries with 'time', 'chord', 'confidence'
        """
        try:
            import librosa

            # Extract chroma
            chroma = self.extract_chroma(audio)

            # Calculate hop time
            hop_length = 512
            hop_time = hop_length / self.sample_rate

            # Calculate frames per segment
            frames_per_segment = int(segment_length / hop_time)

            chords = []
            num_frames = chroma.shape[1]

            for start_frame in range(0, num_frames, frames_per_segment):
                end_frame = min(start_frame + frames_per_segment, num_frames)

                # Average chroma over segment
                segment_chroma = np.mean(
                    chroma[:, start_frame:end_frame],
                    axis=1
                )

                # Detect chord
                chord = self.detect_chord_from_chroma(segment_chroma)

                # Add timing
                time = start_frame * hop_time

                if chord['confidence'] >= min_confidence:
                    chords.append({
                        'time': time,
                        'duration': (end_frame - start_frame) * hop_time,
                        'chord': chord['name'],
                        'root': chord['root'],
                        'quality': chord['quality'],
                        'confidence': chord['confidence']
                    })

            # Remove duplicate consecutive chords
            filtered_chords = []
            prev_chord = None

            for chord in chords:
                if chord['chord'] != prev_chord:
                    filtered_chords.append(chord)
                    prev_chord = chord['chord']
                else:
                    # Extend duration of previous chord
                    if filtered_chords:
                        filtered_chords[-1]['duration'] += chord['duration']

            return filtered_chords

        except ImportError:
            raise ImportError("librosa required for chord detection")

    def chord_progression_to_roman(
        self,
        chords: List[Dict],
        key: str,
        mode: str = 'major'
    ) -> List[str]:
        """
        Convert chord progression to Roman numeral analysis

        Args:
            chords: List of detected chords
            key: Key signature (e.g., 'C', 'F#')
            mode: 'major' or 'minor'

        Returns:
            List of Roman numeral chord names

        TODO: Implement proper Roman numeral analysis
        """
        # This is complex - would need music theory implementation
        # Placeholder for now
        return [chord['chord'] for chord in chords]
