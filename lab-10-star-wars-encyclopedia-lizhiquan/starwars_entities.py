"""
This module holds classes that represent star wars entities.
"""


class Starship:
    """
    Represents a starship.
    """

    def __init__(self, name: str, model: str, starship_class: str,
                 manufacturer: str, cost_in_credits: str, crew: str, **kwargs):
        """
        Initializes a Starship.
        :param name: a str
        :param model: a str
        :param starship_class: a str
        :param manufacturer: a str
        :param cost_in_credits: a str
        :param crew: a str
        :param kwargs: unused args
        """
        self.name = name
        self.model = model
        self.starship_class = starship_class
        self.manufacturer = manufacturer
        self.cost_in_credits = cost_in_credits
        self.crew = crew

    def __str__(self):
        return f'---\n' \
               f'Starship: {self.name}\n' \
               f'Model: {self.model}\n' \
               f'Starship class: {self.starship_class}\n' \
               f'Manufacturer: {self.manufacturer}\n' \
               f'Cost in credits: {self.cost_in_credits}\n' \
               f'Number of crew: {self.crew}\n' \
               f'---'


class Planet:
    """
    Represents a planet.
    """

    def __init__(self, name: str, diameter: str, rotation_period: str,
                 orbital_period: str, gravity: str, population: str, **kwargs):
        """
        Initializes a Planet.
        :param name: a str
        :param diameter: a str
        :param rotation_period: a str
        :param orbital_period: a str
        :param gravity: a str
        :param population: a str
        :param kwargs: unused args
        """
        self.name = name
        self.diameter = diameter
        self.rotation_period = rotation_period
        self.orbital_period = orbital_period
        self.gravity = gravity
        self.population = population

    def __str__(self):
        return f'---\n' \
               f'Planet: {self.name}\n' \
               f'Diameter: {self.diameter}\n' \
               f'Rotation period: {self.rotation_period}\n' \
               f'Orbital period: {self.orbital_period}\n' \
               f'Gravity: {self.gravity}\n' \
               f'Population: {self.population}\n' \
               f'---'
