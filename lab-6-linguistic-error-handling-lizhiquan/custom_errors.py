"""
This module is responsible for housing custom errors.

Classes:
- WordNotFoundError
"""

import difflib


class WordNotFoundError(Exception):
    """
    An error that is raised when the user attempts to query a word that
    does not exist in the dictionary.
    """

    def __init__(self, missing_word: str, dict_keys: list):
        """
        Initializes a WordNotFoundError.
        :param missing_word: a str, the word that does not exist
        :param dict_keys: a list, all the words in the dict
        """
        formatted_msg = f"'{missing_word}' is not found."
        potential_matches = difflib.get_close_matches(missing_word, dict_keys)
        potential_matches = [f"'{word}'" for word in potential_matches]
        if len(potential_matches) > 0:
            formatted_msg += f" Did you mean " \
                             f"{' or '.join(potential_matches)} instead?"
        super().__init__(formatted_msg)
