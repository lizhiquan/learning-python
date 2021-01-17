"""
This module contains all the classes that are responsible or have
something to do with the creation of LibraryItems. Classes currently
implemented:
    - FactoryMapper
      Client facing class used to retrieve the right factory class
"""

import pandas
from abc import ABC, abstractmethod
from typing import Generator
from items import LibraryItem, Manga, Game, Movie


class LibraryItemFactory(ABC):
    """
    An abstract base class that are responsible for loading and creating
    LibraryItem instances.
    """

    def __init__(self, path: str):
        """
        Initializes a LibraryItemFactory.
        :param path: a str, the path to the file
        """
        self.path = path

    @abstractmethod
    def get_next_item(self) -> Generator[LibraryItem, None, None]:
        """
        An abstract method to override in child classes to read the
        excel file and iterate over each row of the data frame. The
        details from these rows are used to create and yield the
        corresponding Library Item.
        :return: a generator
        """
        pass


class MangaFactory(LibraryItemFactory):
    """
    This class is responsible for loading and creating Manga instances.
    """

    def get_next_item(self) -> Generator[LibraryItem, None, None]:
        """
        Reads the excel file and iterate over each row of the data
        frame. The details from these rows are used to create and yield
        Manga instances.
        :return: a generator
        """
        df = pandas.read_excel(self.path)
        for row in df.iterrows():
            row_no = row[0] + 2
            row_data = row[1]

            if row_data.isnull().any():
                print(f"Missing data at line {row_no}")
                continue

            try:
                manga = Manga(**row_data)
            except (ValueError, TypeError) as e:
                print(f"Invalid data at line {row_no}:", e)
            else:
                yield manga


class GameFactory(LibraryItemFactory):
    """
    This class is responsible for loading and creating Game instances.
    """

    def get_next_item(self) -> Generator[LibraryItem, None, None]:
        """
        Reads the excel file and iterate over each row of the data
        frame. The details from these rows are used to create and yield
        Game instances.
        :return: a generator
        """
        df = pandas.read_excel(self.path)
        for row in df.iterrows():
            row_no = row[0] + 2
            row_data = row[1]

            if row_data.isnull().any():
                print(f"Missing data at line {row_no}")
                continue

            try:
                game = Game(**row_data)
            except ValueError as e:
                print(f"Invalid data at line {row_no}:", e)
            else:
                yield game


class MovieFactory(LibraryItemFactory):
    """
    This class is responsible for loading and creating Movie instances.
    """

    def get_next_item(self) -> Generator[LibraryItem, None, None]:
        """
        Reads the excel file and iterate over each row of the data
        frame. The details from these rows are used to create and yield
        Movie instances.
        :return: a generator
        """
        df = pandas.read_excel(self.path)
        for row in df.iterrows():
            row_no = row[0] + 2
            row_data = row[1]

            if row_data.isnull().any():
                print(f"Missing data at line {row_no}")
                continue

            try:
                movie = Movie(**row_data)
            except ValueError as e:
                print(f"Invalid data at line {row_no}:", e)
            else:
                yield movie


class FactoryMapper:
    """
    FactoryMapper contains the class methods to prompt the user for the
    type of item they wish to acquire and returns a factory that can
    provide the items selected.
    """

    factory_map = {
        1: MangaFactory,
        2: GameFactory,
        3: MovieFactory,
    }
    """
    Factory map is a dictionary of type {int, FactoryClass}
    """

    @classmethod
    def execute_factory_menu(cls) -> LibraryItemFactory:
        """
        Prompts the user to select the type of items they wish to load an
        returns the appropriate factory.
        :return: object of type LibraryItemFactory
        """
        print("Item Loader")
        print("-----------")
        print("What kind of items would you like to load?")
        print("1. Manga")
        print("2. Games")
        print("3. Movies")
        user_choice = int(input("Enter your choice (1-3):"))
        factory = cls.factory_map[user_choice]
        path = input("Enter a path: ")
        return factory(path)


if __name__ == '__main__':
    df = pandas.read_excel("manga_data.xlsx")
    for row in df.iterrows():
        print(row[1])
        for i in row[1]:
            print(i, pandas.notnull(i))
