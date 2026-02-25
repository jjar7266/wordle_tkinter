"""
Wordle Clone - Tkinter OOP Version

Written by Jose "Joe" Ruiz

This file sets up the basic structure of the project.
"""
# Tkinter is the built-in GUI library for Python.
# It lets us create windows, buttons, labels, and handle events.

# --------------------------------------------------------------------
# TODO LIST — Next Development Phase
# --------------------------------------------------------------------
# GAME OVER FLOW
# - Add game_over flag to block input after win/lose.
# - Create Game Over popup (win/lose message, correct word).
# - Add Play Again and Quit buttons.
# - Disable keyboard input when game ends.
# - Detect loss after 6 guesses.

# RESTART LOGIC
# - Implement restart_game() to reset:
#     - grid tiles
#     - keyboard colors
#     - row/column indices
#     - current_guess_text
#     - game_over flag
#     - answer + engine

# UI POLISH
# - Decide on dark/light theme for TileGrid.
# - Add tile flip animation (optional).
# - Add bounce animation on correct guess (optional).

# CODE QUALITY
# - Add initialization block for all attributes.
# - Remove debug prints once stable.
# - Add docstrings to new methods.
# - Add helper to reset keyboard colors.

# TESTING
# - Test win flow.
# - Test loss flow.
# - Test restart flow.
# - Test keyboard disabling.
# - Test repeated letters and edge cases.

# FUTURE FEATURES (Optional)
# - Hard mode.
# - Stats screen.
# - Daily mode.
# - Sound effects.
# - Settings menu.
# --------------------------------------------------------------------

import tkinter as tk
import pathlib
import random
from string import ascii_letters

# ... rest of your code ...

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

    It does NOT know anything about:
    - the UI
    - the keyboard
    - tile colors
    - game rules or scoring

    This separation keeps the project modular and easy to maintain.
    """

    def __init__(self, path: pathlib.Path, length: int):
        """
        Parameters:
          - path (pathlib.Path): The file path to the word list (wordlist.txt)
          - length (int): The required word length (Wordle uses 5.)

        When the class is created, we immediately load and filter
        the word list so the game has a clean set of valid words.
        """
        self.path = path
        self.length = length

        # Load and store the filtered list of valid words.

        self.words = self._load_words()

    def _load_words(self):
        """
        Read the file and return a list of valid uppercase words.

        A "valid" word must:
            - be exactly the required length
            - contain only alphbetic characters (A-Z)
            - be safe to use as a Wordle guess or answer

        This method is private (underscore prefix) because it is
        only used internally during initialization.
        """

        # Read the entire file as one string, then split into lines.

        raw_words = self.path.read_text(encoding="utf-8").split("\n")

        # Filter the raw list into a clean list of valid words.

        valid_words = [
            word.upper()
            for word in raw_words
            if len(word) == self.length and all(char in ascii_letters for char in word)

        ]

        # If the file contains no usable words, fail early.

        if not valid_words:
            raise ValueError("No valid words found in wordlist.txt")

        return valid_words

    def choose(self):
        """
        Return a random word from the valid list.

        This is the only public method the game engine uses.
        The game does not need to know how the words were loaded
        or filtered - it only needs a random answer.
        """
        return random.choice(self.words)

# --------------------------------------------------------------------
# WordEngine: Game logic (no UI)
# --------------------------------------------------------------------

class WordEngine:
    """
    This class handles the core Wordle logic.

    Responsibilities:
        - Store the secret answer word
        - Evaluate each guess and return feedback for every letter

    It does NOT know anything about:
        - Tkinter
        - the keyboard
        - the tile grid
        - colors or UI updates

    This separation keeps the game logic clean and testable.
    """

    def __init__(self, answer: str):
        """
        Parameters:
          - answer (str): The secret word chosen for this game.

        The engine stores the answer so it can compare guesses against it.
        """
        self.answer = answer

    def evaluate(self, guess: str):
        """
        Compare the player's guess to answer and return a list of statuses.

        Each letter in the guess receives one of three labels:

           - "correct"
               The letter matches the answer *and* is in the correct position.

           - "misplaced"
                The letter exists somewhere in the answer,
                but NOT in this position.

           - "wrong"
                The letter does not appear anywhere in the answer.

        Example:
            answer = "CRANE"
            guess  = "CARDS"

            result = ["Correct", "misplaced", "wrong", "wrong", "wrong"]

        Returns:
            list[str]: A list of statuses, one for each letter in the guess.
        """
        result = []

        # Compare each letter of the guess to the corresponding letter in the answer.

        # zip(guess, self.answer) pairs letters by position:

        #   ('C', 'C'), ('A', 'R'), ('R', 'A'), ...

        for guess_letter, answer_letter in zip(guess, self.answer):

            # Case 1: Exact match (correct letter, corret position)

            if guess_letter == answer_letter:
                result.append("correct")

            # Case 2: Letter exists in the answer, but in a different position

            elif guess_letter in self.answer:
                result.append("misplaced")

            # Case 3: Letter does not appear in the answer at all

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

    Each tile is a Tkinter Label widget that starts empty and later
    gets filled with letters and colored based on guess evaluation.

    This class ONLY handles the visual board. It does NOT:
       - evaluate guesses
       - choose the answer
       - handle keyboard input
      """

    def __init__(self, root, rows=6, cols=5):
        """
        Parameters:
          - root (tk.TK): The main application window.
          - rows (int): Number of guess rows (default 6).
          - columns (int): Number of letters per row (default 5).

        When created, this class builds the entire 6x5 grid of tiles
        and stores references so the game can update them later.
        """

        self.root = root
        self.rows = rows
        self.cols = cols

        # A 2D list (list of lists) that will store each tile Label.

        # Access pattern:

        #  self.tiles[row_index][column_index]
        self.tiles = []

        # A frame groups the tiles together visually.

        frame = tk.Frame(root)
        frame.pack(pady=20)

        # Create the grid of label widgets.

        for row_index in range(rows):
            row_tiles = []

            for column_index in range(cols):
                # Each tile starts empty and uncolored.

                tile_label = tk.Label(
                    frame,
                    text="",                 # no letter yet

                    width=4,                 # tile width

                    height=2,                # tile height

                    font=("Helvetica", 24),
                    relief="solid",          # gives the tile a border

                    borderwidth=1,
                )
                # Place the tile in the grid layout.

                tile_label.grid(
                    row=row_index,
                    column=column_index,
                    padx=3,
                    pady=3
                )
                # Store the tile so we can update it later.

                row_tiles.append(tile_label)

            # Add the completed row to the tile matrix.

            self.tiles.append(row_tiles)

    # --------------------------------------------------------------------
    # Color a row of tiles after a guess is evaluated
    # --------------------------------------------------------------------

    def color_row(self, row_index, result):
        """
        Color a full row of tiles based on the evaluation result.

        Parameters:
        - row_index (int): Which row to color (0-5)
        - result (list[str]): A list of statuses for each letter:
            "correct", "misplaced", or "wrong"

        This method loops through each tile in the row and updates
        its background color to match Wordle's rules.
        """

        for column_index, status in enumerate(result):
            # Get the tile widget at this row/column

            tile_label = self.tiles[row_index][column_index]

            # Apply the correct Wordle color

            if status == "correct":
                tile_label.config(bg="#6aaa64", fg="white")  # green

            elif status == "misplaced":
                tile_label.config(bg="#c9b458", fg="white")  # yellow

            else:
                tile_label.config(bg="#787c7e", fg="white")  # gray

# --------------------------------------------------------------------
# Keyboard: On-screen Keyboard
# --------------------------------------------------------------------

class Keyboard:
    """
    This class draws the on-screen keyboard used in the Wordle game.

    Responsibilities:
    - Create the keyboard layout (3 rows of buttons)
    - Display letter buttons, Enter, and BACKSPACE
    - Call the appropriate callback functions when buttons are pressed
    - Update key colors after each guess (Wordle-style feedback)

    This class ONLY handels UI. It does NOT contain game logic.
    """

    def __init__(self, root, on_key, on_backspace, on_enter):
        """
        Parameters:
            - root: (tk.Tk) The main application window.
            on_key (function): Called when a letter button is pressed.
            on_backspace (function): Called when the backspace button is pressed.
            on_enter (function): Called when the ENTER button is pressed.

        The keyboard is fully constructed during initialization.
        """

        self.root = root
        self.on_key = on_key  # callback function
        self.on_backspace = on_backspace
        self.on_enter = on_enter

        # Dictionary to store all keyboard buttons by letter.

        # Example: self.buttons["A"] -> the Tkinter Button widget for A

        self.buttons = {}

        # Define the keyboard layout as rows of characters.

        # This matches the real Wordle keyboard.

        layout = [
            list("QWERTYUIOP"),
            list("ASDFGHJKL"),
            ["ENTER"] + list("ZXCVBNM") + ["←"]
        ]

        # Base style for all keys

        self.key_style = {
            "bg": "#3a3a3c",                # dark neutral base

            "fg": "white",                    # readable text

            "font": ("Helvetica", 12, "bold"),
            "relief": "raised",
            "borderwidth": 2,
            "activebackground": "#505053",  # subtle hover

            "activeforeground": "white",
        }
        # A frame to hold the entire keyboard.

        frame = tk.Frame(root)
        frame.pack()

        # Build each row of the keyboard.

        for keyboard_row in layout:
            row_frame = tk.Frame(frame, bg="#121213")
            row_frame.pack(pady=2)

            # Create each button in the row.

            for letter in keyboard_row:

                # Special case: BACKSPACE key

                if letter == "←":
                    button = tk.Button(
                        row_frame,
                        text="←",
                        width=4,
                        command=self.on_backspace,
                        **self.key_style
                    )

                # Special case: ENTER key

                elif letter == "ENTER":
                    button = tk.Button(
                        row_frame,
                        text="ENTER",
                        width=6,
                        command=self.on_enter,
                        **self.key_style
                    )

                # Regular letter keys

                else:
                    # Use selected_letter=letter to capture the current letter
                    # and avoid late-binding issues in lambdas.

                    button = tk.Button(
                        row_frame,
                        text=letter,
                        width=4,
                        command=lambda selected_letter=letter: self.on_key(selected_letter),
                        **self.key_style
                    )

                # Place the button in the row

                button.pack(side="left", padx=3, pady=3)

                # Store the button in the dictionary for later color updates

                self.buttons[letter] = button

    # --------------------------------------------------------------------
    # Update keyboard colors after a guess
    # --------------------------------------------------------------------

    def update_colors(self, result, guess):
        """
        Update the on-screen keyboard colors based on the guess result.

        Parameters:
        - result (list[str]): Status for each letter ("correct", "misplaced", "wrong")
        - guess (str): The actual guessd word (e.g., "CRANE")

        Wordle color priority rules:
        - Green ("correct") is strongest (never overwritten)
        - Yellow ("misplaced") overwrites gray but not green.
        - Gray ("wrong") only applies if the key has no color yet.
        """

        for letter, status in zip(guess, result):

            # Get the button widget for this letter

            button = self.buttons[letter]

            # Check the button's current background color

            current_background = button.cget("bg")

            # Apply color with priority rules

            if status == "correct":
                button.config(bg="#6aaa64", fg="white")  # green

            elif status == "misplaced":
                # Only appy yellow if the key isn't already green

                if current_background not in ("#6aaa64",):
                    button.config(bg="#c9b458", fg="white")  # yellow

            else:  # wrong

                # Only apply gray if the key isn't green or yellow

                if current_background not in ("#6aa64", "#c9b458"):
                    button.config(bg="#787c7e", fg="white")  # gray

# --------------------------------------------------------------------
# WordleGame: Main controller
# --------------------------------------------------------------------

class WordleGame:
    """
    This class ties the entire Wordle application together.

    Responsibilities:
        - load a random answer word
        - create and coordinate all UI components (TileGrid + Keyboard)
        - Track the player's current guess (row, column, text)
        - handle Keyboard input (letters, backspace, enter)
        - Evaluate guesses using WordEngine
        - Update the UI based on evaluation results

    This class acts as the "brain" or controller of the application.
    """

    def __init__(self, root):
        """
        Initialzize the game state, load the answer, and build the UI.
        """
        self.root = root

        # Core configuration

        self.word_length = 5
        self.max_guesses = 6

        # Predeclare attributes so they always exist

        self.answer: str
        self.engine: WordEngine
        self.grid: TileGrid
        self.keyboard: Keyboard

        # ---------------------------------------------------------------
        # Game State
        # ---------------------------------------------------------------

        self.current_row_index = 0
        self.current_column_index = 0
        self.current_guess_text = ""

        # ---------------------------------------------------------------
        # Load a random answer
        # ---------------------------------------------------------------

        selector = WordSelector(
            pathlib.Path(__file__).parent / "wordlist.txt",
            self.word_length,
        )
        self.answer = selector.choose()

        print("DEBUG ANSWER:", self.answer) # Debugging statement

        # Create the game engine that evaluates guesses.

        self.engine = WordEngine(self.answer)

        # ---------------------------------------------------------------
        # Create the UI components
        # ---------------------------------------------------------------

        self.grid = TileGrid(root, self.max_guesses, self.word_length)

        self.keyboard = Keyboard(
            root,
            self.handle_key,        # callback for letter buttons

            self.handle_backspace,  # callback for backspace

            self.handle_enter       # callback for enter
        )

    # --------------------------------------------------------------------
    # Handle letter key press
    # --------------------------------------------------------------------

    def handle_key(self, pressed_letter):
        """
        Called whenever the user clicks a letter button on the keyboard.
        """

        print("Pressed:", pressed_letter)  # Debugging statement to verify key presses

        # If the row is already full, ignore extra letters.

        if self.current_column_index >= self.word_length:
            return

        # Get the tile where the letter should appear.

        tile = self.grid.tiles[self.current_row_index][self.current_column_index]
        tile.config(text=pressed_letter)

        # Add the letter to the current guess string.

        self.current_guess_text += pressed_letter

        # Move to the next tile in the row.

        self.current_column_index += 1

    # --------------------------------------------------------------------
    # Handle backspace
    # --------------------------------------------------------------------

    def handle_backspace(self):
        """
        Called when the user presses the backspace key.
        Removes the last letter typed in the current row.
        """

        print("BACKSPACE pressed")  # Debugging statement to verify backspace presses

        # if at the start of the row, nothing to delete

        if self.current_column_index == 0:
            return

        # Move back one column.

        self.current_column_index -= 1

        # Clear the tile visually.

        tile = self.grid.tiles[self.current_row_index][self.current_column_index]
        tile.config(text="")

        # Remove the last character from the guess text.

        self.current_guess_text = self.current_guess_text[:-1]

    # --------------------------------------------------------------------
    # Handle ENTER key
    # --------------------------------------------------------------------

    def handle_enter(self):
        """
        Called when the user presses ENTER.
        Validates the guess, evaluates it, updates the UI,
        and moves to the next row.
        """

        print("ENTER pressed")  # Debugging statement to verify enter presses

        # Ensure the guess is complete.

        if len(self.current_guess_text) < self.word_length:
            print("Guess not complete")
            return

        # Convert guess to uppercase for consistency.

        guess = self.current_guess_text.upper()
        print("ENTER pressed. Guess submitted:", guess) # Debugging statement to verify the guess text

        # ----------------------------------------------------------------
        # 1. Evaluate the guess using WordEngine
        # ----------------------------------------------------------------

        result = self.engine.evaluate(guess)
        print("Evaluation result:", result)

        # ----------------------------------------------------------------
        # 2. Color the row of tiles
        # ----------------------------------------------------------------

        self.grid.color_row(self.current_row_index, result)

        # ----------------------------------------------------------------
        # 3. Update keyboard colors
        # ----------------------------------------------------------------

        self.keyboard.update_colors(result, guess)

        # ----------------------------------------------------------------
        # 4. Check win/lose conditions
        # ----------------------------------------------------------------

        if guess == self.answer:
            print("You Win!")
            return

        # ----------------------------------------------------------------
        # 5. Move to the next row
        # ----------------------------------------------------------------

        self.current_row_index += 1
        self.current_column_index = 0

        self.current_guess_text = ""

# --------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Wordle - Tkinter by Joe Ruiz")
    game = WordleGame(root)
    root.mainloop()






