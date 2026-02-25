import tkinter as tk

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
