from abc import ABC
from abc import abstractmethod
from transaction import Transaction
from budget import BudgetManager
from budget import BudgetCreator
from user import UserType


class BankAccount(ABC):
    def __init__(self, bank_account_no: str, bank_name: str,
                 bank_balance: float, budget_manager: BudgetManager):
        self.bank_account_no = bank_account_no
        self.bank_name = bank_name
        self.bank_balance = bank_balance
        self.transactions = []
        self.budget_manager = budget_manager
        self.locked = False

    def record_transaction(self, transaction: Transaction) -> bool:
        if self.locked:
            print('Failed to record transaction! This account has been locked!'
                  )
            return False

        if transaction.amount > self.bank_balance:
            print('Failed to record transaction! Not enough balance!')
            return False

        budget = self.budget_manager.get_budget(transaction.budget_category)
        if budget.locked:
            print('Failed to record transaction! This budget is locked!')
            return False

        self.transactions.append(transaction)
        self.bank_balance -= transaction.amount
        budget.amount_spent += transaction.amount
        self.warn_and_lock_if_needed(transaction)
        return True

    @abstractmethod
    def warn_and_lock_if_needed(self, transaction: Transaction):
        pass

    def get_transactions_by_budget(self, category: str) -> list:
        return [t for t in self.transactions if t.budget_category == category]

    def get_budgets(self) -> list:
        return self.budget_manager.get_budgets()

    def __str__(self):
        transactions_info = ''
        for transaction in self.transactions:
            transactions_info += f'{transaction}\n'
        if len(transactions_info) == 0:
            transactions_info = "You haven't made any transaction yet.\n"
        return f'*** Bank Account Details ***\n' \
               f'• Bank account number: {self.bank_account_no}\n' \
               f'• Bank name: {self.bank_name}\n' \
               f'• Status: {"Locked" if self.locked else "Available"}\n' \
               f'• Transactions:\n' \
               f'{transactions_info}' \
               f'• Closing balance: ${self.bank_balance}'


class AngelBankAccount(BankAccount):
    def warn_and_lock_if_needed(self, transaction: Transaction):
        budget = self.budget_manager.get_budget(transaction.budget_category)
        if budget.amount_spent >= budget.total_amount:
            exceeded_ratio = budget.amount_spent / budget.total_amount - 1
            if exceeded_ratio > 0.9:
                print(f'Warning! You have exceeded more than 90% of '
                      f'{transaction.budget_category}.')
            else:
                print(f'You have exceeded {transaction.budget_category} '
                      f'budget.')


class TroublemakerBankAccount(BankAccount):
    def warn_and_lock_if_needed(self, transaction: Transaction):
        budget = self.budget_manager.get_budget(transaction.budget_category)
        if budget.amount_spent >= budget.total_amount:
            exceeded_ratio = budget.amount_spent / budget.total_amount - 1
            if exceeded_ratio > 1.2:
                budget.locked = True
                print(f'Your budget {transaction.budget_category} has been '
                      f'locked!')
            elif exceeded_ratio > 0.75:
                print(f'Warning! You have exceeded more than 75% of '
                      f'{transaction.budget_category}.')
            else:
                print(f'You have exceeded {transaction.budget_category} '
                      f'budget.')


class RebelBankAccount(BankAccount):
    def warn_and_lock_if_needed(self, transaction: Transaction):
        budget = self.budget_manager.get_budget(transaction.budget_category)
        if budget.amount_spent >= budget.total_amount:
            exceeded_ratio = budget.amount_spent / budget.total_amount - 1
            if exceeded_ratio > 1:
                budget.locked = True
                print(f'Your budget {transaction.budget_category} has been '
                      f'locked!')
                if self.budget_manager.no_locked_budgets >= 2:
                    self.locked = True
                    print(f'YOUR ACCOUNT HAS BEEN LOCKED!')
            elif exceeded_ratio > 0.5:
                print(f'Warning! You have exceeded more than 50% of '
                      f'{transaction.budget_category}.')
            else:
                print(f'You have exceeded {transaction.budget_category} '
                      f'budget.')


class BankAccountCreator:
    @staticmethod
    def load_test_account() -> BankAccount:
        budgets = BudgetCreator.load_test_budgets()
        return TroublemakerBankAccount('123123', 'HSBC', 1000, budgets)

    @staticmethod
    def create_bank_account(user_type: UserType) -> BankAccount:
        bank_account_no = input('Enter bank account number: ')
        bank_name = input('Enter bank name: ')
        bank_balance = -1
        while bank_balance < 0:
            bank_balance = float(input('Enter bank balance: '))
            if bank_balance < 0:
                print('Bank balance must be greater than or equal to 0! Please'
                      ' enter again!')
        budgets = BudgetCreator.create_budgets()
        if user_type == UserType.ANGEL:
            return AngelBankAccount(
                bank_account_no,
                bank_name,
                bank_balance,
                budgets,
            )
        elif user_type == UserType.TROUBLEMAKER:
            return TroublemakerBankAccount(
                bank_account_no,
                bank_name,
                bank_balance,
                budgets,
            )
        return RebelBankAccount(
            bank_account_no,
            bank_name,
            bank_balance,
            budgets,
        )
