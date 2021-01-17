"""
This module contains the class definition for User and an UserType enum.
"""

from enum import IntEnum


class UserType(IntEnum):
    """
    An enum represents different types of user.
    """
    ANGEL = 1
    TROUBLEMAKER = 2
    REBEL = 3


class User:
    """
    The User class maintains all information of a user, which has a
    name, an age, and a user type.
    """

    def __init__(self, name: str, age: int, user_type: UserType):
        """
        Initializes a User object.
        :param name: a string
        :param age: an int
        :param user_type: a UserType enum
        """
        self.name = name
        self.age = age
        self.user_type = user_type
