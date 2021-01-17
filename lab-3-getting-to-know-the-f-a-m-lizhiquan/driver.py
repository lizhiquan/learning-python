from datetime import datetime
from budget import BudgetCreator
from bank_account import BankAccountCreator
from transaction import Transaction
from user import User
from user import UserType


class Driver:
    def __init__(self):
        self.user = None
        self.bank_account = None

    def setup(self) -> None:
        self.user = self.create_user()
        self.bank_account = BankAccountCreator.create_bank_account(
            self.user.user_type
        )

    def load_test_data(self) -> None:
        self.user = User('Anthony', 12, UserType.REBEL)
        self.bank_account = BankAccountCreator.load_test_account()

    def get_user_type_menu(self) -> UserType:
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
        name = input('Enter user name: ')
        age = int(input('Enter age: '))
        user_type = self.get_user_type_menu()
        return User(name, age, user_type)

    def get_menu_choice(self) -> int:
        print('============== MENU ==============')
        print('  1. View Budgets')
        print('  2. Record a Transaction')
        print('  3. View Transactions by Budget')
        print('  4. View Bank Account Details')
        print('  5. Exit')
        return int(input('Enter a choice (1-5): '))

    def create_transaction(self) -> Transaction:
        # timestamp_str = input('Timestamp of the transaction (yyyy/MM/dd): ')
        amount = float(input('Enter amount: '))
        budget_category = BudgetCreator.execute_budgets_menu()
        shop_name = input('Enter the name of the shop/website: ')
        return Transaction(datetime.now(), amount, budget_category, shop_name)

    def show_budgets_status(self):
        for budget in self.bank_account.get_budgets():
            print(budget)

    def show_transactions_by_budget(self):
        category = BudgetCreator.execute_budgets_menu()
        transactions = self.bank_account.get_transactions_by_budget(category)
        if len(transactions) == 0:
            print('There is no transaction in this category!')
        else:
            for transaction in transactions:
                print(transaction)

    def record_transaction(self):
        transaction = self.create_transaction()
        self.bank_account.record_transaction(transaction)

    def show_bank_account_details(self):
        print(self.bank_account)

    def start(self) -> None:
        print('Welcome to the Family Appointed Moderator!')
        choice = -1
        while choice != 5:
            choice = self.get_menu_choice()
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
    # driver.setup()
    driver.load_test_data()
    driver.start()
