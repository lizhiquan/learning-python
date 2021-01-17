"""
This module houses all the classes the represent celestial bodies:
- Asteroid: contains radius, position, velocity and created date.
"""

from __future__ import annotations
from datetime import datetime
from random import randint
from vectors import Vector


class Asteroid:
    """
    This class represents an asteroid, which has a radius, its current
    position and velocity, and a created timestamp.
    """

    _next_id = 1
    """The unique ID will be given to the next created object."""

    def __init__(self, radius: int, position: Vector, velocity: Vector,
                 dob_timestamp: datetime, min_bound: float = None,
                 max_bound: float = None):
        """
        Initializes a Asteroid object with radius, position, velocity,
        created date, and assigns a unique ID to it. It also has an
        optional min bound and an optional max bound, which are used to
        determine if this asteroid can move based on its position.
        :param radius: an int, representing the radius
        :param position: a Vector, representing the position
        :param velocity: a Vector, representing the velocity
        :param dob_timestamp: a datetime, representing the created date
        :param min_bound: a float, the min value of the bound in each
                          direction
        :param max_bound: a float, the max value of the bound in each
                          direction
        """
        self.id = Asteroid._generate_unique_id()
        self.radius = radius
        self.position = position
        self.velocity = velocity
        self.dob_timestamp = dob_timestamp
        self.min_bound = min_bound
        self.max_bound = max_bound

    def move(self) -> None:
        """
        Compares with the min and max bound values to determine if this
        asteroid can move without exceeding the bound. If the condition
        is satisfied, updates its current position by adding the
        velocity.
        :return: None
        """
        new_position = self.position + self.velocity

        if self.min_bound:
            if (new_position.x < self.min_bound or
                    new_position.y < self.min_bound or
                    new_position.z < self.min_bound):
                return

        if self.max_bound:
            if (new_position.x > self.max_bound or
                    new_position.y > self.max_bound or
                    new_position.z > self.max_bound):
                return

        self.position = new_position

    @classmethod
    def _generate_unique_id(cls) -> int:
        """
        Returns an unique ID for the current Asteroid object. This ID is
        generated using a class variable that is used to keep track of
        what the next ID should be.
        :return: an int representing a sequential unique ID.
        """
        uid = cls._next_id
        cls._next_id += 1
        return uid

    def __str__(self):
        return f'Asteroid {self.id} ' \
               f'(radius: {self.radius}, ' \
               f'position: {self.position}, ' \
               f'velocity: {self.velocity}, ' \
               f'dob_timestamp: {self.dob_timestamp})'

    @classmethod
    def generate_random_asteroid(cls) -> Asteroid:
        """
        Generates a random asteroid object with a radius in [1, 4],
        velocity in [-5, 5] and a position in [0, 100].
        :return: an Asteroid with random radius, velocity and position
        """
        radius = randint(1, 4)
        velocity = Vector.generate_random_vector(-5, 5)
        min_bound, max_bound = (0, 100)
        position = Vector.generate_random_vector(min_bound, max_bound)
        return cls(radius, position, velocity, datetime.now(), min_bound,
                   max_bound)
