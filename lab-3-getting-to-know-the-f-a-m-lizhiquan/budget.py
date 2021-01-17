class Budget:
    def __init__(self, name: str, total_amount: float):
        self.name = name
        self.total_amount = total_amount
        self.amount_spent = 0
        self.locked = False

    def __str__(self):
        return f'*** Budget: {self.name} ***\n' \
               f'• Status: {"Locked" if self.locked else "Available"}\n' \
               f'• Amount spent: ${self.amount_spent}\n' \
               f'• Amount left: ${self.total_amount - self.amount_spent}\n' \
               f'• Total amount: ${self.total_amount}'


class BudgetManager:
    def __init__(self):
        self.budgets = {}

    def add_budget(self, budget: Budget):
        self.budgets[budget.name] = budget

    def get_budget(self, category: str) -> Budget:
        return self.budgets.get(category, None)

    def get_budgets(self) -> list:
        return list(self.budgets.values())

    @property
    def no_locked_budgets(self) -> int:
        count = 0
        for budget in self.budgets.values():
            if budget.locked:
                count += 1
        return count


class BudgetCreator:
    BUDGET_CATEGORIES = [
        'Games and Entertainment',
        'Clothing and Accessories',
        'Eating Out',
        'Miscellaneous',
    ]

    @staticmethod
    def create_budget(budget_category: str) -> Budget:
        amount = -1
        while amount <= 0:
            amount = float(input(f'Enter {budget_category} budget: '))
            if amount <= 0:
                print('Budget amount must be greater than 0! Please enter '
                      'again!')
        return Budget(budget_category, amount)

    @classmethod
    def create_budgets(cls) -> BudgetManager:
        manager = BudgetManager()
        for category in cls.BUDGET_CATEGORIES:
            budget = cls.create_budget(category)
            manager.add_budget(budget)
        return manager

    @classmethod
    def execute_budgets_menu(cls) -> str:
        no_budgets = len(cls.BUDGET_CATEGORIES)
        choice = -1
        print('Select a budget category:')
        while choice < 1 or choice > no_budgets:
            for idx, category in enumerate(cls.BUDGET_CATEGORIES):
                print(f'  {idx + 1}. {category}')
            choice = int(input(f'Enter a choice (1-{no_budgets}): '))
            if choice < 1 or choice > no_budgets:
                print('Invalid choice! Please enter again!')
        return cls.BUDGET_CATEGORIES[choice-1]

    @classmethod
    def load_test_budgets(cls) -> BudgetManager:
        manager = BudgetManager()
        for category in cls.BUDGET_CATEGORIES:
            budget = Budget(category, 100)
            manager.add_budget(budget)
        return manager
