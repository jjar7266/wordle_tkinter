import tkinter as tk

from tile_grid import TileGrid
from keyboard import Keyboard
from wordle_game import WordleGame

# -----------------------------------------------------------------
# GameFrame: Parent container for the entire Wordle UI
# -----------------------------------------------------------------

class GameFrame(tk.Frame):
    """
    GameFrame is the top-level UI container for the Wordle game.

    This class solves the layout + restart issues by grouping the
    entire game (TileGrid + Keyboard + WordleGame controller)
    inside a single Frame Widget.

    Why this matters:
        - TileGrid and Keyboard used to pack directly into root.
        - Restarting the game only reset widgets, not layout.
        - Tkinter does NOT re-pack widgets on reset.
        - Result: layout collapsed after Play Again

    With GameFrame:
        - The entire UI lives inside this frame.
        - Restarting the game simply destroys this frame
          and creates a new one.
        - Layout is always rebuilt cleanly.
    """

    def __init__(self, root):
        """
        Create a new GameFrame and build the full UI inside it.

        Parameters:
            root (tk.Tk): The main application window.
        """
        super().__init__(root)

        # Pack this frame into the root window.

        # All UI components will be children of this frame.

        self.pack(pady=20)

        # -----------------------------------------------------------------
        # 1. Create the TileGrid (6 rows x 5 columns)
        # -----------------------------------------------------------------

        # IMPORTANT:

        # TileGrid now attaches to THIS frame, not root.

        self.grid_widget = TileGrid(self, rows=6, cols=5)

        # -----------------------------------------------------------------
        # 2. Create the WordleGame controller
        # -----------------------------------------------------------------

        # The controller handles:

        #   - input

        #   - evaluation

        #   - game state

        #   - win/lose logic

        #

        # It needs references to:

        #   - the TileGrid

        #   - the Keyboard

        #   - this GameFrame (for restart)

        #

        # So we create the controller AFTER the grid but BEFORE Keyboard.

        self.controller = WordleGame(self)

        # ----------------------------------------------------------------
        # 3. Create the on-screen Keyboard
        # ----------------------------------------------------------------

        # IMPORTANT:

        # Keyboard now attaches to THIS frame, not root.

        self.keyboard_widget = Keyboard(
            self,
            self.controller.handle_key,
            self.controller.handle_backspace,
            self.controller.handle_enter
        )

        # Give the controller access to the keyboard widget

        self.controller.keyboard = self.keyboard_widget

        # Give the controller access to the grid widget

        self.controller.grid = self.grid_widget

        # Give the controller access to THIS GameFrame

        self.controller.game_frame = self

