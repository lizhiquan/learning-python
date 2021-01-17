"""
The entry point into the program.
This module is responsible for housing the DictionaryMenu class and
handling user input.
"""

from custom_dictionary import CustomDictionary
from custom_errors import WordNotFoundError


class DictionaryMenu:
    """
    Drives the dictionary program and is responsible for handling user
    inputs.
    """

    def __init__(self, dictionary: CustomDictionary):
        """
        Initializes a DictionaryMenu.
        :param dictionary: a CustomDictionary
        """
        self.custom_dictionary = dictionary
        self.prompt_menu = {
            # menu option: (method, StringRepresentation)
            1: (self.query, "Query Definition"),
            2: (self.export_queried, "Export Queried Words"),
            3: (self.append_to_dictionary, "Append to Dictionary"),
            4: (self.view_entries, "View all Entries"),
            5: (self.export_dictionary, "Export Dictionary"),
            6: (quit, "Exit")
        }

    def prompt(self):
        user_choice = 1
        while user_choice in self.prompt_menu:
            for key, value in self.prompt_menu.items():
                print(f"{key}: {value[1]}")

            try:
                user_choice = int(input("Enter your choice: "))
            except ValueError:
                print('Invalid choice')
                user_choice = 1
                continue

            try:
                method = self.prompt_menu[user_choice][0]
            except KeyError:
                print('Invalid choice')
                user_choice = 1
            else:
                method()

            print()

    def query(self) -> None:
        """
        Prompts the user for a word and prints out the query result.
        :return: None
        """
        word = input('Enter a word to query: ')
        try:
            definitions = self.custom_dictionary.query(word)
        except WordNotFoundError as e:
            print(e)
        else:
            for definition in definitions:
                print(f'- {definition}')

    def export_queried(self) -> None:
        """
        Prompts the user for a path and exports queried words.
        :return: None
        """
        path = input('Enter a path to export: ')
        try:
            self.custom_dictionary.exported_queried_words(path)
        except FileNotFoundError:
            print('Failed to export')
        else:
            print('The queried words were exported successfully!')

    def append_to_dictionary(self) -> None:
        """
        Appends a word and associated definition(s) to the dictionary.
        :return: None
        """
        word = input('Enter a word to add: ')
        definitions = []
        definition = '-'
        while definition != '':
            definition = input('Enter a definition (Leave it empty to finish'
                               ' adding): ').strip()
            if definition != '':
                definitions.append(definition)

        try:
            self.custom_dictionary.add_word(word, definitions)
        except ValueError as e:
            print(e)
        else:
            print(f"'{word}' was added successfully!")
            for definition in definitions:
                print(f'- {definition}')

    def view_entries(self) -> None:
        """
        Views all entries in the dictionary.
        :return: None
        """
        for word, definitions in self.custom_dictionary.definitions.items():
            print(word.capitalize())
            print('-' * len(word))
            for definition in definitions:
                print(f'- {definition}')
            print()

    def export_dictionary(self):
        """
        Prompts the user for a path and exports the entire dictionary.
        :return: None
        """
        path = input('Enter a path to export: ')
        try:
            self.custom_dictionary.export_dictionary(path)
        except FileNotFoundError:
            print('Failed to export')
        else:
            print('The dictionary was exported successfully!')


if __name__ == '__main__':
    is_loaded = False
    while not is_loaded:
        path = input('Enter a path to the dictionary file to load: ')
        try:
            dictionary = CustomDictionary(path)
        except FileNotFoundError:
            print('File not found')
        else:
            is_loaded = True
            menu = DictionaryMenu(dictionary)
            menu.prompt()
