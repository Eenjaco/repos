"""
Pitch Detection
Detects fundamental frequency and converts to MIDI notes
"""

import numpy as np
from typing import List, Tuple


class PitchDetector:
    """
    Detects pitch from audio using various algorithms
    """

    def __init__(self, sample_rate: int = 22050):
        """
        Initialize pitch detector

        Args:
            sample_rate: Audio sample rate
        """
        self.sample_rate = sample_rate

    def frequency_to_midi(self, frequency: float) -> int:
        """
        Convert frequency to MIDI note number

        Args:
            frequency: Frequency in Hz

        Returns:
            MIDI note number (0-127)
        """
        if frequency <= 0:
            return 0

        # A4 = 440 Hz = MIDI note 69
        midi_note = 69 + 12 * np.log2(frequency / 440.0)
        return int(round(midi_note))

    def midi_to_frequency(self, midi_note: int) -> float:
        """
        Convert MIDI note to frequency

        Args:
            midi_note: MIDI note number (0-127)

        Returns:
            Frequency in Hz
        """
        return 440.0 * (2 ** ((midi_note - 69) / 12))

    def detect_pitch_librosa(
        self,
        audio: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Detect pitch using librosa's piptrack

        Args:
            audio: Audio data

        Returns:
            Tuple of (frequencies, times)
        """
        try:
            import librosa

            # Extract pitch using piptrack
            pitches, magnitudes = librosa.piptrack(
                y=audio,
                sr=self.sample_rate,
                fmin=librosa.note_to_hz('C2'),
                fmax=librosa.note_to_hz('C7')
            )

            # Get the most prominent pitch at each time
            frequencies = []
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                freq = pitches[index, t]
                if freq > 0:  # Only include detected pitches
                    frequencies.append(freq)
                else:
                    frequencies.append(0)

            # Convert frame indices to times
            times = librosa.frames_to_time(
                np.arange(len(frequencies)),
                sr=self.sample_rate
            )

            return np.array(frequencies), times

        except ImportError:
            raise ImportError("librosa required for pitch detection")

    def detect_pitch_crepe(
        self,
        audio: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Detect pitch using CREPE (deep learning model)
        More accurate but slower than librosa

        Args:
            audio: Audio data

        Returns:
            Tuple of (times, frequencies, confidences)

        TODO: Implement CREPE integration
        """
        try:
            import crepe

            # CREPE expects float32 audio
            audio = audio.astype(np.float32)

            # Run CREPE pitch detection
            time, frequency, confidence, activation = crepe.predict(
                audio,
                self.sample_rate,
                viterbi=True
            )

            return time, frequency, confidence

        except ImportError:
            raise ImportError(
                "CREPE required for advanced pitch detection. "
                "Install with: pip install crepe"
            )

    def pitch_to_notes(
        self,
        frequencies: np.ndarray,
        times: np.ndarray,
        confidences: np.ndarray = None,
        min_duration: float = 0.1,
        confidence_threshold: float = 0.5
    ) -> List[dict]:
        """
        Convert pitch contour to discrete MIDI notes

        Args:
            frequencies: Array of detected frequencies
            times: Array of corresponding times
            confidences: Optional confidence scores
            min_duration: Minimum note duration in seconds
            confidence_threshold: Minimum confidence to include note

        Returns:
            List of note dictionaries with 'time', 'duration', 'midi', 'frequency'
        """
        notes = []
        current_note = None
        current_start = None

        for i, (freq, time) in enumerate(zip(frequencies, times)):
            # Skip if below confidence threshold
            if confidences is not None:
                if confidences[i] < confidence_threshold:
                    if current_note is not None:
                        # End current note
                        duration = time - current_start
                        if duration >= min_duration:
                            notes.append({
                                'time': current_start,
                                'duration': duration,
                                'midi': current_note,
                                'frequency': self.midi_to_frequency(current_note),
                                'note_name': self._midi_to_note_name(current_note)
                            })
                        current_note = None
                    continue

            # Skip silence
            if freq == 0 or freq < 20:
                if current_note is not None:
                    duration = time - current_start
                    if duration >= min_duration:
                        notes.append({
                            'time': current_start,
                            'duration': duration,
                            'midi': current_note,
                            'frequency': self.midi_to_frequency(current_note),
                            'note_name': self._midi_to_note_name(current_note)
                        })
                    current_note = None
                continue

            midi_note = self.frequency_to_midi(freq)

            # Start new note or continue current
            if current_note is None:
                current_note = midi_note
                current_start = time
            elif abs(midi_note - current_note) > 0.5:  # Note changed
                # Save previous note
                duration = time - current_start
                if duration >= min_duration:
                    notes.append({
                        'time': current_start,
                        'duration': duration,
                        'midi': current_note,
                        'frequency': self.midi_to_frequency(current_note),
                        'note_name': self._midi_to_note_name(current_note)
                    })
                # Start new note
                current_note = midi_note
                current_start = time

        # Add final note
        if current_note is not None:
            duration = times[-1] - current_start
            if duration >= min_duration:
                notes.append({
                    'time': current_start,
                    'duration': duration,
                    'midi': current_note,
                    'frequency': self.midi_to_frequency(current_note),
                    'note_name': self._midi_to_note_name(current_note)
                })

        return notes

    def _midi_to_note_name(self, midi: int) -> str:
        """Convert MIDI number to note name (e.g., 60 -> 'C4')"""
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        octave = (midi // 12) - 1
        note = notes[midi % 12]
        return f"{note}{octave}"
