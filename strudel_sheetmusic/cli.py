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

try:
    from src.audio.audio_analyzer import AudioAnalyzer
    from src.audio.pitch_detector import PitchDetector
    from src.audio.chord_detector import ChordDetector
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False


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


def cmd_analyze_audio(args):
    """Analyze audio file for musical features"""
    if not AUDIO_AVAILABLE:
        print("✗ Audio analysis not available. Install dependencies:", file=sys.stderr)
        print("  pip install -r requirements_audio.txt")
        return 1

    print(f"Analyzing audio: {args.audio_file}")
    print("-" * 60)

    try:
        analyzer = AudioAnalyzer()

        # Full analysis
        results = analyzer.analyze_full(args.audio_file)

        # Print results
        print(f"\n📁 File: {results['file']}")
        print(f"⏱️  Duration: {results['duration']:.2f}s")
        print(f"🎵 BPM: {results['bpm']:.1f}")
        print(f"🎹 Key: {results['key']} {results['mode']}")
        print(f"🥁 Beats detected: {results['beat_count']}")

        if args.show_beats:
            print(f"\nFirst 10 beat positions:")
            for i, beat in enumerate(results['beat_positions'][:10], 1):
                print(f"  Beat {i:2d}: {beat:6.2f}s")

        # Chord detection if requested
        if args.detect_chords:
            print("\n🎸 Detecting chords...")
            audio = analyzer.audio_data
            chord_detector = ChordDetector()
            chords = chord_detector.detect_chord_progression(
                audio,
                segment_length=args.chord_segment,
                min_confidence=0.5
            )

            print(f"Found {len(chords)} chord changes:")
            for chord in chords[:20]:  # Show first 20
                print(f"  {chord['time']:6.2f}s: {chord['chord']:>7} "
                      f"({chord['confidence']:.2f})")

        # Melody extraction if requested
        if args.extract_melody:
            print("\n🎼 Extracting melody...")
            try:
                melody = analyzer.extract_melody()
                print(f"Found {len(melody)} notes:")
                for note in melody[:20]:  # Show first 20
                    print(f"  {note['time']:6.2f}s: {note['note_name']:>4} "
                          f"({note['duration']:.2f}s)")
            except NotImplementedError:
                print("  ℹ️  Melody extraction requires basic-pitch")
                print("  Install with: pip install basic-pitch")

        print("\n✓ Analysis complete!")

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        import traceback
        if args.verbose:
            traceback.print_exc()
        return 1

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

  # Analyze audio file
  %(prog)s analyze-audio song.mp3
  %(prog)s analyze-audio song.mp3 --detect-chords --extract-melody
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

    # Audio analysis command
    if AUDIO_AVAILABLE:
        audio_parser = subparsers.add_parser("analyze-audio", help="Analyze audio file")
        audio_parser.add_argument("audio_file", help="Input audio file (mp3, wav, etc.)")
        audio_parser.add_argument("--detect-chords", action="store_true",
                                 help="Detect chord progression")
        audio_parser.add_argument("--extract-melody", action="store_true",
                                 help="Extract main melody")
        audio_parser.add_argument("--show-beats", action="store_true",
                                 help="Show beat positions")
        audio_parser.add_argument("--chord-segment", type=float, default=2.0,
                                 help="Chord detection segment length (default: 2.0s)")
        audio_parser.add_argument("-v", "--verbose", action="store_true",
                                 help="Verbose output")

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

    if AUDIO_AVAILABLE:
        commands["analyze-audio"] = cmd_analyze_audio

    if args.command not in commands:
        print(f"✗ Unknown command: {args.command}", file=sys.stderr)
        parser.print_help()
        return 1

    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
