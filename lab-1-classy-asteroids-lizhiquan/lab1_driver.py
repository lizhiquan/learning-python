"""
This module houses the controller class, which drives the simulations of
our celestial bodies in a 3D space.
"""

from time import sleep
from celestial_bodies import Asteroid


class Controller:
    """
    The driver class which drives the simulation.
    """

    def __init__(self):
        """
        Initializes the controller by generating 100 random asteroids.
        """
        self.asteroids = []
        for _ in range(100):
            self.asteroids.append(Asteroid.generate_random_asteroid())

    def simulate(self, seconds: int) -> None:
        """
        Simulates asteroids moving in a 3D space in a number of seconds.
        :param seconds: an int, number of seconds to run the simulation
        :return: None
        """
        for _ in range(seconds):
            for asteroid in self.asteroids:
                asteroid.move()
                print(asteroid)
            sleep(1)


def main():
    """
    Instantiates and executes the controller.
    """
    controller = Controller()
    controller.simulate(3)


if __name__ == '__main__':
    main()
