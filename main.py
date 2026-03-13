import tkinter as tk
from game_frame import GameFrame

"""
Wordle Clone - Tkinter OOP Version

Written by Jose "Joe" Ruiz

This file sets up the basic structure of the project.
"""

# Tkinter is the built-in GUI library for Python.
# It lets us create windows, buttons, labels, and handle events.

# --------------------------------------------------------------------
# TODO LIST — Updated After Debug System Completion
# --------------------------------------------------------------------

# GAME OVER FLOW
# ✓ Add game_over flag to block input after win/lose
# ✓ Create Game Over popup (win/lose message, correct word)
# ✓ Add Play Again button
# - Add Quit button (optional)
# ✓ Disable keyboard input when game ends
# ✓ Detect loss after 6 guesses

# RESTART LOGIC
# ✓ Implement restart_game() to reset:
#       - grid tiles (via full GameFrame rebuild)
#       - keyboard colors
#       - row/column indices
#       - current_guess_text
#       - game_over flag
#       - answer + engine
# ✓ Fix circular import by using local import inside restart_game()
# ✓ Ensure Play Again rebuilds the entire UI cleanly

# DEBUG SYSTEM
# ✓ Add global AppSettings.debug_mode flag
# ✓ Initialize GameFrame.debug_mode from AppSettings
# ✓ Pass debug flag into WordEngine on creation
# ✓ Ensure engine inherits debug state after Play Again
# ✓ Bind CTRL+D to toggle debug mode
# ✓ Print answer immediately when debug is turned ON

# UI POLISH
# - Decide on dark/light theme for TileGrid
# - Add tile flip animation (optional)
# - Add bounce animation on correct guess (optional)
# - Improve popup styling (centered, padding, spacing)

# CODE QUALITY
# ✓ Add initialization block for all attributes
# - Add docstrings to new methods
# - Add helper to reset keyboard colors (if needed)
# - Consider extracting constants (colors, sizes) into a config module

# TESTING
# ✓ Test win flow
# ✓ Test loss flow
# ✓ Test restart flow
# - Test keyboard disabling thoroughly
# - Test repeated letters and edge cases
# - Test invalid words and error feedback

# FUTURE FEATURES (Optional)
# - Hard mode
# - Stats screen (games played, win streak, distribution)
# - Daily mode
# - Sound effects
# - Settings menu
# --------------------------------------------------------------------


# --------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------

if __name__ == "__main__":
    # Create the main application window
    root = tk.Tk()
    root.title("Wordle - Tkinter by Joe Ruiz")

    # Create the GameFrame (the entire UI lives inside this frame)
    GameFrame(root)

    root.mainloop()
