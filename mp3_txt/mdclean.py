#!/usr/bin/env python3
"""
mdclean - Clean and structure raw transcriptions

Modes:
  fast    - Unstructured-based structure detection (paragraphs, headings)
  quality - Unstructured + Ollama for punctuation, grammar, error correction

Usage:
    python3 mdclean.py input.md output.md --mode fast
    python3 mdclean.py input.md output.md --mode quality
"""

import re
import sys
from pathlib import Path
from typing import Tuple
import argparse


def extract_frontmatter(content: str) -> Tuple[str, str]:
    """
    Extract YAML frontmatter from markdown content.

    Returns:
        (frontmatter, body) - frontmatter includes the --- delimiters
    """
    if not content.startswith('---\n'):
        return '', content

    # Find the closing ---
    parts = content.split('---\n', 2)
    if len(parts) < 3:
        return '', content

    frontmatter = f"---\n{parts[1]}---\n"
    body = parts[2]

    return frontmatter, body


def clean_fast_mode(text: str) -> str:
    """
    Fast mode: Structure detection using basic NLP.

    - Detect paragraph breaks (topic changes)
    - Basic capitalization and punctuation inference
    - Preserve content, improve readability
    """
    # Import here to avoid loading if not needed
    try:
        from unstructured.partition.text import partition_text
        from unstructured.staging.base import elements_to_text
    except ImportError:
        print("Error: unstructured not installed. Run: pip install 'unstructured[all-docs]'")
        sys.exit(1)

    # Partition text into semantic elements
    elements = partition_text(text=text)

    # Group elements into paragraphs
    paragraphs = []
    current_paragraph = []

    for elem in elements:
        elem_text = str(elem).strip()
        if not elem_text:
            continue

        # Check if this is likely a new paragraph
        # (Unstructured detects NarrativeText, Title, ListItem, etc.)
        elem_type = type(elem).__name__

        if elem_type == 'Title':
            # Flush current paragraph
            if current_paragraph:
                paragraphs.append(' '.join(current_paragraph))
                current_paragraph = []
            # Add title as its own paragraph
            paragraphs.append(f"## {elem_text}")
        elif elem_type == 'ListItem':
            # Flush current paragraph
            if current_paragraph:
                paragraphs.append(' '.join(current_paragraph))
                current_paragraph = []
            # Add list item
            paragraphs.append(f"- {elem_text}")
        else:
            # NarrativeText or other - accumulate
            current_paragraph.append(elem_text)

    # Flush remaining paragraph
    if current_paragraph:
        paragraphs.append(' '.join(current_paragraph))

    # Join paragraphs with double newlines
    return '\n\n'.join(paragraphs)


def clean_quality_mode(text: str) -> str:
    """
    Quality mode: Unstructured + Ollama for best results.

    - Structure detection (Unstructured)
    - Punctuation, capitalization, grammar (Ollama)
    - Error correction (Ollama)
    """
    try:
        import ollama
    except ImportError:
        print("Error: ollama not installed. Run: pip install ollama")
        sys.exit(1)

    # First pass: Structure detection with Unstructured
    structured_text = clean_fast_mode(text)

    # Second pass: Polish with Ollama
    # Process in chunks to avoid token limits
    paragraphs = structured_text.split('\n\n')
    cleaned_paragraphs = []

    print("Polishing with Ollama (this may take a few minutes)...")

    for i, paragraph in enumerate(paragraphs):
        if not paragraph.strip():
            cleaned_paragraphs.append('')
            continue

        # Skip headings and list items (already formatted)
        if paragraph.startswith('##') or paragraph.startswith('-'):
            cleaned_paragraphs.append(paragraph)
            continue

        print(f"  Processing paragraph {i+1}/{len(paragraphs)}...")

        # Send to Ollama for cleaning
        prompt = f"""Fix this transcription by adding proper punctuation and capitalization.
Correct obvious transcription errors (homophones, mishearings).
Preserve ALL content - do not summarize or remove anything.
Output only the corrected text, nothing else.

Transcript:
{paragraph}

Corrected:"""

        try:
            response = ollama.generate(
                model='llama3.2:3b',
                prompt=prompt,
                options={'temperature': 0.3}  # Lower temperature for consistency
            )

            cleaned = response['response'].strip()
            cleaned_paragraphs.append(cleaned)
        except Exception as e:
            print(f"    Warning: Ollama error for paragraph {i+1}: {e}")
            print(f"    Keeping original paragraph")
            cleaned_paragraphs.append(paragraph)

    return '\n\n'.join(cleaned_paragraphs)


def main():
    parser = argparse.ArgumentParser(
        description='Clean and structure raw transcriptions',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fast mode (structure detection only)
  python3 mdclean.py input.md output.md --mode fast

  # Quality mode (structure + LLM polish)
  python3 mdclean.py input.md output.md --mode quality
"""
    )

    parser.add_argument('input', type=str, help='Input markdown file')
    parser.add_argument('output', type=str, help='Output markdown file')
    parser.add_argument('--mode', type=str, choices=['fast', 'quality'],
                        default='fast', help='Cleaning mode (default: fast)')

    args = parser.parse_args()

    # Read input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)

    print(f"Reading: {args.input}")
    content = input_path.read_text()

    # Extract frontmatter
    frontmatter, body = extract_frontmatter(content)

    # Clean based on mode
    print(f"Mode: {args.mode}")

    if args.mode == 'fast':
        cleaned_body = clean_fast_mode(body)
    elif args.mode == 'quality':
        cleaned_body = clean_quality_mode(body)
    else:
        print(f"Error: Unknown mode: {args.mode}")
        sys.exit(1)

    # Recombine with frontmatter
    final_content = frontmatter + '\n' + cleaned_body if frontmatter else cleaned_body

    # Write output
    output_path = Path(args.output)
    output_path.write_text(final_content)

    print(f"✅ Cleaned transcript saved to: {args.output}")
    print(f"\nStats:")
    print(f"  Input:  {len(content)} chars, {len(content.splitlines())} lines")
    print(f"  Output: {len(final_content)} chars, {len(final_content.splitlines())} lines")


if __name__ == '__main__':
    main()
