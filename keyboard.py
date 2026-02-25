import tkinter as tk

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

                if current_background not in ("#6aaa64", "#c9b458"):
                    button.config(bg="#787c7e", fg="white")  # gray
