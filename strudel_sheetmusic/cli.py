#!/usr/bin/env python3
"""
Strudel Sheet Music Converter - Command Line Interface
Basic CLI for testing and development
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.omr.pdf_processor import PDFProcessor
from src.tuning.werkmeister import WerkmeisterI, WerkmeisterII, WerkmeisterIII, EqualTemperament


def cmd_pdf_to_images(args):
    """Convert PDF to images"""
    print(f"Converting PDF: {args.pdf_file}")

    processor = PDFProcessor(dpi=args.dpi)

    try:
        # Convert PDF to images
        images = processor.convert_to_images(args.pdf_file)
        print(f"✓ Converted {len(images)} pages")

        # Save images if output directory specified
        if args.output:
            Path(args.output).mkdir(parents=True, exist_ok=True)
            saved_paths = processor.save_images(images, args.output, prefix="page")
            print(f"✓ Saved images to {args.output}")
            for path in saved_paths:
                print(f"  - {path}")
        else:
            print("ℹ No output directory specified, images not saved")

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1

    return 0


def cmd_show_tuning(args):
    """Show tuning system information"""

    # Select tuning system
    tunings = {
        "equal": EqualTemperament,
        "werkmeister1": WerkmeisterI,
        "werkmeister2": WerkmeisterII,
        "werkmeister3": WerkmeisterIII,
    }

    if args.tuning not in tunings:
        print(f"✗ Unknown tuning: {args.tuning}", file=sys.stderr)
        print(f"Available tunings: {', '.join(tunings.keys())}")
        return 1

    tuning_class = tunings[args.tuning]
    tuning = tuning_class(base_frequency=args.base_freq)

    print(f"\n{tuning}")
    print(f"Base frequency: {args.base_freq} Hz (A4)")
    print("\nFrequency Table (Octave 4):")
    print("-" * 40)

    table = tuning.get_frequency_table(octave=4)
    for note, freq in table.items():
        deviation = tuning.get_deviation_cents(note)
        deviation_str = f"{deviation:+.1f}" if deviation != 0 else " 0.0"
        print(f"{note:>3}4: {freq:7.2f} Hz  ({deviation_str} cents)")

    # Show pitch bend values if requested
    if args.show_bend:
        print("\nMIDI Pitch Bend Values:")
        print("-" * 40)
        for note in ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]:
            midi = tuning._note_to_midi(f"{note}4")
            bend = tuning.get_pitch_bend(midi)
            print(f"{note:>3}4 (MIDI {midi:3d}): {bend:+6d}")

    return 0


def cmd_compare_tunings(args):
    """Compare multiple tuning systems"""
    print(f"\nTuning Comparison for {args.note}\n")
    print("-" * 60)

    tunings = {
        "Equal": EqualTemperament(),
        "Werkmeister I": WerkmeisterI(),
        "Werkmeister II": WerkmeisterII(),
        "Werkmeister III": WerkmeisterIII(),
    }

    # Parse note (e.g., "C4")
    try:
        midi = WerkmeisterI._note_to_midi(args.note)
        note_name = WerkmeisterI._midi_to_note_name(midi)
    except:
        print(f"✗ Invalid note: {args.note}", file=sys.stderr)
        return 1

    print(f"{'Temperament':<20} {'Frequency':<12} {'Deviation':<12}")
    print("-" * 60)

    for name, tuning in tunings.items():
        freq = tuning.calculate_frequency(midi)
        deviation = tuning.get_deviation_cents(note_name)
        print(f"{name:<20} {freq:>8.2f} Hz  {deviation:>+7.1f} cents")

    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Strudel Sheet Music Converter CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert PDF to images
  %(prog)s pdf-to-images sheet_music.pdf -o output/

  # Show tuning information
  %(prog)s show-tuning werkmeister1

  # Compare tunings for specific note
  %(prog)s compare-tunings C#4
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # PDF to images command
    pdf_parser = subparsers.add_parser("pdf-to-images", help="Convert PDF to images")
    pdf_parser.add_argument("pdf_file", help="Input PDF file")
    pdf_parser.add_argument("-o", "--output", help="Output directory for images")
    pdf_parser.add_argument("-d", "--dpi", type=int, default=300, help="DPI (default: 300)")

    # Show tuning command
    tuning_parser = subparsers.add_parser("show-tuning", help="Show tuning system info")
    tuning_parser.add_argument(
        "tuning",
        choices=["equal", "werkmeister1", "werkmeister2", "werkmeister3"],
        help="Tuning system"
    )
    tuning_parser.add_argument("-f", "--base-freq", type=float, default=440.0,
                              help="Base frequency for A4 (default: 440)")
    tuning_parser.add_argument("-b", "--show-bend", action="store_true",
                              help="Show MIDI pitch bend values")

    # Compare tunings command
    compare_parser = subparsers.add_parser("compare-tunings", help="Compare tuning systems")
    compare_parser.add_argument("note", help="Note to compare (e.g., C4, F#5)")

    # Parse arguments
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Run command
    commands = {
        "pdf-to-images": cmd_pdf_to_images,
        "show-tuning": cmd_show_tuning,
        "compare-tunings": cmd_compare_tunings,
    }

    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
