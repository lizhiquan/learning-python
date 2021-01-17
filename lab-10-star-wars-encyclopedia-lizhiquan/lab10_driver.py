"""
This module houses the driver of this program.
"""
import starwars_request
import asyncio


class Lab10Driver:
    """
    This class is responsible for driving the program.
    """

    def __init__(self):
        """
        Initialize the Driver with the main menu, query type and output
        type menu maps (dictionaries).
        """
        self.main_menu_map = {
            1: (self.query, "Query"),
            2: (quit, "Exit")
        }
        self.output_map = Lab10Driver.generate_enum_menu_map(
            starwars_request.OutputMode)
        self.query_map = Lab10Driver.generate_enum_menu_map(
            starwars_request.RequestMode)

    def prompt_main_menu(self):
        """
        Display a dynamically generated menu from a dictionary that maps
        an integer to Enum entries. Exits the program if invalid input
        is encountered.
        :param prompt_menu:  a dictionary (key: int, value: Enum)
        :param header: a string
        :return: int, the choice made by the user
        """
        print(f" Star Wars Data Acquisition\n"
              " --------------------------")
        try:
            for key, value in self.main_menu_map.items():
                print(f"{key}: {value[1]}")
            user_choice = int(input("Enter your choice:"))
            return user_choice
        except TypeError:
            print("Invalid choice")

    @staticmethod
    def generate_enum_menu_map(my_enum_class):
        """
        Dynamically generates a dictionary where menu choices (int) are
        mapped to the enum entries.
        :param my_enum_class: The enum class
        :return: a dictionary (key: int, value: Enum)
        """
        menu_map = {}
        menu_id = 1
        for enum_entry in my_enum_class:
            menu_map[menu_id] = enum_entry
            menu_id += 1
        return menu_map

    @staticmethod
    def prompt_from_enum_map(enum_map: dict, heading: str):
        """
        Prompts the user to select an Enum entry based on the enum_map.
        Exits the program if wrong input is encountered.
        :param enum_map: a dictionary (key: int, value: enum entry)
        :param heading: a string, menu heading
        :return: Enum
        """
        print(f" {heading}\n -------------")
        for menu_id, enum_entry in enum_map.items():
            print(f"{menu_id}: {enum_entry.value}")
        try:
            user_choice = int(input("Enter your choice\n"))
            enum_entry = enum_map[user_choice]
            return enum_entry
        except (KeyError, TypeError):
            print("Invalid choice")
            print("Try again")
            exit()

    def query(self):
        """
        Prompts the user for the type of query, the type of output and
        the query details (id numbers or names to be queried). The
        method then creates an appropriate star wars manager instance and
        executes the queries asynchronously.
        """
        request_mode = Lab10Driver.prompt_from_enum_map(self.query_map,
                                                        "Select Query Type")
        data_set = []
        user_input = input("Enter the id number or name of the entity "
                           "you wish to query. Enter 'EXIT' to exit\n")
        while user_input.lower() != "exit":
            data_set.append(user_input)
            user_input = input("Enter the next id or name or enter "
                               "'EXIT' to exit\n")
        output_mode = Lab10Driver.prompt_from_enum_map(self.output_map,
                                                       "Select Output Mode")

        manager = starwars_request.StarWarsRequestManager(
            request_mode, output_mode)
        asyncio.run(manager.process_requests(data_set))


if __name__ == '__main__':
    driver = Lab10Driver()
    driver.query()






