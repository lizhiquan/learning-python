"""
Contains the Factory Classes related to the Item class.
"""
from abc import ABC, abstractmethod
from items import Toy, StuffedAnimal, Candy
from items import SantaWorkshop, CandyCanes, Reindeer
from items import RCSpider, PumpkinCaramelToffee, DancingSkeleton
from items import RobotBunny, CremeEggs, EasterBunny


class ItemFactory(ABC):
    """
    An abstract base class that is responsible for creating Item
    instances.
    """

    @abstractmethod
    def create_toy(self, product_details: dict) -> Toy:
        """
        An abstract method to create a Toy.
        :param product_details: a dictionary/pandas series of details
        :return: a Toy
        """
        pass

    @abstractmethod
    def create_stuffed_animal(self, product_details: dict) -> StuffedAnimal:
        """
        An abstract method to create a StuffedAnimal.
        :param product_details: a dictionary/pandas series of details
        :return: a StuffedAnimal
        """
        pass

    @abstractmethod
    def create_candy(self, product_details: dict) -> Candy:
        """
        An abstract method to create a Candy.
        :param product_details: a dictionary/pandas series of details
        :return: a Candy
        """
        pass


class ChristmasFactory(ItemFactory):
    """
    This class is responsible for creating Christmas Item instances.
    """

    def create_toy(self, product_details: dict) -> Toy:
        """
        Creates a SantaWorkshop Toy.
        :param product_details: a dictionary/pandas series of details
        :return: a Toy
        """
        return SantaWorkshop(**product_details)

    def create_candy(self, product_details: dict) -> Candy:
        """
        Creates a CandyCanes Candy.
        :param product_details: a dictionary/pandas series of details
        :return: a Candy
        """
        return CandyCanes(**product_details)

    def create_stuffed_animal(self, product_details: dict) -> StuffedAnimal:
        """
        Creates a Reindeer StuffedAnimal.
        :param product_details: a dictionary/pandas series of details
        :return: a StuffedAnimal
        """
        return Reindeer(**product_details)


class HalloweenFactory(ItemFactory):
    """
    This class is responsible for creating Halloween Item instances.
    """

    def create_toy(self, product_details: dict) -> Toy:
        """
        Creates a RCSpider Toy.
        :param product_details: a dictionary/pandas series of details
        :return: a Toy
        """
        return RCSpider(**product_details)

    def create_candy(self, product_details: dict) -> Candy:
        """
        Creates a PumpkinCaramelToffee Candy.
        :param product_details: a dictionary/pandas series of details
        :return: a Candy
        """
        return PumpkinCaramelToffee(**product_details)

    def create_stuffed_animal(self, product_details: dict) -> StuffedAnimal:
        """
        Creates a DancingSkeleton StuffedAnimal.
        :param product_details: a dictionary/pandas series of details
        :return: a StuffedAnimal
        """
        return DancingSkeleton(**product_details)


class EasterFactory(ItemFactory):
    """
    This class is responsible for creating Easter Item instances.
    """

    def create_toy(self, product_details: dict) -> Toy:
        """
        Creates a RobotBunny Toy.
        :param product_details: a dictionary/pandas series of details
        :return: a Toy
        """
        return RobotBunny(**product_details)

    def create_candy(self, product_details: dict) -> Candy:
        """
        Creates a CremeEggs Candy.
        :param product_details: a dictionary/pandas series of details
        :return: a Candy
        """
        return CremeEggs(**product_details)

    def create_stuffed_animal(self, product_details: dict) -> StuffedAnimal:
        """
        Creates a EasterBunny StuffedAnimal.
        :param product_details: a dictionary/pandas series of details
        :return: a StuffedAnimal
        """
        return EasterBunny(**product_details)
