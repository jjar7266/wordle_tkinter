# --------------------------------------------------------------------
# WordEngine: Core Wordle Logic (No UI)
# --------------------------------------------------------------------
#
# This file contains the *pure logic* for evaluating Wordle guesses.
# It does NOT know anything about Tkinter, tiles, colors, or the keyboard.
#
# The goal is to keep the logic clean, testable, and easy to understand.
# --------------------------------------------------------------------

class WordEngine:
    """
    The WordEngine stores the secret answer and evaluates guesses.

    Responsibilities:
        - Hold the secret answer word
        - Compare a guess to the answer
        - Return feedback for each letter:
              "correct"   → right letter, right position
              "misplaced" → right letter, wrong position
              "wrong"     → letter not in the answer at all

    This class is intentionally UI‑agnostic.
    """

    def __init__(self, answer: str, debug: bool = False):
        """
        Initialize the engine with the chosen answer.

        Parameters:
            answer (str): The secret 5‑letter word for this game.
            debug  (bool): When True, print internal evaluation details.
                           Useful for development and debugging.
        """
        self.answer = answer
        self.debug = debug

    # ----------------------------------------------------------------
    # evaluate()
    # ----------------------------------------------------------------
    # This is the heart of the Wordle logic.
    #
    # IMPORTANT:
    # Wordle requires a *two‑pass algorithm* to correctly handle
    # duplicate letters. A simple "if letter in answer" check is NOT
    # enough and will produce incorrect results (which is the bug you
    # discovered!).
    #
    # PASS 1:
    #   - Mark all GREEN tiles (correct position)
    #   - Count leftover letters in the answer for yellow processing
    #
    # PASS 2:
    #   - Mark YELLOW tiles only if leftover copies exist
    #
    # This perfectly matches real Wordle behavior.
    # ----------------------------------------------------------------
    def evaluate(self, guess: str):
        """
        Evaluate a guess and return a list of statuses.

        Returns:
            list[str]: One of:
                "correct"   → letter matches answer in same position
                "misplaced" → letter exists but in a different position
                "wrong"     → letter not in the answer at all
        """

        # ------------------------------------------------------------
        # Debug output (only prints when debug mode is ON)
        # ------------------------------------------------------------
        if self.debug:
            print("DEBUG → ANSWER:", self.answer)
            print("DEBUG → GUESS :", guess)

        # Start with everything marked as "wrong"
        result = ["wrong"] * len(guess)

        # Dictionary to track leftover letters in the answer
        # after greens are accounted for.
        remaining = {}

        # ------------------------------------------------------------
        # PASS 1: Mark greens and count leftover letters
        # ------------------------------------------------------------
        for i, (g, a) in enumerate(zip(guess, self.answer)):

            if g == a:
                # Exact match → GREEN
                result[i] = "correct"
            else:
                # Count this answer letter as "available" for yellows
                remaining[a] = remaining.get(a, 0) + 1

        # ------------------------------------------------------------
        # PASS 2: Mark yellows using leftover counts
        # ------------------------------------------------------------
        for i, g in enumerate(guess):

            # Skip letters already marked green
            if result[i] == "correct":
                continue

            # If the guessed letter exists in the leftover pool,
            # it is a YELLOW (misplaced) letter.
            if g in remaining and remaining[g] > 0:
                result[i] = "misplaced"
                remaining[g] -= 1  # consume one copy

            # Otherwise it stays "wrong"

        return result

    def toggle_debug(self):
        self.debug = not self.debug
        print(f"DEBUG MODE -> {'ON' if self.debug else 'OFF'}")
