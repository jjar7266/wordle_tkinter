import tkinter as tk
import pathlib

from tile_grid import TileGrid
from keyboard import Keyboard
from word_engine import WordEngine
from word_selector import WordSelector

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

