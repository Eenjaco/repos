"""
Werkmeister Temperaments
Historical tuning systems by Andreas Werkmeister (1645-1706)
"""

from .temperament import Temperament


class WerkmeisterI(Temperament):
    """
    Werkmeister I (III) - "Correct Temperament"

    Most famous of Werkmeister's temperaments.
    Good compromise for all keys, widely used for Baroque organ music.
    """

    # Cents deviation from equal temperament
    DEVIATIONS = {
        "C": 0,
        "C#": -10,
        "D": -8,
        "D#": -6,
        "E": -10,
        "F": -2,
        "F#": -8,
        "G": -6,
        "G#": -8,
        "A": -6,
        "A#": -10,
        "B": -4
    }

    def get_deviation_cents(self, note_name: str) -> float:
        """Get cent deviation for this temperament"""
        # Remove octave information if present
        note = note_name[0] + (note_name[1] if len(note_name) > 1 and note_name[1] in "#b" else "")
        return self.DEVIATIONS.get(note, 0)


class WerkmeisterII(Temperament):
    """
    Werkmeister II

    Alternative tuning with different character.
    """

    DEVIATIONS = {
        "C": 0,
        "C#": -12,
        "D": -6,
        "D#": -12,
        "E": -8,
        "F": -2,
        "F#": -10,
        "G": -4,
        "G#": -10,
        "A": -8,
        "A#": -12,
        "B": -6
    }

    def get_deviation_cents(self, note_name: str) -> float:
        note = note_name[0] + (note_name[1] if len(note_name) > 1 and note_name[1] in "#b" else "")
        return self.DEVIATIONS.get(note, 0)


class WerkmeisterIII(Temperament):
    """
    Werkmeister III (IV) - "Septenarius"

    Named for divisions by seven.
    """

    DEVIATIONS = {
        "C": 0,
        "C#": -7,
        "D": -7,
        "D#": -7,
        "E": -7,
        "F": -5,
        "F#": -7,
        "G": -7,
        "G#": -7,
        "A": -7,
        "A#": -7,
        "B": -5
    }

    def get_deviation_cents(self, note_name: str) -> float:
        note = note_name[0] + (note_name[1] if len(note_name) > 1 and note_name[1] in "#b" else "")
        return self.DEVIATIONS.get(note, 0)


class EqualTemperament(Temperament):
    """
    Equal Temperament

    Modern standard tuning (baseline for comparison).
    """

    def get_deviation_cents(self, note_name: str) -> float:
        """No deviation - all intervals equal"""
        return 0.0
