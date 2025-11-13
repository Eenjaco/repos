#!/usr/bin/env python3
"""
Quick Start Example
Demonstrates basic functionality of the Strudel Sheet Music Converter
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.tuning.werkmeister import WerkmeisterI, EqualTemperament


def example_tuning_systems():
    """Demonstrate tuning system calculations"""

    print("=" * 60)
    print("Tuning System Demonstration")
    print("=" * 60)

    # Create tuning systems
    equal = EqualTemperament(base_frequency=440)
    werk1 = WerkmeisterI(base_frequency=440)

    # Compare frequencies for middle C
    print("\nMiddle C (C4) Frequencies:")
    print("-" * 60)

    c4_equal = equal.calculate_frequency(60)
    c4_werk = werk1.calculate_frequency(60)

    print(f"Equal Temperament:  {c4_equal:.4f} Hz")
    print(f"Werkmeister I:      {c4_werk:.4f} Hz")
    print(f"Difference:         {c4_werk - c4_equal:.4f} Hz")

    # Show frequency table
    print("\n\nFrequency Table Comparison (Octave 4):")
    print("-" * 60)
    print(f"{'Note':<5} {'Equal (Hz)':<12} {'Werkmeister I (Hz)':<20} {'Diff (cents)':<12}")
    print("-" * 60)

    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    for note in notes:
        midi = werk1._note_to_midi(f"{note}4")
        freq_equal = equal.calculate_frequency(midi)
        freq_werk = werk1.calculate_frequency(midi)

        # Calculate cent difference
        cent_diff = 1200 * (freq_werk / freq_equal).bit_length() if freq_werk != freq_equal else 0
        # More accurate cent calculation
        import math
        if freq_werk != freq_equal:
            cent_diff = 1200 * math.log2(freq_werk / freq_equal)
        else:
            cent_diff = 0

        print(f"{note:<5} {freq_equal:>10.2f}  {freq_werk:>10.2f}        {cent_diff:>+8.2f}")

    # Demonstrate pitch bend
    print("\n\nMIDI Pitch Bend Values:")
    print("-" * 60)
    print(f"{'Note':<5} {'MIDI':<6} {'Pitch Bend':<12} {'Cents':<10}")
    print("-" * 60)

    for note in notes[:6]:  # First half of octave
        midi = werk1._note_to_midi(f"{note}4")
        bend = werk1.get_pitch_bend(midi)
        cents = werk1.get_deviation_cents(note)

        print(f"{note:<5} {midi:<6} {bend:>+8d}      {cents:>+7.1f}")

    print("\n")


def example_pdf_processing():
    """Demonstrate PDF processing (if PDF available)"""

    print("=" * 60)
    print("PDF Processing Demonstration")
    print("=" * 60)

    from src.omr.pdf_processor import PDFProcessor

    processor = PDFProcessor(dpi=300)

    print("\nPDF Processor initialized with:")
    print(f"  DPI: {processor.dpi}")
    print("\nTo process a PDF:")
    print("  1. Place PDF in samples/ directory")
    print("  2. Run: processor.convert_to_images('samples/your_file.pdf')")
    print("  3. Images will be ready for OMR processing")

    print("\n")


def example_architecture_overview():
    """Show the pipeline architecture"""

    print("=" * 60)
    print("Pipeline Architecture Overview")
    print("=" * 60)

    pipeline = """
    1. PDF Input
       ↓
    2. PDF → Images (pdf_processor.py)
       ↓
    3. OMR Processing (omr_engine.py) [TODO]
       ↓
    4. MusicXML → MIDI (midi_converter.py) [TODO]
       ↓
    5. Instrument Mapping (mapper.py) [TODO]
       ↓
    6. Tuning Application (temperament.py) ✓
       ↓
    7. Strudel Code Generation (strudel_generator.py) [TODO]
       ↓
    8. Strudel Output
    """

    print(pipeline)

    print("\n✓ = Implemented")
    print("[TODO] = To be implemented")

    print("\n")


def main():
    """Run all examples"""

    print("\n" + "=" * 60)
    print(" Strudel Sheet Music Converter - Quick Start Examples")
    print("=" * 60 + "\n")

    try:
        # Run examples
        example_tuning_systems()
        example_pdf_processing()
        example_architecture_overview()

        print("=" * 60)
        print("Examples completed successfully!")
        print("=" * 60)
        print("\nNext steps:")
        print("  1. Add PDF samples to samples/organ/")
        print("  2. Try: python cli.py show-tuning werkmeister1")
        print("  3. Try: python cli.py compare-tunings C#4")
        print("  4. Read docs/GETTING_STARTED.md for development guide")
        print("\n")

    except ImportError as e:
        print(f"\n✗ Import Error: {e}")
        print("\nMake sure to install requirements:")
        print("  pip install -r requirements.txt")
        return 1

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
