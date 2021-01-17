from enum import IntEnum


class UserType(IntEnum):
    ANGEL = 1
    TROUBLEMAKER = 2
    REBEL = 3


class User:
    def __init__(self, name: str, age: int, user_type: UserType):
        self.name = name
        self.age = age
        self.user_type = user_type
