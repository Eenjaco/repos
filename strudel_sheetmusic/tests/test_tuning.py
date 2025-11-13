"""
Tests for tuning systems
"""

import pytest
from src.tuning.werkmeister import WerkmeisterI, WerkmeisterII, WerkmeisterIII, EqualTemperament


class TestWerkmeisterI:
    """Test Werkmeister I (III) temperament"""

    def test_initialization(self):
        """Test tuning system initialization"""
        tuning = WerkmeisterI(base_frequency=440)
        assert tuning.base_frequency == 440
        assert tuning.reference_note == "A4"

    def test_equal_temperament_baseline(self):
        """Test equal temperament as baseline (no deviations)"""
        equal = EqualTemperament(base_frequency=440)
        assert equal.get_deviation_cents("C") == 0
        assert equal.get_deviation_cents("F#") == 0

    def test_werkmeister_deviations(self):
        """Test Werkmeister I has expected deviations"""
        tuning = WerkmeisterI()

        # C should be reference (0 cents)
        assert tuning.get_deviation_cents("C") == 0

        # Other notes should have negative deviations (flatter)
        assert tuning.get_deviation_cents("C#") == -10
        assert tuning.get_deviation_cents("D") == -8
        assert tuning.get_deviation_cents("E") == -10
        assert tuning.get_deviation_cents("F") == -2

    def test_frequency_calculation(self):
        """Test frequency calculation for A4"""
        tuning = WerkmeisterI(base_frequency=440)

        # A4 (MIDI 69) with -6 cents deviation
        # Should be slightly flat of 440
        a4_freq = tuning.calculate_frequency(69)
        assert 438 < a4_freq < 440

        # C4 (MIDI 60) with 0 cents deviation
        # Should be exactly equal temperament value
        c4_freq = tuning.calculate_frequency(60)
        expected_c4 = 440 * (2 ** (-9/12))  # 9 semitones below A4
        assert abs(c4_freq - expected_c4) < 0.1

    def test_frequency_table(self):
        """Test generating frequency table"""
        tuning = WerkmeisterI()
        table = tuning.get_frequency_table(octave=4)

        assert len(table) == 12
        assert "C" in table
        assert "F#" in table
        assert all(isinstance(freq, float) for freq in table.values())

    def test_pitch_bend_calculation(self):
        """Test MIDI pitch bend calculation"""
        tuning = WerkmeisterI()

        # C has 0 deviation, so pitch bend should be 0
        c_bend = tuning.get_pitch_bend(60)
        assert c_bend == 0

        # C# has -10 cents, should have negative pitch bend
        cs_bend = tuning.get_pitch_bend(61)
        assert cs_bend < 0
        assert -500 < cs_bend < 0  # Reasonable range

    def test_pitch_bend_range(self):
        """Test pitch bend stays within MIDI range"""
        tuning = WerkmeisterI()

        for midi_note in range(0, 128):
            bend = tuning.get_pitch_bend(midi_note)
            assert -8192 <= bend <= 8191


class TestWerkmeisterII:
    """Test Werkmeister II temperament"""

    def test_different_from_werkmeister_i(self):
        """Test that Werkmeister II differs from Werkmeister I"""
        w1 = WerkmeisterI()
        w2 = WerkmeisterII()

        # They should have different deviations
        assert w1.get_deviation_cents("C#") != w2.get_deviation_cents("C#")


class TestWerkmeisterIII:
    """Test Werkmeister III (IV) Septenarius"""

    def test_septenarius_pattern(self):
        """Test characteristic -7 cent pattern"""
        tuning = WerkmeisterIII()

        # Most notes should have -7 cents
        assert tuning.get_deviation_cents("C#") == -7
        assert tuning.get_deviation_cents("D") == -7
        assert tuning.get_deviation_cents("E") == -7


class TestTemperamentBase:
    """Test base Temperament class functionality"""

    def test_note_to_midi_conversion(self):
        """Test note name to MIDI number conversion"""
        from src.tuning.temperament import Temperament

        assert Temperament._note_to_midi("C4") == 60
        assert Temperament._note_to_midi("A4") == 69
        assert Temperament._note_to_midi("C#4") == 61
        assert Temperament._note_to_midi("Bb3") == 58

    def test_midi_to_note_name(self):
        """Test MIDI number to note name conversion"""
        from src.tuning.temperament import Temperament

        assert Temperament._midi_to_note_name(60) == "C"
        assert Temperament._midi_to_note_name(69) == "A"
        assert Temperament._midi_to_note_name(61) == "C#"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
