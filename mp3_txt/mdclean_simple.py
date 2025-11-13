#!/usr/bin/env python3
"""
mdclean_simple - Clean transcriptions using Ollama only (no Unstructured dependency)

This is a simpler version that just uses Ollama for cleaning.
Works immediately without waiting for Unstructured installation.

Usage:
    # Auto-detect and use best available model
    python3 mdclean_simple.py input.md output.md

    # Specify a model explicitly
    python3 mdclean_simple.py input.md output.md --model qwen2.5:0.5b

    # List available models
    python3 mdclean_simple.py --list-models
"""

import re
import sys
from pathlib import Path
from typing import Tuple, List
import argparse
import subprocess
import json


def list_ollama_models() -> List[dict]:
    """Get list of available Ollama models."""
    try:
        result = subprocess.run(
            ['ollama', 'list'],
            capture_output=True,
            text=True,
            check=True
        )

        lines = result.stdout.strip().split('\n')[1:]  # Skip header
        models = []

        for line in lines:
            parts = line.split()
            if len(parts) >= 4:
                name = parts[0]
                size = ' '.join(parts[2:4])  # "1.9 GB" or "397 MB"
                models.append({'name': name, 'size': size})

        return models
    except Exception as e:
        print(f"Error listing Ollama models: {e}")
        return []


def choose_best_model() -> str:
    """
    Choose the best available model for current system.
    Prioritizes smaller models for 8GB RAM systems.
    """
    models = list_ollama_models()
    if not models:
        print("Error: No Ollama models found. Run: ollama pull qwen2.5:0.5b")
        sys.exit(1)

    # Prioritize by size (smaller = better for RAM-constrained systems)
    size_priority = {
        'MB': 0,  # Prefer MB models
        'GB': 1,  # GB models second
    }

    def model_priority(model):
        size_str = model['size']
        size_value = float(size_str.split()[0])
        size_unit = size_str.split()[1]
        unit_priority = size_priority.get(size_unit, 999)
        # Return tuple: (unit priority, size value)
        # Smaller is better
        return (unit_priority, size_value)

    sorted_models = sorted(models, key=model_priority)
    return sorted_models[0]['name']


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


def clean_with_ollama(text: str, model: str = 'qwen2.5-coder:3b') -> str:
    """
    Clean transcription using Ollama.

    Uses qwen2.5-coder:3b by default (already installed).
    Can switch to llama3.2:3b when download completes.
    """
    try:
        import ollama
    except ImportError:
        print("Error: ollama not installed. Run: pip install ollama")
        sys.exit(1)

    # Split into chunks (avoid token limits)
    lines = text.strip().split('\n')
    chunks = []
    current_chunk = []
    current_length = 0

    for line in lines:
        line_length = len(line)
        if current_length + line_length > 2000:  # ~500 tokens
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

    print(f"Processing {total} chunks with Ollama ({model})...")

    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i+1}/{total}...", end=' ', flush=True)

        prompt = f"""Clean up this transcript by:
1. Adding proper punctuation (periods, commas, question marks, etc.)
2. Adding proper capitalization
3. Fixing obvious transcription errors
4. Organizing into natural paragraphs (add blank lines between paragraphs)
5. DO NOT summarize or remove content - preserve everything

Transcript:
{chunk}

Cleaned version:"""

        try:
            response = ollama.generate(
                model=model,
                prompt=prompt,
                options={
                    'temperature': 0.2,  # Low for consistency
                    'num_predict': 4096,  # Allow longer output
                }
            )

            cleaned = response['response'].strip()
            cleaned_chunks.append(cleaned)
            print("✓")

        except Exception as e:
            print(f"✗ (error: {e})")
            cleaned_chunks.append(chunk)  # Keep original on error

    return '\n\n'.join(cleaned_chunks)


def main():
    parser = argparse.ArgumentParser(
        description='Clean transcriptions using Ollama (simple version)',
    )

    parser.add_argument('input', type=str, nargs='?', help='Input markdown file')
    parser.add_argument('output', type=str, nargs='?', help='Output markdown file')
    parser.add_argument('--model', type=str,
                        help='Ollama model to use (auto-selects best if not specified)')
    parser.add_argument('--list-models', action='store_true',
                        help='List available Ollama models and exit')

    args = parser.parse_args()

    # Handle --list-models
    if args.list_models:
        models = list_ollama_models()
        if not models:
            print("No Ollama models found.")
            print("Download a model with: ollama pull qwen2.5:0.5b")
            sys.exit(1)

        print("\nAvailable Ollama models:")
        print("-" * 50)
        for model in models:
            print(f"  {model['name']:<25} {model['size']}")
        print("-" * 50)
        print(f"\nRecommended for 8GB RAM: Models under 500MB")
        print(f"Best choice: {choose_best_model()}")
        sys.exit(0)

    # Validate required arguments
    if not args.input or not args.output:
        parser.error("input and output are required (unless using --list-models)")

    # Choose model
    if args.model:
        model = args.model
        print(f"Using specified model: {model}")
    else:
        model = choose_best_model()
        print(f"Auto-selected model: {model}")

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
    cleaned_body = clean_with_ollama(body, model=model)

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
