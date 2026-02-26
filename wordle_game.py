import tkinter as tk
import pathlib

from tile_grid import TileGrid
from keyboard import Keyboard
from word_engine import WordEngine
from word_selector import WordSelector

# --------------------------------------------------------------------
# WordleGame: Main controller (game logic only)
# --------------------------------------------------------------------

class WordleGame:
    """
    The WordleGame class controls all game logic:

        - Load a random answer word
        - Tracks guess state (row, column, text)
        - Handles Keyboard input (letters, backspace, enter)
        - Evaluate guesses using WordEngine
        - Update the TileGrid + Keyboard colors
        - Detects win/lose conditions
        - Triggers restart via GameFrame

    IMPORTANT:
        This class NO LONGER manages layout.
        TileGrid + Keyboard are created by GameFrame.
        WordleGame only receives references to them.
    """

    def __init__(self, parent_frame):
        """
        Initialzize the game state.

        Parameters:
            parent_frame (tk.Frame):
                The GameFrame that owns this controller.
                Used for restart (destroy + recreate GameFrame).
        """
        self.game_frame = parent_frame

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
        # Game Over Flag
        # ---------------------------------------------------------------

        self.game_over = False

        # ---------------------------------------------------------------
        # Load ANSWER LIST (Wordle curated list)
        # ---------------------------------------------------------------

        answer_selector = WordSelector(
            pathlib.Path(__file__).parent / "wordlist.txt",
            self.word_length
        )

        # Store the cleaned list of answer words

        self.answer_words = answer_selector.words

        # Choose a random answer from the curated list

        self.answer = answer_selector.choose()

        print("DEBUG ANSWER:", self.answer) # Debugging statement

        # ---------------------------------------------------------------
        # LOAD VALIDATION LIST (full dictionary)
        # ---------------------------------------------------------------

        validator_selector = WordSelector(
            pathlib.Path(__file__).parent / "words.txt",
            self.word_length
        )

        # Store the validator list as a set for fast lookup

        self.valid_words = set(validator_selector.words)

        # Create the game engine that evaluates guesses.

        self.engine = WordEngine(self.answer)

    # --------------------------------------------------------------------
    # Handle letter Input
    # --------------------------------------------------------------------

    def handle_key(self, pressed_letter: str):
        """
        Called when the user presses a letter on the on-screen keyboard.

        Rules:
            - Ignore input if the game is over.
            - Ignore input if the row is already full.
            - Otherwise, place the letter in the next tile.
        """

        # If the game is over, ignore all input.

        if self.game_over:
            return

        print("Pressed:", pressed_letter)  # Debugging statement to verify key presses

        # If the row is already full, ignore extra letters.

        if self.current_column_index >= self.word_length:
            return

        # Add letter to guess text

        self.current_guess_text += pressed_letter

        # Update tile visually

        tile = self.grid.tiles[self.current_row_index][self.current_column_index]
        tile.config(text=pressed_letter)

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

        # If the game is over, ignore all input.

        if self.game_over:
            return

        print("BACKSPACE pressed")  # Debugging statement to verify backspace presses

        # if at the start of the row, nothing to delete

        if self.current_column_index == 0:
            return

        # Move back one column.

        self.current_column_index -= 1

        # Remove last letter from guess text

        self.current_guess_text = self.current_guess_text[:-1]

        # Clear the tile visually

        tile = self.grid.tiles[self.current_row_index][self.current_column_index]
        tile.config(text="")

    # --------------------------------------------------------------------
    # Handle ENTER key
    # --------------------------------------------------------------------

    def handle_enter(self):
        """
        Called when the user presses ENTER.

        Rules:
            - Ignore if game is over.
            - Ignore if row is not full.
            - Validate guess is a real word.
            - Evaluate guess using WordEngine.
            - Color tiles + update Keyboard.
            - Check win/lose.
            - Move to next row if game continues.
        """

        # If the game is over, ignore all input.

        if self.game_over:
            return

        print("ENTER pressed")  # Debugging statement to verify enter presses

        print("BUFFER: ", repr(self.current_guess_text))  # Debugging statement

        # Must have exactly 5 letters

        if len(self.current_guess_text) != self.word_length:

            # UI message
            self.game_frame.show_message("Not enough letters")

            return

        # Convert guess to uppercase for consistency.

        guess = self.current_guess_text.upper()

        # ---------------------------------------------------------------
        # Validate that the guess is a real word
        # ---------------------------------------------------------------

        if guess not in self.valid_words:

            # UI message
            self.game_frame.show_message("Not in word list")

            return

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
            self.end_game(win=True)
            return

        # ----------------------------------------------------------------
        # 5. Move to the next row
        # ----------------------------------------------------------------

        self.current_row_index += 1
        self.current_column_index = 0

        self.current_guess_text = ""

        # --------------------------------------------------------------
        # LOSS CHECK
        # --------------------------------------------------------------

        if self.current_row_index >= self.max_guesses:
            self.end_game(win=False)
            return

    # --------------------------------------------------------------
    # End Game Handler
    # --------------------------------------------------------------

    def end_game(self, win: bool):
        """
        Called when the player wins or loses.

        Responsibilities:
            - Set game_over flag
            - Show a popup message
            - Display the correct answer if lost
            - Provide a Play Again button
        """

        self.game_over = True

        # Create a popup window

        popup = tk.Toplevel(self.game_frame.master)
        popup.title("Game Over")
        popup.config(bg="#121213")

        # -----------------------------------------------------------
        # Center the popup relative to the main window
        # -----------------------------------------------------------

        popup.geometry("+400+200")

        # -----------------------------------------------------------
        # Win or lose message
        # -----------------------------------------------------------

        if win:
            message = "You Win!"
        else:
            message = f"You Lose!\nThe word was: {self.answer}"

        label = tk.Label(
            popup,
            text=message,
            font=("Helvetica", 18, "bold"),
            fg="white",
            bg="#121213",
            pady=20
        )
        label.pack()

        # -----------------------------------------------------------------
        # Play Again button
        # ----------------------------------------------------------------

        play_again_button = tk.Button(
            popup,
            text="Play Again",
            font=("Helvetica", 14, "bold"),
            bg="#538d4e",
            fg="white",
            padx=20,
            pady=10,
            command=lambda: self.restart_game(popup)
        )
        play_again_button.pack(pady=10)

    # -----------------------------------------------------------------
    # Restart Game Handler
    # -----------------------------------------------------------------

    def restart_game(self, popup: tk.Toplevel):
        """
        Destroy the popup and rebuild the entire UI by destroying
        and recreating the GameFrame.
        """

        popup.destroy()

        # Destroy the entire GameFrame (grid + keyboard + controller)

        self.game_frame.destroy()

        # Import here to avoid circular import

        from game_frame import GameFrame

        root = self.game_frame.master
        GameFrame(root)

