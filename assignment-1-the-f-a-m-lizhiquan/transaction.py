"""
This module contains the class definition for Transaction.
"""

from datetime import datetime
from budget import BudgetCategory


class Transaction:
    """
    The Transaction class maintains all information of a transaction,
    which has a timestamp, an amount, a budget category, and a shop
    name.
    """

    def __init__(self, timestamp: datetime, amount: float,
                 budget_category: BudgetCategory, shop_name: str):
        """
        Initializes a Transaction.
        :param timestamp: a datetime
        :param amount: a float
        :param budget_category: a BudgetCategory
        :param shop_name: a string
        """
        self.timestamp = timestamp
        self.amount = amount
        self.budget_category = budget_category
        self.shop_name = shop_name

    def __str__(self):
        formatted_timestamp = self.timestamp.strftime("%Y-%m-%d %H:%M")
        return f'[{formatted_timestamp}]: A transaction of ${self.amount}' \
               f' was recorded at {self.shop_name}.'
