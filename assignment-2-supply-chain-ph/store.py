"""
This module houses the Store class that handles orders, getting items
from the factory and generating daily transaction reports.
"""
from datetime import datetime
from order_processor import Order
from items import ItemType, Item


class Store:
    """
    Represents a storefront that is responsible for:
    - Receiving orders and maintaining its inventory.
    - Getting items from a factory class if the store does not have
    enough stock.
    - Creating the Daily Transaction Report.

    - Attributes:
        - _inventory: dict[str(product_id): list(Item)]
        - _sample_products: dict[str(product_id): Item]
        - _orders_history: list(str)
    """

    def __init__(self):
        """
        Initializes a Store.
        """
        self._inventory = {}
        self._sample_products = {}
        self._orders_history = []

    def process_order(self, order: Order) -> None:
        """
        Processes an order.
        :param order: the order to process.
        :return: None
        """
        try:
            # Restock if needed
            products = self._inventory.get(order.product_id, [])
            current_quantity = len(products)
            while current_quantity < order.quantity:
                current_quantity = self.stock_inventory(order, 100)
        except Exception as e:
            print(f'Order {order.order_number}: {e}')
            self._orders_history.append(f'Order {order.order_number}, '
                                        f'Could not process order data was '
                                        f'corrupted, InvalidDataError - {e}')
        else:
            # Process the products
            products = self._inventory[order.product_id]
            new_quantity = len(products) - order.quantity
            self._inventory[order.product_id] = products[:new_quantity]
            self._orders_history.append(f'Order {order.order_number}, '
                                        f'Item {order.item_type.value}, '
                                        f'Product ID {order.product_id}, '
                                        f'Name "{order.name}", '
                                        f'Quantity {order.quantity}')

    def stock_inventory(self, order: Order, restock_quantity: int) -> int:
        """
        Stocks up the inventory and returns the current quantity after
        restock. It also creates a sample item and stores it in
        `sample_products`.
        :param order: an Order
        :param restock_quantity: an int, the quantity to stock
        :return: an int, the current quantity after restock
        """
        if order.product_id not in self._sample_products:
            self._sample_products[order.product_id] = self.create_item(order)

        products = self._inventory.get(order.product_id, [])
        new_products = [self.create_item(order)
                        for _ in range(restock_quantity)]
        products.extend(new_products)
        self._inventory[order.product_id] = products
        self._orders_history.append(f'Stock, Product ID {order.product_id}, '
                                    f'Name "{order.name}", '
                                    f'Quantity {restock_quantity}')
        return len(products)

    def create_item(self, order: Order) -> Item:
        """
        Creates an appropriate item from the factory stored in order.
        :param order: an Order
        :return: an Item
        """
        if order.item_type == ItemType.TOY:
            return order.factory.create_toy(order.product_details)
        elif order.item_type == ItemType.STUFFED_ANIMAL:
            return order.factory.create_stuffed_animal(order.product_details)
        return order.factory.create_candy(order.product_details)

    def check_inventory(self) -> None:
        """
        Checks and prints the inventory for stock levels.
        :return: None.
        """
        for product_id, products in self._inventory.items():
            quantity = len(products)
            item = self._sample_products[product_id]
            print(f'Product ID {item.product_id}, Name "{item.name}", '
                  f'Status: {self.get_quantity_status(quantity)}')

    def get_quantity_status(self, quantity: int) -> str:
        """
        Returns the status of an item in the inventory.
        :param quantity: an int
        :return: a str
        """
        if quantity >= 10:
            return 'IN STOCK'
        if quantity >= 3:
            return 'LOW'
        if quantity > 0:
            return 'VERY LOW'
        return 'OUT OF STOCK'

    def generate_daily_report(self) -> None:
        """
        Generates a daily transaction report.
        :return: None.
        """
        file_name = datetime.today().strftime("DTR_%d%m%y_%H%M.txt")
        with open(file_name, mode='w') as file:
            file.write('HOLIDAY STORE - DAILY TRANSACTION REPORT (DRT)\n')
            file.write(f'{datetime.today().strftime("%m-%d-%y %H:%M")}\n\n')
            for log in self._orders_history:
                file.write(f'{log}\n')
