#!/usr/bin/env python3
"""
mdclean_claude - Clean transcriptions using Claude API

High quality cleaning using Claude API. Requires API key but produces
excellent results for punctuation, capitalization, and error correction.

Usage:
    python3 mdclean_claude.py input.md output.md

    # Set API key via environment variable:
    export ANTHROPIC_API_KEY="your-key-here"
    python3 mdclean_claude.py input.md output.md
"""

import re
import sys
import os
from pathlib import Path
from typing import Tuple
import argparse


def extract_frontmatter(content: str) -> Tuple[str, str]:
    """Extract YAML frontmatter from markdown content."""
    if not content.startswith('---\n'):
        return '', content

    parts = content.split('---\n', 2)
    if len(parts) < 3:
        return '', content

    frontmatter = f"---\n{parts[1]}---\n"
    body = parts[2]

    return frontmatter, body


def clean_with_claude(text: str, api_key: str) -> str:
    """
    Clean transcription using Claude API.

    Args:
        text: Raw transcript text
        api_key: Anthropic API key

    Returns:
        Cleaned text with proper punctuation and structure
    """
    try:
        import anthropic
    except ImportError:
        print("Error: anthropic package not installed. Run: pip install anthropic")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    # Split into chunks (~4000 chars each to stay well under token limits)
    lines = text.strip().split('\n')
    chunks = []
    current_chunk = []
    current_length = 0

    for line in lines:
        line_length = len(line)
        if current_length + line_length > 4000:
            if current_chunk:
                chunks.append('\n'.join(current_chunk))
            current_chunk = [line]
            current_length = line_length
        else:
            current_chunk.append(line)
            current_length += line_length

    if current_chunk:
        chunks.append('\n'.join(current_chunk))

    # Process each chunk
    cleaned_chunks = []
    total = len(chunks)

    print(f"Processing {total} chunks with Claude API...")

    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i+1}/{total}...", end=' ', flush=True)

        prompt = f"""Clean up this transcript by:
1. Adding proper punctuation (periods, commas, question marks, etc.)
2. Adding proper capitalization
3. Fixing obvious transcription errors (homophones, mishearings)
4. Organizing into natural paragraphs (add blank lines between paragraphs)
5. Preserving ALL content - do not summarize or remove anything

Return ONLY the cleaned transcript, no explanations or meta-commentary.

Transcript:
{chunk}"""

        try:
            message = client.messages.create(
                model="claude-3-5-haiku-20241022",  # Fast, cost-effective
                max_tokens=8000,
                temperature=0.3,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            cleaned = message.content[0].text.strip()
            cleaned_chunks.append(cleaned)
            print("✓")

        except Exception as e:
            print(f"✗ (error: {e})")
            cleaned_chunks.append(chunk)  # Keep original on error

    return '\n\n'.join(cleaned_chunks)


def main():
    parser = argparse.ArgumentParser(
        description='Clean transcriptions using Claude API',
    )

    parser.add_argument('input', type=str, help='Input markdown file')
    parser.add_argument('output', type=str, help='Output markdown file')
    parser.add_argument('--api-key', type=str,
                        help='Anthropic API key (or set ANTHROPIC_API_KEY env var)')

    args = parser.parse_args()

    # Get API key
    api_key = args.api_key or os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("Error: No API key provided.")
        print("  Set via --api-key flag or ANTHROPIC_API_KEY environment variable")
        print("  Get your key at: https://console.anthropic.com/")
        sys.exit(1)

    # Read input
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)

    print(f"Reading: {args.input}")
    content = input_path.read_text()

    # Extract frontmatter
    frontmatter, body = extract_frontmatter(content)

    # Clean
    cleaned_body = clean_with_claude(body, api_key)

    # Recombine
    final_content = frontmatter + '\n' + cleaned_body if frontmatter else cleaned_body

    # Write output
    output_path = Path(args.output)
    output_path.write_text(final_content)

    print(f"\n✅ Cleaned transcript saved to: {args.output}")
    print(f"\nStats:")
    print(f"  Input:  {len(content)} chars, {len(content.splitlines())} lines")
    print(f"  Output: {len(final_content)} chars, {len(final_content.splitlines())} lines")


if __name__ == '__main__':
    main()
