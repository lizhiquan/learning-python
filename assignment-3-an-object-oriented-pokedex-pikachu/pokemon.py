"""
This module is responsible for Pokemon Data.

Classes:
- PokemonAbility
- PokemonStat
- PokemonMove
- PokemonItem
- Pokemon
"""


class PokemonAbility:
    """Represents a Pokemon Ability"""

    def __init__(self, name: str, id: int, generation: dict,
                 effect_entries: list, pokemon: list, **kwargs):
        """
        Initializes Pokemon Ability
        :param name: a str, the ability's name
        :param id: an int, converted to an int, the id of the ability
        :param generation: a dict {name, url}
        :param effect_entries: a list of dicts {effect, short_effect,
                               language: {name, url}}
        :param pokemon: a list, of dicts {is_hidden, slot, pokemon:
                        {name, url}}
        """
        self.name = name
        self.id = id
        self.generation = generation["name"]
        for entry in effect_entries:
            if entry["language"]["name"] == "en":
                self.effect = entry["effect"]
                self.short_effect = entry["short_effect"]
        self.pokemon = [entry["pokemon"]["name"] for entry in pokemon]

    def __str__(self) -> str:
        return (
            f"Ability Name: {self.name}\n"
            f"ID: {self.id}\n"
            f"Generation: {self.generation}\n"
            f"Effect: {self.effect}\n"
            f"Effect (Short): {self.short_effect}\n"
            f"Pokemon: {', '.join(self.pokemon)}\n"
        )


class PokemonItem:
    """Represents an Item in the Pokemon Universe"""

    def __init__(self, id: int, name: str, cost: int, fling_power: int,
                 effect_entries: list, **kwargs):
        """
        Initializes Pokemon Item
        :param id: an int, of the item's id
        :param name: a string, the item's name
        :param cost: an int, the item's cost
        :param fling_power: an int, determines the item's power
        :param effect_entries: a list of dicts {effect, short effect,
                               language: {name, url}}
        """
        self.id = id
        self.name = name
        self.cost = cost
        self.fling_power = fling_power
        for entry in effect_entries:
            if entry["language"]["name"] == "en":
                self.short_effect = entry["short_effect"]

    def __str__(self) -> str:
        return (
            f"Item Name: {self.name}\n"
            f"ID: {self.id}\n"
            f"Cost: {self.cost}\n"
            f"Fling Power: {self.fling_power}\n"
            f"Effect (Short): {self.short_effect}\n"
        )


class PokemonStat:
    """Represents a Pokemon Stat"""

    def __init__(self, name: str, id: int, is_battle_only: bool,
                 move_damage_class: dict, **kwargs):
        """
        Initializes PokemonStat
        :param name: a string, the stats name
        :param id: an int, the stat's id
        :param is_battle_only: a boolean, determines if the stat is only
                               for combat.
        :param move_damage_class: a dict {name, url}
        """
        self.name = name
        self.id = id
        self.is_battle_only = is_battle_only
        self.move_damage_class = move_damage_class["name"] \
            if move_damage_class else None

    def __str__(self) -> str:
        return (
            f"Stat Name: {self.name}\n"
            f"ID: {self.id}\n"
            f"Is Battle Only: {self.is_battle_only}\n"
            f"Move Damage Class: {self.move_damage_class}\n"
        )


class PokemonMove:
    """Represents a Pokemon Move"""

    def __init__(self, name: str, id: int, generation: dict, accuracy: int,
                 pp: int, power: int, type: dict, damage_class: dict,
                 effect_entries: list, **kwargs):
        """
        :param name: str, the move's name
        :param id: an int, the move's id,
        :param generation: a dict, contains 2 keys, name and url
        :param accuracy: an int, the move's accuracy
        :param pp: an int, the move's pp cost
        :param power: an int, the moves power level
        :param type: a dict, contains 2 keys, name and url
        :param damage_class: a dict, contains 2 keys, name and url
        :param effect_entries: a list of dicts, with keys effect,
                               short_effect, language: {name, url}
        """
        self.name = name
        self.id = id
        self.generation = generation["name"]
        self.accuracy = accuracy
        self.pp = pp
        self.power = power
        self.type = type["name"]
        self.damage_class = damage_class["name"]
        for entry in effect_entries:
            if entry["language"]["name"] == "en":
                self.short_effect = entry["short_effect"]

    def __str__(self) -> str:
        return (
            f"Move Name: {self.name}\n"
            f"ID: {self.id}\n"
            f"Generation: {self.generation}\n"
            f"Accuracy: {self.accuracy}\n"
            f"PP: {self.pp}\n"
            f"Power: {self.power}\n"
            f"Type: {self.type}\n"
            f"Damage Class: {self.damage_class}\n"
            f"Effect (Short): {self.short_effect}\n"
        )


class Pokemon:
    """Represents a Pokemon"""

    def __init__(self, name: str, id: int, height: int, weight: int,
                 stats: list, types: list, abilities: list, moves: list,
                 **kwargs):
        """
        :param name: a str, the pokemon's name
        :param id: an int, the pokemon's id
        :param height: an int, the pokemon's height
        :param weight: an int, the pokemon's weight
        :param types: a list of strings, the pokemon's types
        :param abilities: a list of dicts {ability: {name, url},
                          is_hidden, slot}
        :param stats: a list of dicts {base_stat, effort, stat: {name,
                      url}}
        :param moves: a list of dicts 
                      move: {name, url},
                      version_group_details: [{level_learned_at, ...}]
        """
        self.name = name
        self.id = id
        self.weight = weight
        self.height = height
        self.types = [type['type']['name'] for type in types]
        self.stats = [(stat['stat']['name'], stat['base_stat'])
                      for stat in stats]
        self.abilities = [ability['ability']['name']
                          for ability in abilities]
        self.moves = [(move['move']['name'],
                      move['version_group_details'][0]['level_learned_at'])
                      for move in moves]

    @property
    def stat_names(self) -> list:
        """
        Returns a list of stat names.
        :return: a list
        """
        return [stat.name if isinstance(stat, PokemonStat)
                else stat[0]
                for stat in self.stats]

    @property
    def move_names(self) -> list:
        """
        Returns a list of move names.
        :return: a list
        """
        return [move.name if isinstance(move, PokemonMove)
                else move[0]
                for move in self.moves]

    def __str__(self) -> str:
        formatted_stats = [stat if isinstance(stat, PokemonStat)
                           else f"{stat[0]}: {stat[1]}"
                           for stat in self.stats]
        formatted_moves = [move if isinstance(move, PokemonMove)
                           else f"{move[0]}: learned at level {move[1]}"
                           for move in self.moves]
        stats = '\n'.join([f'• {stat}' for stat in formatted_stats])
        abilities = '\n'.join([f'• {ability}' for ability in self.abilities])
        moves = '\n'.join([f'• {move}' for move in formatted_moves])
        return (
            f"Pokemon Name: {self.name}\n"
            f"ID: {self.id}\n"
            f"Height: {self.height} decimetres\n"
            f"Weight: {self.weight} hectograms\n"
            f"Types: {', '.join(self.types)}\n"
            f"Stats:\n{stats}\n"
            f"Abilities:\n{abilities}\n"
            f"Moves:\n{moves}\n"
        )
