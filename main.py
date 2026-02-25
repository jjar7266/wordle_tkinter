import tkinter as tk
from wordle_game import WordleGame

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


# --------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Wordle - Tkinter by Joe Ruiz")
    game = WordleGame(root)
    root.mainloop()



