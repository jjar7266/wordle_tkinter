import pathlib
import random
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
