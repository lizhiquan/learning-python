from datetime import datetime


class Transaction:
    def __init__(self, timestamp: datetime, amount: float,
                 budget_category: str, shop_name: str):
        self.timestamp = timestamp
        self.amount = amount
        self.budget_category = budget_category
        self.shop_name = shop_name

    def __str__(self):
        formatted_timestamp = self.timestamp.strftime("%Y-%m-%d %H:%M")
        return f'[{formatted_timestamp}]: A transaction of ${self.amount}' \
               f' was recorded at {self.shop_name}.'
