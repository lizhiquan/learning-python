"""
This module contains the class definitions for all types of BankAccount
alongside BankAccountCreator as a supporting class to create an
appropriate bank account for a given user type.
"""

from abc import ABC
from abc import abstractmethod
from transaction import Transaction
from budget import Budget
from budget import BudgetManager
from budget import BudgetCategory
from budget import BudgetCreator
from user import UserType


class BankAccount(ABC):
    """
    An abstract base class that represents a bank account. By default,
    all bank accounts have:
    - a bank account number
    - a bank name
    - a bank balance
    - a budget manager to manage budgets
    - a list of transactions
    - a locked state to determine whether this account is locked.
    """

    def __init__(self, bank_account_no: str, bank_name: str,
                 bank_balance: float, budget_manager: BudgetManager):
        """
        Initializes a bank account.
        :param bank_account_no: a string
        :param bank_name: a string
        :param bank_balance: a float
        :param budget_manager: a BudgetManager
        """
        self.bank_account_no = bank_account_no
        self.bank_name = bank_name
        self.bank_balance = bank_balance
        self.transactions = []
        self.budget_manager = budget_manager
        self._locked = False

    def record_transaction(self, transaction: Transaction) -> bool:
        """
        Records a transaction and returns True if this transaction is
        recorded successfully. A transaction is recorded successfully
        when this bank account is not locked, has enough balance, and
        the budget associated with the transaction is not locked.
        :param transaction: a Transaction, the transaction to record
        :return: a bool, True if record successfully, False otherwise
        """
        if self._locked:
            print('Failed to record transaction! Your account has been locked!'
                  )
            return False

        if transaction.amount > self.bank_balance:
            print('Failed to record transaction! Not enough balance!')
            return False

        budget = self.budget_manager.get_budget(transaction.budget_category)
        if budget.locked:
            print('Failed to record transaction! This budget has been locked!')
            return False

        self.transactions.append(transaction)
        self.bank_balance -= transaction.amount
        budget.amount_spent += transaction.amount
        self._warn_and_lock_if_needed(transaction)
        return True

    @abstractmethod
    def _warn_and_lock_if_needed(self, transaction: Transaction) -> None:
        """
        Contains the logic to check if a warning or notification should
        be issued to the user. It also locks a budget or this bank
        account if needed. The exact algorithm would vary bank account
        to bank account.
        :param transaction: a Transaction, the newly recorded
                            transaction
        :return: None
        """
        pass

    def print_transactions_for_review(self, budget: Budget) -> None:
        """
        Prints a list of transactions in the given budget for review.
        :param budget: a Budget
        :return: None
        """
        print(f'Please review the following transactions in the {budget.name} '
              f'budget:')
        transactions = self.get_transactions_by_budget(budget.category)
        for transaction in transactions:
            print(transaction)

    def _warn_nearing_exceed_budget(self, budget: Budget,
                                    exceeded_percent: int) -> None:
        """
        Issues a warning to the user that they are about to exceed this
        budget.
        :param budget: a Budget, the budget that they are about to
                       exceed
        :param exceeded_percent: an int, the percent that they have
                                 already exceeded
        :return: None
        """
        print(f'[WARNING] You are about to exceed the {budget.name} budget! '
              f'You went over {exceeded_percent}% of the total '
              f'${budget.total_amount}.')

    def _notify_exceeded_budget(self, budget: Budget) -> None:
        """
        Notifies the user that they've just exceeded this budget.
        :param budget: a Budget, the budget that they've just exceeded
        :return: None
        """
        print(f'[NOTIFICATION] You have exceeded the {budget.name} budget.')

    def _lock_budget(self, budget: Budget) -> None:
        """
        Locks a budget.
        :param budget: a Budget, the budget to be locked
        :return: None
        """
        budget.lock()
        print(f'Your {budget.name} budget has now been locked!')

    def get_transactions_by_budget(self, category: BudgetCategory) -> list:
        """
        Returns a list of transactions for the given budget category.
        :param category: a BudgetCategory
        :return: a list of Transaction, the transactions in that
                 category
        """
        return [transaction
                for transaction in self.transactions
                if transaction.budget_category == category]

    def get_budgets(self) -> list:
        """
        Returns a list of budgets.
        :return: a list of Budget objects
        """
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
               f'• Status: {"Locked" if self._locked else "Available"}\n' \
               f'• Transactions:\n' \
               f'{transactions_info}' \
               f'• Closing balance: ${self.bank_balance}'


class AngelBankAccount(BankAccount):
    """
    This bank account is designed for Angel users. The Angel user
    represents a user who's parents are not worried at all.
    """

    def _warn_and_lock_if_needed(self, transaction: Transaction) -> None:
        """
        Issues a warning or locks budget/bank account when these
        conditions are met:
        - Never gets locked out of a budget category. They can continue
        spending money even if they exceed the budget in question.
        - Gets politely notified if they exceed a budget category.
        - Gets a warning if they exceed more than 90% of a budget.
        :param transaction: a Transaction, the newly recorded
                            transaction
        :return: None
        """
        budget = self.budget_manager.get_budget(transaction.budget_category)
        exceeded_ratio = budget.exceeded_ratio
        if exceeded_ratio > 1:
            self._notify_exceeded_budget(budget)
            self.print_transactions_for_review(budget)
        elif exceeded_ratio > 0.9:
            self._warn_nearing_exceed_budget(budget, 90)
            self.print_transactions_for_review(budget)


class TroublemakerBankAccount(BankAccount):
    """
    This bank account is designed for Troublemaker children. These
    children often find themselves in trouble. These are usually minor
    incidents and their parents are concerned but not worried.
    """

    def _warn_and_lock_if_needed(self, transaction: Transaction) -> None:
        """
        Issues a warning or locks budget/bank account when these
        conditions are met:
        - Gets a warning if they exceed more than 75% of a budget
        category.
        - Gets politely notified if they exceed a budget category.
        - Gets locked out of conducting transactions in a budget
        category if they exceed it by 120% of the amount assigned to the
        budget in question.
        :param transaction: a Transaction, the newly recorded
                            transaction
        :return: None
        """
        budget = self.budget_manager.get_budget(transaction.budget_category)
        exceeded_ratio = budget.exceeded_ratio
        if exceeded_ratio > 1.2:
            self._lock_budget(budget)
            self.print_transactions_for_review(budget)
        elif exceeded_ratio > 1:
            self._notify_exceeded_budget(budget)
            self.print_transactions_for_review(budget)
        elif exceeded_ratio > 0.75:
            self._warn_nearing_exceed_budget(budget, 75)
            self.print_transactions_for_review(budget)


class RebelBankAccount(BankAccount):
    """
    This bank account is designed for Rebel children. The Rebel
    represents a child who refuses to follow any rules and believes that
    society should be broken down and restructured. Parents of these
    children are quite worried about them.
    """

    def _warn_and_lock_if_needed(self, transaction: Transaction) -> None:
        """
        Issues a warning or locks budget/bank account when these
        conditions are met:
        - They get a warning for every transaction after exceeding 50%
        of a budget.
        - Gets ruthlessly notified if they exceed a budget category.
        - Gets locked out of conducting transactions in a budget
        category if they exceed it by 100% of the amount assigned to the
        budget in question.
        - If they exceed their budget in 2 or more categories then they
        get locked out of their account completely.
        :param transaction: a Transaction, the newly recorded
                            transaction
        :return: None
        """
        budget = self.budget_manager.get_budget(transaction.budget_category)
        exceeded_ratio = budget.exceeded_ratio
        if exceeded_ratio > 1:
            self._notify_exceeded_budget(budget)
            self._lock_budget(budget)
            self.print_transactions_for_review(budget)
            if self.budget_manager.no_locked_budgets >= 2:
                self._locked = True
                print('YOUR BANK ACCOUNT HAS BEEN LOCKED!')
        elif exceeded_ratio > 0.5:
            self._warn_nearing_exceed_budget(budget, 50)
            self.print_transactions_for_review(budget)


class BankAccountCreator:
    """
    An utility class that helps create a BankAccount.
    """

    _user_type_mapper = {
        UserType.ANGEL: AngelBankAccount,
        UserType.TROUBLEMAKER: TroublemakerBankAccount,
        UserType.REBEL: RebelBankAccount,
    }
    """
    A dictionary that maps a UserType enum to an appropriate BankAccount
    class. 
    """

    @staticmethod
    def load_test_account() -> BankAccount:
        """
        Creates and returns a test bank account.
        :return: a BankAccount
        """
        budget_manager = BudgetCreator.load_test_budget_manager()
        return TroublemakerBankAccount('123123', 'HSBC', 1000, budget_manager)

    @classmethod
    def create_bank_account(cls, user_type: UserType) -> BankAccount:
        """
        Prompts the user for bank account details, initializes a Bank
        Account based on the given user type and returns it.
        :param user_type: a UserType
        :return: a BankAccount
        """
        bank_account_no = input('Enter bank account number: ')
        bank_name = input('Enter bank name: ')
        bank_balance = -1
        while bank_balance < 0:
            bank_balance = float(input('Enter bank balance: '))
            if bank_balance < 0:
                print('Bank balance must be greater than or equal to 0! Please'
                      ' enter again!')
        budget_manager = BudgetCreator.create_budget_manager()
        return cls._user_type_mapper[user_type](
            bank_account_no,
            bank_name,
            bank_balance,
            budget_manager,
        )
