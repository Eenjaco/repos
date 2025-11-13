"""
Base Temperament Class
Foundation for all tuning systems
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict
import math


@dataclass
class Note:
    """Represents a musical note"""
    pitch: int  # MIDI note number
    name: str   # Note name (e.g., "C4", "F#5")


class Temperament(ABC):
    """
    Abstract base class for tuning systems
    """

    def __init__(self, base_frequency: float = 440.0, reference_note: str = "A4"):
        """
        Initialize temperament

        Args:
            base_frequency: Frequency of reference note in Hz
            reference_note: MIDI note name for reference (default A4)
        """
        self.base_frequency = base_frequency
        self.reference_note = reference_note
        self.reference_midi = self._note_to_midi(reference_note)

    @abstractmethod
    def get_deviation_cents(self, note_name: str) -> float:
        """
        Get cent deviation from equal temperament for a note

        Args:
            note_name: Note name (e.g., "C", "F#")

        Returns:
            Deviation in cents (positive = sharper, negative = flatter)
        """
        pass

    def calculate_frequency(self, midi_note: int) -> float:
        """
        Calculate frequency for a MIDI note in this temperament

        Args:
            midi_note: MIDI note number (0-127)

        Returns:
            Frequency in Hz
        """
        # Get note name without octave
        note_name = self._midi_to_note_name(midi_note)

        # Start with equal temperament frequency
        semitones_from_ref = midi_note - self.reference_midi
        equal_freq = self.base_frequency * (2 ** (semitones_from_ref / 12))

        # Apply temperament deviation
        deviation_cents = self.get_deviation_cents(note_name)
        frequency = equal_freq * (2 ** (deviation_cents / 1200))

        return frequency

    def get_pitch_bend(self, midi_note: int) -> int:
        """
        Calculate MIDI pitch bend value for this note

        Args:
            midi_note: MIDI note number

        Returns:
            Pitch bend value (-8192 to +8191)
        """
        note_name = self._midi_to_note_name(midi_note)
        deviation_cents = self.get_deviation_cents(note_name)

        # MIDI pitch bend: ±2 semitones = ±200 cents = ±8192
        # 1 cent ≈ 40.96 pitch bend units
        pitch_bend = int((deviation_cents / 200) * 8192)

        # Clamp to valid range
        return max(-8192, min(8191, pitch_bend))

    def get_frequency_table(self, octave: int = 4) -> Dict[str, float]:
        """
        Generate frequency table for one octave

        Args:
            octave: Octave number

        Returns:
            Dictionary mapping note names to frequencies
        """
        notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        return {
            note: self.calculate_frequency(self._note_to_midi(f"{note}{octave}"))
            for note in notes
        }

    @staticmethod
    def _note_to_midi(note_name: str) -> int:
        """Convert note name to MIDI number (e.g., 'A4' -> 69)"""
        note_map = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}

        note = note_name[0].upper()
        octave = int(note_name[-1])

        midi = note_map[note] + (octave + 1) * 12

        # Handle sharps and flats
        if "#" in note_name or "♯" in note_name:
            midi += 1
        elif "b" in note_name or "♭" in note_name:
            midi -= 1

        return midi

    @staticmethod
    def _midi_to_note_name(midi_note: int) -> str:
        """Convert MIDI number to note name without octave"""
        notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        return notes[midi_note % 12]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(base={self.base_frequency}Hz)"
