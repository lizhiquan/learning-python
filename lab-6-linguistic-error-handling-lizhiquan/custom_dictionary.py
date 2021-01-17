"""
This module is responsible for housing the CustomDictionary class.
"""

from custom_errors import WordNotFoundError


class CustomDictionary:
    """
    This class represents a custom dictionary that manages a list of
    words and their definitions. It also keeps track of the history of
    queried words.
    """

    def __init__(self, path: str):
        """
        Initializes a CustomDictionary.
        :param path: a str, the path to the dictionary data file
        """
        self.file_manager = DictionaryFileManager()
        self.definitions = self.file_manager.load_dictionary(path)
        self.words_queried = set()

    def query(self, word: str) -> list:
        """
        Returns the definitions associated with that word as a list.
        Raises `WordNotFoundError` if the word is not found.
        :param word: a str, the word to look up
        :return: a list, definitions of the given word
        """
        try:
            definition = self.definitions[word]
        except Exception:
            raise WordNotFoundError(word, list(self.definitions.keys()))
        else:
            self.words_queried.add(word)
            return definition

    def exported_queried_words(self, path: str) -> None:
        """
        Exports all the queried words and their definitions to a text
        file as per the path specified.
        :param path: a str
        :return: None
        """
        self.file_manager.export_words(path, list(self.words_queried),
                                       self.definitions)

    def add_word(self, word: str, list_definitions: list) -> None:
        """
        Adds a new word and its definitions to the definitions
        dictionary attribute. Raises `TypeError` if `list_definitions`
        is not of type list, `ValueError` if the new word already
        existed in the dictionary.
        :param word: a str
        :param list_definitions: a list
        :return: None
        """
        if not isinstance(list_definitions, list):
            raise TypeError('list_definitions must be type list')
        if not word:
            raise ValueError('Invalid word')
        if word in self.definitions:
            raise ValueError(f"'{word}' already existed in the dictionary")
        if len(list_definitions) == 0:
            raise ValueError('You must have at least 1 definition for this '
                             'word')
        self.definitions[word] = list_definitions

    def export_dictionary(self, path: str) -> None:
        """
        Exports all the words and their associated definitions in the
        definitions attribute to a text file at the provided path.
        :param path: a str
        :return: None
        """
        self.file_manager.export_words(path, list(self.definitions.keys()),
                                       self.definitions)


class DictionaryFileManager:
    """
    This class is responsible for reading and writing to dictionary text
    files.
    """

    def load_dictionary(self, path: str) -> dict:
        """
        Loads dictionary from a file path, constructs and returns a dict
        object with key is the word and value is a list of definitions
        it has.
        :param path: a str, the path to the dictionary data file
        :return: a dict, key is the word and value is a list of
                 definitions it has
        """
        with open(path, mode='r') as file:
            data = file.read()
            blocks = data.split('--')[1:]
            word_definitions = [list(filter(None, block.split('\n')))
                                for block in blocks]
            return {item[0]: item[1:] for item in word_definitions}

    def export_words(self, path: str, words: list, definitions: dict) -> None:
        """
        Exports all the given words and their associated definitions to
        a text file at the provided path.
        :param words: a list
        :param path: a str
        :param definitions: a dict
        :return: None
        """
        with open(path, mode='w') as file:
            for word in words:
                file.write(f'--{word}\n')
                for definition in definitions[word]:
                    file.write(f'{definition}\n')
