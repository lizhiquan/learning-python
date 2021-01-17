"""
This module houses the OrderProcessor and supporting classes that are
responsible for processing orders in an excel file.
"""
import pandas
from typing import Generator
from items import ItemType
from item_factory import ItemFactory
from item_factory import ChristmasFactory
from item_factory import HalloweenFactory
from item_factory import EasterFactory


class Order:
    """
    A representation of an item order.
    """

    def __init__(self, order_number: int, product_id: str, item: str,
                 name: str, quantity: int, factory: ItemFactory, **kwargs):
        """
        Initializes an order.
        """
        if pandas.isna(order_number):
            raise ValueError('order_number is missing')
        if pandas.isna(quantity):
            raise ValueError('quantity is missing')
        if int(quantity) <= 0:
            raise ValueError('quantity must be > 0')
        self.order_number = int(order_number)
        self.product_id = product_id
        self.item_type = ItemType(item)
        self.name = name
        self.quantity = int(quantity)
        self.factory = factory
        self.product_details = {
            'name': name,
            'product_id': product_id,
            **kwargs,
        }


class OrderProcessor:
    """
    An Order Utility class that is responsible for reading each row of
    excel files and creating and yielding an Order object.
    """

    def __init__(self, file_path: str):
        """
        Initializes an OrderProcessor.
        :param file_path: a str, path to the file
        """
        self.factory_map = {
            "Christmas": ChristmasFactory(),
            "Halloween": HalloweenFactory(),
            "Easter": EasterFactory(),
        }
        self.file_path = file_path

    def get_next_order(self) -> Generator[Order, None, None]:
        """
        Loads orders from an excel sheet file, instantiates an Order
        object and yields it.
        :return: a generator that yields Order
        """
        df = pandas.read_excel(self.file_path)
        for row in df.iterrows():
            row_no = row[0] + 2
            row_data = row[1]

            try:
                factory = self.factory_map[row_data['holiday']]
            except KeyError as e:
                print(f'Line {row_no}: Invalid holiday {e}')
                continue

            row_data.drop('holiday', inplace=True)

            try:
                order = Order(factory=factory, **row_data)
            except Exception as e:
                print(f'Line {row_no}: {e}')
            else:
                yield order
