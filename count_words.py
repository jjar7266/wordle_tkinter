"""
count_words.py
A small reusable utility script for analyzing word list files.

Purpose:
    - Count total words in any text file.
    - Count how many of those words are exactly 5 letters long.
    - Designed to work with ANY word list (words.txt, enable.txt, etc.)
    - Useful for Wordle-style games or dictionary cleanup.

Usage:
    python count_words.py words.txt
    python count_words.py my_dictionary.txt

Notes:
    - The script expects one word per line.
    - It ignores blank lines.
    - It does NOT modify your files — read-only analysis.
"""

import sys
import pathlib


def count_five_letter_words(path):
    """Load the file, count total words and 5-letter words, and print results."""
    file_path = pathlib.Path(path)

    # Validate file exists before attempting to read
    if not file_path.exists():
        print(f"Error: File not found → {file_path}")
        return

    # Read all non-empty lines
    with open(file_path, "r", encoding="utf-8") as f:
        words = [w.strip() for w in f if w.strip()]

    # Filter for exactly 5-letter words
    five_letter = [w for w in words if len(w) == 5]

    # Display results
    print(f"\nAnalyzing file: {file_path.name}")
    print(f"Total words: {len(words)}")
    print(f"5-letter words: {len(five_letter)}\n")


if __name__ == "__main__":
    # Require a filename argument
    if len(sys.argv) < 2:
        print("Usage: python count_words.py <filename>")
    else:
        count_five_letter_words(sys.argv[1])
