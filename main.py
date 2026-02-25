"""
Wordle Clone - Tkinter OOP Version

Written by Jose "Joe" Ruiz

This file sets up the basic structure of the project.
"""
# Tkinter is the built-in GUI library for Python.
# It lets us create windows, buttons, labels, and handle events.

import tkinter as tk

# pathlib gives us an object-oriented way to work with file paths.

import pathlib

# random will be used to pick a random word from the word list.

import random

# ascii_letters helps us validate that a word contains only letters.

from string import ascii_letters

# --------------------------------------------------------------------
# WordSelector: Loads and filters the word list
# --------------------------------------------------------------------

class WordSelector:
    """
    This class is responsible ONLY for:
    - reading the wordlist file
    - filtering valid words
    - choosing a random answer

    It does NOT know anything about the UI or game rules.
    """

    def __init__(self, path: pathlib.Path, length: int):
        self.path = path
        self.length = length
        self.words = self._load_words()

    def _load_words(self):
        """Read the file and return a list of valid uppercase words."""
        raw_words = self.path.read_text(encoding="utf-8").split("\n")

        # Filter words:

        # - correct length

        # - only letters

        valid_words = [
            word.upper()
            for word in raw_words
            if len(word) == self.length and all(char in ascii_letters for char in word)

        ]
        if not valid_words:
            raise ValueError("No valid words found in wordlist.txt")

        return valid_words

    def choose(self):
        """Return a random word from the valid list."""
        return random.choice(self.words)

# --------------------------------------------------------------------
# WordEngine: Game logic (no UI)
# --------------------------------------------------------------------

class WordEngine:
    """
    This class handles:
    - storing the answer
    - evaluating guesses

    It does NOT know anything about Tkinter or the UI.
    """

    def __init__(self, answer: str):
        self.answer = answer

    def evaluate(self, guess: str):
        """
        Compare guess to answer and return a list of statuses:
        - "correct" (right letter, right place)
        - "misplaced" (right letter, wrong place)
        - "wrong" (letter not in word)
        """
        result = []

        for guess_letter, answer_letter in zip(guess, self.answer):
            if guess_letter == answer_letter:
                result.append("correct")
            elif guess_letter in self.answer:
                result.append("misplaced")
            else:
                result.append("wrong")

        return result

# --------------------------------------------------------------------
# TileGrid: The 6x5 grid of letter tiles
# --------------------------------------------------------------------

class TileGrid:
    """
    This class draws the Wordle board:
    - 6 rows (guesses)
    -5 columns (letters)

    Each tile is a Tkinter Label widget.
    """

    def __init__(self, root, rows=6, cols=5):
        self.root = root
        self.rows = rows
        self.cols = cols

        # Store references to each tile so we can update them later.

        self.tiles = []

        # A frame groups the tiles together visually.

        frame = tk.Frame(root)
        frame.pack(pady=20)

        # Create the grid of labels.

        for row_index in range(rows):
            row_tiles = []
            for column_index in range(cols):
                tile_label = tk.Label(
                    frame,
                    text="",
                    width=4,
                    height=2,
                    font=("Helvetica", 24),
                    relief="solid",
                    borderwidth=1,
                )
                tile_label.grid(row=row_index, column=column_index, padx=3, pady=3)
                row_tiles.append(tile_label)
            self.tiles.append(row_tiles)

# --------------------------------------------------------------------
# Keyboard: On-screen Keyboard
# --------------------------------------------------------------------

class Keyboard:
    """
    This class draws the on-screen keyboard.
    It does NOT handle game logic - only UI buttons.
    """

    def __init__(self, root, on_key, on_backspace, on_enter):
        self.root = root
        self.on_key = on_key  # callback function
        self.on_backspace = on_backspace
        self.on_enter = on_enter
        self.buttons = {}

        layout = [
            list("QWERTYUIOP"),
            list("ASDFGHJKL"),
            ["ENTER"] + list("ZXCVBNM") + ["←"]
        ]

        frame = tk.Frame(root)
        frame.pack()

        for keyboard_row in layout:
            row_frame = tk.Frame(frame)
            row_frame.pack()

            for letter in keyboard_row:
                if letter == "←":
                    button = tk.Button(
                        row_frame,
                        text="←",
                        width=4,
                        command=self.on_backspace
                    )
                elif letter == "ENTER":
                    button = tk.Button(
                        row_frame,
                        text="ENTER",
                        width=6,
                        command=self.on_enter
                    )
                else:
                    button = tk.Button(
                    row_frame,
                    text=letter,
                    width=4,
                    command=lambda selected_letter=letter: self.on_key(selected_letter),
                )
                button.pack(side="left", padx=2, pady=2)
                self.buttons[letter] = button

# --------------------------------------------------------------------
# WordleGame: Main controller
# --------------------------------------------------------------------

class WordleGame:
    """
    This class ties everything together:
    - loads the answer
    - creates the UI
    - handles Key presses
    - tracks the current guess

    It is the "brain" of the application.
    """

    def __init__(self, root):
        self.root = root
        self.word_length = 5
        self.max_guesses = 6

        # Load a random answer

        selector = WordSelector(
            pathlib.Path(__file__).parent / "wordlist.txt",
            self.word_length,
        )
        self.answer = selector.choose()

        # Create the game engine

        self.engine = WordEngine(self.answer)

        # Create the UI components

        self.grid = TileGrid(root, self.max_guesses, self.word_length)
        self.keyboard = Keyboard(root, self.handle_key, self.handle_backspace,
                                 self.handle_enter)


        # Track typing state

        self.current_row_index = 0
        self.current_column_index = 0
        self.current_guess_text = ""

    def handle_key(self, pressed_letter):
        print("Pressed:", pressed_letter)  # Debugging statement to verify key presses
        """
        This method is called whenever the user clicks a keyboard button.
        """
        if self.current_column_index >= self.word_length:
            return

        # Place the letter in the tile

        tile = self.grid.tiles[self.current_row_index][self.current_column_index]
        tile.config(text=pressed_letter)

        # Update guess text

        self.current_guess_text += pressed_letter

        # Move to next column

        self.current_column_index += 1

    def handle_backspace(self):
        print("BACKSPACE pressed")  # Debugging statement to verify backspace presses
        if self.current_column_index == 0:
            return

        self.current_column_index -= 1

        tile = self.grid.tiles[self.current_row_index][self.current_column_index]
        tile.config(text="")

        self.current_guess_text = self.current_guess_text[:-1]

    def handle_enter(self):
        print("ENTER pressed")  # Debugging statement to verify enter presses
        # your upcoming enter logic here

        if len(self.current_guess_text) < self.word_length:
            return  # later: yellow warning

# --------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Wordle - Tkinter by Joe Ruiz")
    game = WordleGame(root)
    root.mainloop()






