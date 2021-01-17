"""
This module houses the Driver class that drives the program.
"""
from movie_database_proxy import MovieDatabaseProxy
from movie_database import Movie


class Driver:
    """
    The main class that drives the program.
    """

    def __init__(self):
        """
        Initializes a Driver.
        """
        self.db = self.instantiate_database()
        self.menu_prompt = {
            # menu option: (method, StringRepresentation)
            1: (self.add_movie, "Add movie"),
            2: (self.remove_movie, "Remove movie"),
            3: (self.search_movie, "Search movie"),
            4: (self.view_all_movies, "View all movies"),
            5: (quit, "Exit")
        }

    def instantiate_database(self) -> MovieDatabaseProxy:
        """
        Prompts for username, password, and db file name and creates
        a MovieDatabaseProxy that authenticates the user.
        :return: a MovieDatabaseProxy
        """
        username = input("Enter username: ")
        password = input("Enter password: ")
        db_file_name = input("Enter database file name: ")
        try:
            db = MovieDatabaseProxy(db_file_name, username, password)
        except Exception as e:
            print(e)
            return self.instantiate_database()
        else:
            return db

    def show_main_menu(self) -> None:
        """
        Prints a menu to the console and handles user input.
        :return: None
        """
        user_choice = -1
        while user_choice != 5:
            for key, value in self.menu_prompt.items():
                print(f"{key}: {value[1]}")
            try:
                user_choice = int(input("Enter your choice: "))
                choice = self.menu_prompt[user_choice][0]
            except KeyError:
                print("Option doesn't exist")
            except ValueError:
                print("Invalid entry")
            else:
                choice()
            finally:
                print()

    def add_movie(self) -> None:
        """
        Prompts and adds a movie to the database.
        :return: None
        """
        try:
            title = input("Enter a title: ")
            director = input("Enter a director: ")
            release_year = int(input("Enter a release year: "))
            language = input("Enter a language: ")
            movie = Movie(title, director, release_year, language)
            self.db.insert(movie)
        except Exception as e:
            print(f"Failed to add movie: {e}")
        else:
            print("Movie added")

    def remove_movie(self) -> None:
        """
        Prompts and removes a movie in the database.
        :return: None
        """
        try:
            movie_id = int(input("Enter a movie id: "))
            self.db.delete(movie_id)
        except Exception as e:
            print(f"Failed to remove movie: {e}")
        else:
            print("Movie deleted")

    def search_movie(self) -> None:
        """
        Prompts and searches a movie in the database.
        :return: None
        """
        try:
            title = input("Enter a title: ")
            director = input("Enter a director: ")
            release_year = input("Enter a release year: ")
            if release_year != '':
                release_year = int(release_year)
            language = input("Enter a language: ")
            movies = self.db.search(title, director, language, release_year)
        except Exception as e:
            print(e)
        else:
            if len(movies) == 0:
                print("Movie not found")
            else:
                for movie in movies:
                    print("-----")
                    print(movie)

    def view_all_movies(self) -> None:
        """
        Shows a list of all movies.
        :return: None
        """
        movies = self.db.view()
        if len(movies) == 0:
            print("There is no movie in the database yet")
        else:
            for movie in movies:
                print("-----")
                print(movie)


if __name__ == '__main__':
    driver = Driver()
    driver.show_main_menu()
