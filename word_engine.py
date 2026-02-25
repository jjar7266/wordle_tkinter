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
