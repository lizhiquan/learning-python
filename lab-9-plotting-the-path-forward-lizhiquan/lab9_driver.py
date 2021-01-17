"""
This module houses the driver class which drives the program.
"""
from data_processor import DataProcessor
from observers import BarGraph, LineGraph, TableGenerator


class Driver:
    """
    This class is responsible for driving the program.
    """

    def __init__(self):
        """
        Initializes a driver.
        """
        self.processor = DataProcessor()

    def prompt_output_choice(self, message: str) -> bool:
        """
        Prompts for output choice and return user's selection.
        :param message: a str
        :return: True if user chooses yes, False otherwise
        """
        choice = None
        while choice not in ['y', 'n']:
            choice = input(f'{message} (y/n) ')
            if choice not in ['y', 'n']:
                print('Invalid choice')
        return choice == 'y'

    def setup_observers(self) -> None:
        """
        Prompts and sets up observers.
        :return: None
        """
        bar_graph = BarGraph(True, 'red', 'yellow')
        line_graph = LineGraph('solid', True, 'blue')
        table = TableGenerator('center')

        if self.prompt_output_choice('Would you like the output in bar graph?'
                                     ):
            self.processor.subscribe_callbacks(bar_graph)

        if self.prompt_output_choice('Would you like the output in line graph?'
                                     ):
            self.processor.subscribe_callbacks(line_graph)

        if self.prompt_output_choice('Would you like the output in table?'):
            self.processor.subscribe_callbacks(table)

    def show_main_menu(self) -> None:
        """
        Prints a menu to the console and handles user input.
        :return: None
        """
        menu_prompt = {
            1: (self.process_data, "Process data"),
            2: (quit, "Exit")
        }
        user_choice = -1
        while user_choice != 2:
            for key, value in menu_prompt.items():
                print(f"{key}: {value[1]}")
            try:
                user_choice = int(input("Enter your choice: "))
                choice = menu_prompt[user_choice][0]
            except KeyError:
                print("Option doesn't exist")
            except ValueError:
                print("Invalid entry")
            else:
                choice()
            finally:
                print()

    def process_data(self) -> None:
        """
        Prompts and process the data.
        :return: None
        """
        excel_file = input('Enter excel file: ')
        output_title = input('Enter output title: ')
        try:
            self.processor.process_data(excel_file, output_title)
        except Exception as e:
            print(e)
        else:
            print('Data processed')


if __name__ == '__main__':
    driver = Driver()
    driver.setup_observers()
    driver.show_main_menu()
