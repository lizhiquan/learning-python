"""
Contains the item class and its related subclasses.
"""

from abc import ABC
from enum import Enum
import re


class ItemType(Enum):
    """
    The type of the item.
    """
    TOY = "Toy"
    STUFFED_ANIMAL = "StuffedAnimal"
    CANDY = "Candy"


class Item(ABC):
    """
    An interface for an item.
    """

    def __init__(self, product_id: str, name: str, description: str, **kwargs):
        """
        Initializes an Item.
        :param product_id: a str
        :param name: a str
        :param description: a str
        """
        if not isinstance(product_id, str):
            raise TypeError('product_id must be a str')
        if len(product_id) == 0:
            raise ValueError(f'product_id must not be empty')
        if not isinstance(name, str):
            raise TypeError('name must be a str')
        if len(name) == 0:
            raise ValueError(f'name must not be empty')
        if not isinstance(description, str):
            raise TypeError('description must be a str')
        if len(description) == 0:
            raise ValueError(f'description must not be empty')
        self.product_id = product_id
        self.name = name
        self.description = description


class BooleanType(Enum):
    """
    Represents a boolean type from a string.
    """
    TRUE = "Y"
    FALSE = "N"


class Toy(Item, ABC):
    """
    Represents a Toy Item.
    """

    def __init__(self, has_batteries: str, min_age: int, **kwargs):
        """
        Initializes a Toy.
        :param has_batteries: a str
        :param min_age: an int
        :param kwargs: Any additional keyword attributes for the base
                       class. Required to have 'name', 'description',
                       and 'product_id'.
        """
        super().__init__(**kwargs)
        if int(min_age) < 0:
            raise ValueError(f'min_age must be >= 0')
        self.has_batteries = BooleanType(has_batteries) == BooleanType.TRUE
        self.min_age = int(min_age)


class SantaWorkshop(Toy):
    """
    A concrete Toy class that represents a Santa Workshop.
    """

    def __init__(self, dimensions: str, num_rooms: int, **kwargs):
        """
        Initializes a SantaWorkshop.
        :param dimensions: a str, with a format of 'width,height'
        :param num_rooms: an int
        :param kwargs: Any additional keyword attributes for the base
                       class. Required to have 'min_age', 'name',
                       'description', and 'product_id'.
        """
        super().__init__(**kwargs)
        if not re.search('^C[0-9]{4}T$', self.product_id):
            raise ValueError("product_id must follow the format C####T "
                             "where # is a number")
        if self.has_batteries:
            raise ValueError(f'has_batteries must be False')
        if not re.search('^[0-9]+,[0-9]+$', dimensions):
            raise ValueError("dimensions must follow the format width,height")
        if int(num_rooms) <= 0:
            raise ValueError(f'num_rooms must be > 0')
        self.dimensions = dimensions
        self.num_rooms = int(num_rooms)


class SpiderType(Enum):
    """
    Represents a spider type.
    """
    TARANTULA = "Tarantula"
    WOLF_SPIDER = "Wolf Spider"


class RCSpider(Toy):
    """
    A concrete Toy Class that represents a remote controlled spider.
    """

    def __init__(self, speed: int, jump_height: int, has_glow: str,
                 spider_type: str, **kwargs):
        """
        Initializes a RCSpider.
        :param speed: an int
        :param jump_height: a int
        :param has_glow: a str
        :param spider_type: a str, must be either "Tarantula" or
                            "WolfSpider"
        :param kwargs: Any additional keyword attributes for the base
                       class. Required to have 'min_age', 'name',
                       'description', and 'product_id'.
        """
        super().__init__(**kwargs)
        if not re.search('^H[0-9]{4}T$', self.product_id):
            raise ValueError("product_id must follow the format H####T "
                             "where # is a number")
        if not self.has_batteries:
            raise ValueError(f'has_batteries must be True')
        if int(speed) <= 0:
            raise ValueError(f'speed must be > 0')
        if int(jump_height) <= 0:
            raise ValueError(f'jump_height must be > 0')
        self.speed = int(speed)
        self.jump_height = int(jump_height)
        self.has_glow = BooleanType(has_glow) == BooleanType.TRUE
        self.spider_type = SpiderType(spider_type)


class RobotBunnyColour(Enum):
    """
    Represents the color of a robot bunny.
    """
    ORANGE = "Orange"
    BLUE = "Blue"
    PINK = "Pink"


class RobotBunny(Toy):
    """
    A concrete Toy class that represents a Robot Bunny.
    """

    def __init__(self, num_sound: int, colour: str, **kwargs):
        """
        Initializes a RobotBunny.
        :param num_sound: an int
        :param colour: a str, must be either "Orange", "Blue", or "Pink"
        :param kwargs: Any additional keyword attributes for the base
                       class. Required to have 'min_age', 'name',
                       'description', and 'product_id'.
        """
        super().__init__(**kwargs)
        if not re.search('^E[0-9]{4}T$', self.product_id):
            raise ValueError("product_id must follow the format E####T "
                             "where # is a number")
        if not self.has_batteries:
            raise ValueError(f'has_batteries must be True')
        if int(num_sound) <= 0:
            raise ValueError(f'num_sound must be > 0')
        self.num_sound = int(num_sound)
        self.colour = RobotBunnyColour(colour)


class Stuffing(Enum):
    """
    Represents a stuffing.
    """
    POLYESTER_FIBREFILL = "Polyester Fibrefill"
    WOOL = "Wool"


class Size(Enum):
    """
    Represents a size.
    """
    SMALL = "S"
    MEDIUM = "M"
    LARGE = "L"


class Fabric(Enum):
    """
    Represents a fabric.
    """
    LINEN = "Linen"
    COTTON = "Cotton"
    ACRYLIC = "Acrylic"


class StuffedAnimal(Item, ABC):
    """
    Represents a Stuffed Animal Item.
    """

    def __init__(self, stuffing: str, fabric: str, size: str, **kwargs):
        """
        Initializes a StuffedAnimal.
        :param stuffing: a str, must be either "Polyester Fibrefill"
                         or "Wool"
        :param fabric: a str, must be either "Linen", "Cotton", or
                       "Acrylic"
        :param size: a str, must be either "S", "M", or "L"
        :param kwargs: Any additional keyword attributes for the base
                       class. Required to have 'name', 'description',
                       and 'product_id'.
        """
        super().__init__(**kwargs)
        self.stuffing = Stuffing(stuffing)
        self.size = Size(size)
        self.fabric = Fabric(fabric)


class DancingSkeleton(StuffedAnimal):
    """
    A concrete Stuffed Animal class that represents a Dancing Skeleton.
    """

    def __init__(self, has_glow: str, **kwargs):
        """
        Initializes a DancingSkeleton.
        :param kwargs: Any additional keyword attributes for the base
                       class. Required to have 'size', 'name',
                       'description', and 'product_id'.
        """
        super().__init__(**kwargs)
        if not re.search('^H[0-9]{4}S$', self.product_id):
            raise ValueError("product_id must follow the format H####S "
                             "where # is a number")
        if self.stuffing != Stuffing.POLYESTER_FIBREFILL:
            raise ValueError(f'stuffing must be '
                             f'"{Stuffing.POLYESTER_FIBREFILL.value}"')
        if self.fabric != Fabric.ACRYLIC:
            raise ValueError(f'fabric must be "{Fabric.ACRYLIC.value}"')
        if has_glow != BooleanType.TRUE.value:
            raise ValueError(f'has_glow must be "{BooleanType.TRUE.value}"')
        self.has_glow = BooleanType(has_glow) == BooleanType.TRUE


class Reindeer(StuffedAnimal):
    """
    A Concrete Stuffed Animal class that represents a Reindeer.
    """

    def __init__(self, has_glow: str, **kwargs):
        """
        Initializes a Reindeer.
        :param kwargs: Any additional keyword attributes for the base
                       class. Required to have 'size', 'name',
                       'description', and 'product_id'.
        """
        super().__init__(**kwargs)
        if not re.search('^C[0-9]{4}S$', self.product_id):
            raise ValueError("product_id must follow the format C####S "
                             "where # is a number")
        if self.stuffing != Stuffing.WOOL:
            raise ValueError(f'stuffing must be "{Stuffing.WOOL.value}"')
        if self.fabric != Fabric.COTTON:
            raise ValueError(f'fabric must be "{Fabric.COTTON.value}"')
        if has_glow != BooleanType.TRUE.value:
            raise ValueError(f'has_glow must be "{BooleanType.TRUE.value}"')
        self.has_glow = BooleanType(has_glow) == BooleanType.TRUE


class EasterBunnyColour(Enum):
    """
    Represents an Easter bunny color.
    """
    WHITE = "White"
    GREY = "Grey"
    PINK = "Pink"
    BLUE = "Blue"


class EasterBunny(StuffedAnimal):
    """
    A Concrete Stuffed Animal class that represents an Easter Bunny.
    """

    def __init__(self, colour: str, **kwargs):
        """
        Initializes a Reindeer.
        :param colour: a str, must be either "White", "Grey", "Pink" or
                       "Blue"
        :param kwargs: Any additional keyword attributes for the base
                       class. Required to have 'size', 'name',
                       'description', and 'product_id'.
        """
        super().__init__(**kwargs)
        if not re.search('^E[0-9]{4}S$', self.product_id):
            raise ValueError("product_id must follow the format E####S "
                             "where # is a number")
        if self.stuffing != Stuffing.POLYESTER_FIBREFILL:
            raise ValueError(f'stuffing must be '
                             f'"{Stuffing.POLYESTER_FIBREFILL.value}"')
        if self.fabric != Fabric.LINEN:
            raise ValueError(f'fabric must be "{Fabric.LINEN.value}"')
        self.colour = EasterBunnyColour(colour)


class Candy(Item, ABC):
    """
    Represents a Candy Item.
    """

    def __init__(self, has_nuts: str, has_lactose: str, **kwargs):
        """
        Initializes a Candy.
        :param has_nuts: a bool
        :param has_lactose: a bool
        :param kwargs: Any additional keyword attributes for the base
                       class. Required to have 'name', 'description',
                       and 'product_id'.
        """
        super().__init__(**kwargs)
        self.has_nuts = BooleanType(has_nuts) == BooleanType.TRUE
        self.has_lactose = BooleanType(has_lactose) == BooleanType.TRUE


class ToffeeVariety(Enum):
    SEA_SALT = "Sea Salt"
    REGULAR = "Regular"


class PumpkinCaramelToffee(Candy):
    """
    A concrete Candy class that represents an Pumpkin Caramel Toffee.
    """

    def __init__(self, variety: str, **kwargs):
        """
        Initializes a PumpkinCaramelToffee.
        :param variety: a str, must be either "Sea Salt" or "Regular"
        :param kwargs: Any additional keyword attributes for the base
                       class. Required to have 'name', 'description',
                       and 'product_id'.
        """
        super().__init__(**kwargs)
        if not re.search('^H[0-9]{4}C$', self.product_id):
            raise ValueError("product_id must follow the format H####C "
                             "where # is a number")
        if not self.has_nuts:
            raise ValueError(f'has_nuts must be True')
        if not self.has_lactose:
            raise ValueError(f'has_lactose must be True')
        self.variety = ToffeeVariety(variety)


class CandyCaneColour(Enum):
    """
    Represents the color of the stripes on the candy cane.
    """
    RED = "Red"
    GREEN = "Green"


class CandyCanes(Candy):
    """
    A Concrete Candy class that represents Candy Canes.
    """

    def __init__(self, colour: str, **kwargs):
        """
        Initializes a CandyCanes.
        :param colour: a str, must be either "Red" or "Green"
        :param kwargs: Any additional keyword attributes for the base
                       class. Required to have 'name', 'description',
                       and 'product_id'.
        """
        super().__init__(**kwargs)
        if not re.search('^C[0-9]{4}C$', self.product_id):
            raise ValueError("product_id must follow the format C####C "
                             "where # is a number")
        if self.has_nuts:
            raise ValueError(f'has_nuts must be False')
        if self.has_lactose:
            raise ValueError(f'has_lactose must be False')
        self.colour = CandyCaneColour(colour)


class CremeEggs(Candy):
    """
    A Concrete Candy class that represents Creme Eggs.
    """

    def __init__(self, pack_size: int, **kwargs):
        """
        Initializes a CremeEggs.
        :param pack_size: an int
        :param kwargs: Any additional keyword attributes for the base
                       class. Required to have 'name', 'description',
                       and 'product_id'.
        """
        super().__init__(**kwargs)
        if not re.search('^E[0-9]{4}C$', self.product_id):
            raise ValueError("product_id must follow the format E####C "
                             "where # is a number")
        if not self.has_nuts:
            raise ValueError(f'has_nuts must be True')
        if not self.has_lactose:
            raise ValueError(f'has_lactose must be True')
        if int(pack_size) <= 0:
            raise ValueError(f'pack_size must be > 0')
        self.pack_size = int(pack_size)
