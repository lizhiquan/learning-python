"""
This module contains the class definitions for Budget, BudgetManager,
and BudgetCreator as a supporting class for constructing a BudgetManager
maintaining all the Budget objects.
"""

from enum import Enum


class BudgetCategory(Enum):
    """
    An enum represents supported budget categories.
    """
    GAMES_AND_ENTERTAINMENT = 'Games and Entertainment'
    CLOTHING_AND_ACCESSORIES = 'Clothing and Accessories'
    EATING_OUT = 'Eating Out'
    MISCELLANEOUS = 'Miscellaneous'


class Budget:
    """
    A class that represents a budget. A budget has:
    - a name/category
    - a total amount
    - a amount spent
    - a state determines if this budget is locked.
    """

    def __init__(self, category: BudgetCategory, total_amount: float):
        """
        Initializes a Budget.
        :param category: a BudgetCategory
        :param total_amount: a float
        """
        self.category = category
        self.total_amount = total_amount
        self.amount_spent = 0
        self._locked = False

    def __str__(self):
        return f'*** Budget: {self.name} ***\n' \
               f'• Status: {"Locked" if self._locked else "Available"}\n' \
               f'• Amount spent: ${self.amount_spent}\n' \
               f'• Amount left: ${self.total_amount - self.amount_spent}\n' \
               f'• Total amount: ${self.total_amount}'

    @property
    def name(self) -> str:
        """
        Returns the name/category of the budget.
        :return: a string
        """
        return str(self.category.value)

    @property
    def exceeded_ratio(self) -> float:
        """
        A property that calculates the exceeded ratio (amount spent /
        total amount) of this budget.
        :return: a float
        """
        return self.amount_spent / self.total_amount

    @property
    def locked(self) -> bool:
        """
        Read only property of the _locked attribute, to determine if
        this budget is locked.
        :return: a bool
        """
        return self._locked

    def lock(self) -> None:
        """
        Locks this budget.
        :return: None
        """
        self._locked = True


class BudgetManager:
    """
    The BudgetManager maintains a dictionary of budgets (referenced via
    budget names).
    """

    def __init__(self):
        """
        Initializes a BudgetManager.
        """
        self.budgets = {}

    def add_budget(self, budget: Budget) -> None:
        """
        Adds a budget to the dictionary.
        :param budget: a Budget
        :return: None
        """
        self.budgets[budget.category] = budget

    def get_budget(self, category: BudgetCategory) -> Budget:
        """
        Finds and returns budget stored in the dictionary.
        :param category: the budget name to get
        :return: a Budget
        """
        return self.budgets.get(category, None)

    def get_budgets(self) -> list:
        """
        Returns budgets stored in the dictionary as a list.
        :return: a list of Budget objects
        """
        return list(self.budgets.values())

    @property
    def no_locked_budgets(self) -> int:
        """
        Counts and returns the number of locked budgets.
        :return: an int, the number of locked budgets
        """
        count = 0
        for budget in self.budgets.values():
            if budget.locked:
                count += 1
        return count


class BudgetCreator:
    """
    An utility class that helps create Budget and BudgetManager.
    """

    @staticmethod
    def create_budget(budget_category: BudgetCategory) -> Budget:
        """
        Creates and returns a budget from user input for the given
        budget category.
        :param budget_category: a string
        :return: a Budget
        """
        amount = -1
        while amount <= 0:
            amount = float(input(f'Enter {budget_category.value} budget: '))
            if amount <= 0:
                print('Budget amount must be greater than 0! Please enter '
                      'again!')
        return Budget(budget_category, amount)

    @classmethod
    def create_budget_manager(cls) -> BudgetManager:
        """
        Prompts the user for the amount of each budget. These budgets
        will be added to a BudgetManager. The manager then will be
        returned out.
        :return: a BudgetManager
        """
        manager = BudgetManager()
        for category in list(BudgetCategory):
            budget = cls.create_budget(category)
            manager.add_budget(budget)
        return manager

    @staticmethod
    def execute_budgets_menu() -> BudgetCategory:
        """
        Presents the budget menu for the user to select and returns the
        budget category that user chooses.
        :return: a BudgetCategory
        """
        categories = list(BudgetCategory)
        no_budgets = len(categories)
        choice = -1
        print('Select a budget category:')
        while choice < 1 or choice > no_budgets:
            for idx, category in enumerate(categories):
                print(f'  {idx + 1}. {category.value}')
            choice = int(input(f'Enter a choice (1-{no_budgets}): '))
            if choice < 1 or choice > no_budgets:
                print('Invalid choice! Please enter again!')
        return categories[choice - 1]

    @classmethod
    def load_test_budget_manager(cls) -> BudgetManager:
        """
        Sets up and returns a BudgetManager with each budget of amount
        $100.
        :return: a BudgetManager
        """
        manager = BudgetManager()
        for category in list(BudgetCategory):
            budget = Budget(category, 100)
            manager.add_budget(budget)
        return manager
