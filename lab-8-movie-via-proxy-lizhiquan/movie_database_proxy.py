"""
This module houses the MovieDatabaseProxy class and its supporting
classes to control access to the database.
"""
import enum
import pandas
from movie_database import Movie, MovieDatabase


class UserAccessEnum(enum.Enum):
    """
    Represents different access permissions.
    """
    MEMBER = "member"
    """These users can only view and search the database."""
    ADMIN = "admin"
    """
    These users can view, search, insert, and delete from the database.
    """


class User:
    """
    Represents a user using the system.
    """

    def __init__(self, username: str, password: str,
                 access_type: str):
        """
        Initializes a User.
        :param username: a str
        :param password: a str
        :param access_type: a str
        """
        self.username = username
        self.password = password
        self.access_type = UserAccessEnum(access_type)


class InvalidCredentialsError(Exception):
    """
    Represents an invalid credential error.
    """

    def __init__(self):
        """
        Initializes a InvalidCredentialsError.
        """
        super().__init__("Invalid credentials")


class UnauthorizedError(Exception):
    """
    Represents an unauthorized error.
    """

    def __init__(self):
        """
        Initializes a UnauthorizedError.
        """
        super().__init__("Unauthorized action")


class MovieDatabaseProxy:
    """
    A proxy class of MovieDatabase. This class will control access to
    the database based on:
        - User access level.
        - Implement results caching.

    Attributes:
        - _user: User
        - _cache: dictionary(primary_key: int, movie: Movie)
        - _db: MovieDatabase
    """

    def __init__(self, db_file_name: str, username: str, password: str):
        """
        Initializes a MovieDatabaseProxy.
        :param db_file_name: a str
        :param username: a str
        :param password: a str
        """
        user = self._authenticate_user(username, password)
        if not user:
            raise InvalidCredentialsError()
        self._user = user
        self._cache = {}
        self._db = MovieDatabase(db_file_name)
        self.update_cache()

    def _authenticate_user(self, username: str, password: str) -> User:
        """
        Authenticates a user by confirming that the username and
        password provided are valid based on the data stored in
        `user_accounts.xlsx`.
        :param username: a str
        :param password: a str
        :return: a User if found a matched credentials, None otherwise
        """
        df = pandas.read_excel("user_accounts.xlsx")
        for row in df.iterrows():
            try:
                user = User(**row[1])
            except Exception as e:
                print(e)
            else:
                if user.username == username and user.password == password:
                    return user

    def update_cache(self) -> None:
        """
        Retrieves all the results from the Database and save it in the
        cache.
        :return: None
        """
        for movie in self._db.view():
            self._cache[movie.key] = movie

    def connect(self):
        """
        Establishes a connection to the database and instantiates the
        cursor as well. If the movies table or the file does not exist,
        it creates one.
        """
        self._db.connect()

    def close_connection(self):
        """
        Closes the connection to the database preventing further changes.
        """
        self._db.close_connection()

    def insert(self, movie: Movie) -> Movie:
        """
        Inserts a row into the movies database. Refer to the column
        headings in the class comments to see what the movies database
        is composed of.
        :param movie: a Movie
        :return: A movie object with the key filled in.
        """
        if self._user.access_type != UserAccessEnum.ADMIN:
            raise UnauthorizedError()
        movie = self._db.insert(movie)
        self._cache[movie.key] = movie
        return movie

    def view(self) -> list:
        """
        Retrieves all the rows in the movies table.
        :return: a list of Movies.
        """
        if len(self._cache) == 0:
            self.update_cache()
        return list(self._cache.values())

    def delete(self, movie_id: int):
        """
        Deletes a row specified by the key in the movies table.
        :param movie_id: an int
        """
        if self._user.access_type != UserAccessEnum.ADMIN:
            raise UnauthorizedError()
        self._db.delete(movie_id)
        self._cache.pop(movie_id)

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
        movies = [movie for movie in self._cache.values()
                  if movie.title == title
                  or movie.director == director
                  or movie.language == language
                  or movie.release_year == release_year]

        if len(movies) > 0:
            return movies

        movies = self._db.search(title, director, language, release_year)
        for movie in movies:
            self._cache[movie.key] = movie
        return movies
