"""
This module contains the Driver class which drives the FAM application.
"""

from datetime import datetime
from budget import BudgetCreator
from bank_account import BankAccountCreator
from transaction import Transaction
from user import User
from user import UserType


class Driver:
    """
    This Driver class is responsible for driving the FAM application. It
    maintains a user, a bank account and handles user's menu selection.
    """

    def __init__(self):
        """
        Initializes a Driver object.
        """
        self.user = None
        self.bank_account = None

    def setup(self) -> None:
        """
        Initializes user and bank account attributes from user inputs.
        :return: None
        """
        self.user = self.create_user()
        self.bank_account = BankAccountCreator.create_bank_account(
            self.user.user_type
        )

    def load_test_data(self) -> None:
        """
        Initializes user and bank account attributes from test data
        without prompting the user.
        :return: None
        """
        self.user = User('Anthony', 12, UserType.REBEL)
        self.bank_account = BankAccountCreator.load_test_account()

    def execute_user_type_menu(self) -> UserType:
        """
        Presents the user type menu and asks for user's choice. A user
        type is returned as an enum.
        :return: a UserType
        """
        user_type = None
        while user_type is None:
            print('  1. The Angel')
            print('  2. The Troublemaker')
            print('  3. The Rebel')
            choice = int(input('Enter a choice for user type (1-3): '))
            if choice == 1:
                user_type = UserType.ANGEL
            elif choice == 2:
                user_type = UserType.TROUBLEMAKER
            elif choice == 3:
                user_type = UserType.REBEL
            else:
                print('Invalid choice! Please enter again!')
        return user_type

    def create_user(self) -> User:
        """
        Prompts for user information, initializes a User object with
        the input data and returns it.
        :return: a User
        """
        name = input('Enter user name: ')
        age = -1
        while age <= 0:
            age = int(input('Enter age: '))
            if age <= 0:
                print('Invalid age, please enter again!')

        user_type = self.execute_user_type_menu()
        return User(name, age, user_type)

    def create_transaction(self) -> Transaction:
        """
        Prompts for transaction details, initializes a Transaction
        object with the input data and returns it.
        :return: a Transaction
        """
        amount = -1
        while amount <= 0:
            amount = float(input('Enter amount: '))
            if amount <= 0:
                print('Amount must be greater than 0! Please enter again!')
        budget_category = BudgetCreator.execute_budgets_menu()
        shop_name = input('Enter the name of the shop/website: ')
        return Transaction(datetime.now(), amount, budget_category, shop_name)

    def show_budgets_status(self) -> None:
        """
        Prints the user the current status of their budgets (locked or
        not) in addition to the amount spent, amount left, and the total
        amount allocated to the budget.
        :return: None
        """
        for budget in self.bank_account.get_budgets():
            print(budget)

    def show_transactions_by_budget(self) -> None:
        """
        Takes the user to a sub-menu where they select their budget
        category and view all the transactions to date in that category.
        :return: None
        """
        category = BudgetCreator.execute_budgets_menu()
        transactions = self.bank_account.get_transactions_by_budget(category)
        if len(transactions) == 0:
            print('There is no transaction in this category!')
        else:
            for transaction in transactions:
                print(transaction)

    def record_transaction(self) -> None:
        """
        Prompts user for transaction details and records it to the bank
        account.
        :return: None
        """
        transaction = self.create_transaction()
        self.bank_account.record_transaction(transaction)

    def show_bank_account_details(self) -> None:
        """
        Prints out the bank account details of the user and all
        transactions conducted to date alongside the closing balance.
        :return: None
        """
        print(self.bank_account)

    def execute_main_menu(self) -> None:
        """
        Drive the program by displaying the main menu, prompt the user
        for a choice and execute the appropriate behavior based on the
        choice.
        :return: None
        """
        print('Welcome to the Family Appointed Moderator!')
        choice = -1
        while choice != 5:
            print()
            print('============== MENU ==============')
            print('  1. View Budgets')
            print('  2. Record a Transaction')
            print('  3. View Transactions by Budget')
            print('  4. View Bank Account Details')
            print('  5. Exit')
            choice = int(input('Enter a choice (1-5): '))
            if choice == 1:
                self.show_budgets_status()
            elif choice == 2:
                self.record_transaction()
            elif choice == 3:
                self.show_transactions_by_budget()
            elif choice == 4:
                self.show_bank_account_details()
            elif choice != 5:
                print('Invalid choice! Please enter again!')
            print()
        print('Thanks for using The F.A.M!')


if __name__ == '__main__':
    driver = Driver()
    driver.setup()
    # driver.load_test_data()
    driver.execute_main_menu()
