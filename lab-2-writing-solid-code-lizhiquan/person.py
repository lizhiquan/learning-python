"""
Contains the Person class which specifies the details of an individual
with cards.
"""

import datetime


class Person:
    """
    Provides a simple representation of a Person. Each person has a name
    and a date of birth.
    """

    def __init__(self, name: str, dob: datetime.datetime):
        """
        Initializes an object of type Person
        :param name: a string
        :param dob: a DateTime object.
        """
        self.name = name
        self.date_of_birth = dob

    def __str__(self):
        return f"Name: {self.name}, Date of Birth: {self.date_of_birth}"
