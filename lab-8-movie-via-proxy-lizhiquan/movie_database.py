"""
This module houses the code to perform sql queries on a database.
"""
import sqlite3


class Movie:

    def __init__(self, title: str, director: str, release_year: int,
                 language: str, key: int = None):
        """
        A movie object identified by it's key and/or it's title/director
        pair. Made primarily for use with a database.
        :param key: an int (unique) (optional, not required if the movie
                    does not exist in the database yet. Determined by
                    the database upon insertion).
        :param title: a string (unique when paired with a director)
        :param director: a string (unique when paired with title)
        :param release_year: an int (4 digits)
        :param language: a string
        """
        self.key = key
        self.title = title
        self.director = director
        self.language = language
        self.release_year = release_year

    def __str__(self):
        return f"Key: {self.key}, Title: {self.title},\n" \
               f"Director: {self.director},\n" \
               f"Release Year: {self.release_year},\n" \
               f"Language: {self.language}"


class MovieDatabase:
    """
    The MovieDatabase class allows users to connect and create a movies
    database while performing simple data manipulation tasks.
    The columns that make up each row are:

    1. PRIMARY KEY (integer, key)
    2. TITLE (text)
    3. DIRECTOR (text)
    4. LANGUAGE (text)
    5. RELEASE_YEAR (integer)

    All changes are committed immediately.
    """

    def __init__(self, db_file_name: str, movies: list = None):
        """
        Initializes the database object and establishes a connection to it.
        A new database is created if one does not exist already at the path
        specified. Optionally, the program will attempt to insert some
        movies after connecting with a database if a list of movies is
        provided.
        :param db_file_name: a string, path to the database file ending in
                            extension .db.
        :param movies: a List containing objects of type Movie.
        """
        self.name = db_file_name
        self.db_connection = None
        self.cursor = None
        self.connect()

        if movies:
            for movie in movies:
                self.insert(movie)

    def connect(self):
        """
        Establishes a connection to the database and instantiates the
        cursor as well. If the movies table or the file does not exist,
        it creates one.
        """
        self.db_connection = sqlite3.connect(self.name)
        self.cursor = self.db_connection.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY, "
            "title text, director text, language text, release_year integer)"
        )
        self.db_connection.commit()

    def close_connection(self):
        """
        Closes the connection to the database preventing further changes.
        """
        self.db_connection.close()

    def insert(self, movie: Movie) -> Movie:
        """
        Inserts a row into the movies database. Refer to the column
        headings in the class comments to see what the movies database
        is composed of.
        :param title: a string
        :param director: a string
        :param language: a string, ISO language code
        :param release_year: an int
        :return: A movie object with the key filled in.
        """
        self.cursor.execute("INSERT INTO movies VALUES (NULL,?,?,?,?)",
                            (movie.title, movie.director, movie.language,
                             movie.release_year))
        self.db_connection.commit()
        return self.search(movie.title, movie.director, movie.language,
                           movie.release_year)[0]

    def view(self) -> list:
        """
        Retrieves all the rows in the movies table.
        :return: a list of Movies.
        """
        self.cursor.execute("SELECT * FROM movies")
        rows = self.cursor.fetchall()
        movie_list = []
        for row in rows:
            movie = Movie(key=row[0], title=row[1], director=row[2],
                          language=row[3], release_year=row[4])
            movie_list.append(movie)
        return movie_list

    def delete(self, movie_id):
        """
        Deletes a row specified by the key in the movies table.
        :param movie_id: an int
        """
        self.cursor.execute("DELETE FROM movies WHERE id=?", (movie_id,))
        self.db_connection.commit()

    def search(self, title="", director="", language="", release_year=""):
        """
        Retrieves the rows that match any combination of the given
        parameters.
        :param title: a string
        :param director: a string
        :param language: a string, ISO language code
        :param release_year: an int
        :return: a list of rows
        """
        self.cursor.execute(
            "SELECT * FROM movies WHERE title=? OR director=? "
            "OR language=? OR release_year=?",
            (title, director, language, release_year))
        rows = self.cursor.fetchall()
        movie_list = []
        for row in rows:
            movie = Movie(key=row[0], title=row[1], director=row[2],
                          language=row[3], release_year=row[4])
            movie_list.append(movie)
        return movie_list
