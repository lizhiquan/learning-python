"""
The program's entry point and drives the program.
The program manages a storefront and the supply chain.
"""
import xlrd
from store import Store
from order_processor import OrderProcessor


class UserMenu:
    """
    The main class that drives the program.
    """

    def __init__(self):
        """
        Initializes a UserMenu.
        """
        self.store = Store()
        self.menu_prompt = {
            # menu option: (method, StringRepresentation)
            1: (self.process_web_orders, "Process Web Orders"),
            2: (self.check_inventory, "Check Inventory"),
            3: (self.exit, "Exit")
        }

    def show_main_menu(self) -> None:
        """
        Prints a menu to the console and handles user input.
        :return: None
        """
        user_choice = -1
        while user_choice != 3:
            print("Welcome to ToySuppliesAreUs!")
            for key, value in self.menu_prompt.items():
                print(f"{key}: {value[1]}")
            try:
                user_choice = int(input("Enter your choice: "))
                choice = self.menu_prompt[user_choice][0]
            except KeyError:
                print("Option doesn't exist")
            except ValueError:
                print("Invalid entry")
            else:
                choice()
            finally:
                print()

    def process_web_orders(self) -> None:
        """
        Processes web orders from the online store.
        :return: None
        """
        # file_path = input('Enter a path to orders: ')
        file_path = "sample_orders.xlsx"
        order_processor = OrderProcessor(file_path)
        try:
            for order in order_processor.get_next_order():
                self.store.process_order(order)
        except FileNotFoundError:
            print("File not found")
        except xlrd.biffh.XLRDError:
            print("Unsupported format")
        except Exception as e:
            print(e)
        else:
            print("Orders processed")

    def check_inventory(self) -> None:
        """
        Checks the status of inventory levels.
        :return: None
        """
        self.store.check_inventory()

    def exit(self) -> None:
        """
        Generates a daily transaction report before exiting the program.
        :return: None
        """
        self.store.generate_daily_report()
        quit()


if __name__ == "__main__":
    menu = UserMenu()
    menu.show_main_menu()
