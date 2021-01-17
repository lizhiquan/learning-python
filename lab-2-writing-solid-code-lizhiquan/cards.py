"""
This module is responsible for defining and encapsulating the various
Card types and any associated classes such as the CardGenerator.
"""

from abc import ABC
from abc import abstractmethod
from datetime import datetime
from datetime import timedelta
import re


class Card(ABC):
    """
    Refers to a generic card that can be found in a Wallet. Each card:
    - consists of a unique id_number
    - contains an expiry date.
    - Stores the name of the cardholder.

    When a card is accessed, it's validity is checked.
    """

    def __init__(self, name: str, id_num: str, exp_date: datetime):
        """
        Initializes a card object.
        :param name: a string, card holder name
        :param id_num: a string, card ID
        :param exp_date: a datetime, card expiry date
        """
        self.cardholder_name = name
        self.id_number = id_num
        self.expiry_date = exp_date

    @abstractmethod
    def access_card(self) -> bool:
        """
        Accesses the card. Needs to be overridden by each child class.
        Returns True if the card is successfully accessed.
        :return: a bool, True if the card is successfully accessed
        """
        pass

    def __str__(self):
        return f"Card: {self.id_number}\n" \
               f"------------------\n" \
               f"Owner Name: {self.cardholder_name}\n" \
               f"ID Number: {self.id_number}\n" \
               f"Expiry Date: {self.expiry_date}"


class IDCard(Card):
    """
    IDCard is an implementation of the Card abstract class.
    The id_number of an IDCard should follow the format "ARD######".
    """

    def access_card(self) -> bool:
        """
        Returns True if:
        - the expiry date is later than the current system date and
        - the format of the id_number is "ARD######".
        Otherwise returns False.
        :return: a bool, True if the conditions above are satisfied
        """
        if datetime.now() >= self.expiry_date:
            return False
        if not CardValidator.validate_id_card_number(self.id_number):
            return False
        return True


class CreditCard(Card):
    """
    CreditCard is an implementation of the Card abstract class.
    The id_number of a Credit Card should be 16 digits represented as a
    string.
    There is an extra attribute remaining_balance as a float. This is
    the amount of money the credit card has access to.
    """

    def __init__(self, name: str, id_num: str, exp_date: datetime,
                 remaining_balance: float):
        """
        Initializes a CreditCard object.
        :param name: a string, card holder name
        :param id_num: a string, card ID
        :param exp_date: a datetime, card expiry date
        :param remaining_balance: a float, card remaining balance
        """
        super().__init__(name, id_num, exp_date)
        self.remaining_balance = remaining_balance

    def access_card(self) -> bool:
        """
        Verifies the expiry date is later than the current system date
        and the format of the id_number is 16 digits, then prompts the
        user for the amount to charge. Charges the user by deducting the
        amount if the card has enough remaining_balance.
        Returns True if the card was charged successfully. Otherwise
        returns False.
        :return: a bool, True if the conditions above are satisfied
        """
        if datetime.now() >= self.expiry_date:
            return False
        if not CardValidator.validate_credit_card_number(self.id_number):
            return False

        charge_amount = -1
        while charge_amount <= 0:
            charge_amount = float(input("Enter an amount to charge: "))
            if charge_amount <= 0:
                print("Invalid amount! Amount must be greater than 0, "
                      "please enter again!")

        if self.remaining_balance < charge_amount:
            return False

        self.remaining_balance -= charge_amount
        return True

    def __str__(self):
        return f"Card: {self.id_number}\n" \
               f"------------------\n" \
               f"Owner Name: {self.cardholder_name}\n" \
               f"ID Number: {self.id_number}\n" \
               f"Expiry Date: {self.expiry_date}\n" \
               f"Remaining Balance: {self.remaining_balance}"


class CardGenerator:
    """
    A utility class that helps create different types of card.
    """

    @classmethod
    def execute_add_card_menu(cls, name: str) -> Card:
        """
        Presents a menu to ask for the type of card that the user wants
        to add, then calls the corresponding create method and returns
        the newly created card.
        :param name: a string, card holder name
        :return: a Card
        """
        choice = -1
        while not (choice == 1 or choice == 2):
            print("1. Add an ID card")
            print("2. Add a credit card")
            choice = int(input("Enter your choice (1-2): "))
            if choice == 1:
                return cls.create_id_card(name)
            elif choice == 2:
                return cls.create_credit_card(name)
            else:
                print("Invalid choice! Please enter again!")

    @staticmethod
    def create_id_card(name: str) -> IDCard:
        """
        Constructs an id card from user input and returns an IDCard
        object.
        :param name: a string, card holder name
        :return: an IDCard
        """
        card_number = ""
        valid = False
        while not valid:
            card_number = input("Enter card number (ARD######): ")
            valid = CardValidator.validate_id_card_number(card_number)
            if not valid:
                print("Invalid card number format! Please try again!")
        expiry_date_str = input("Enter expiry date (YY/MM/DD): ")
        expiry_date = datetime.strptime(expiry_date_str, "%y/%m/%d")
        return IDCard(name, card_number, expiry_date)

    @staticmethod
    def create_credit_card(name: str) -> CreditCard:
        """
        Constructs a credit card from user input and returns a
        CreditCard object.
        :param name: a string, card holder name
        :return: a CreditCard
        """
        card_number = ""
        valid = False
        while not valid:
            card_number = input("Enter card number (16 digits): ")
            valid = CardValidator.validate_credit_card_number(card_number)
            if not valid:
                print("Invalid card number format! Please try again!")
        expiry_date_str = input("Enter expiry date (MM/YY): ")
        expiry_date = datetime.strptime(expiry_date_str, "%m/%y")
        remaining_balance = -1
        while remaining_balance < 0:
            remaining_balance = float(input("Enter balance amount: "))
            if remaining_balance < 0:
                print("Invalid amount! Amount must be greater than or equal to"
                      " 0, please enter again!")
        return CreditCard(name, card_number, expiry_date, remaining_balance)


class CardValidator:
    """
    A utility class that helps validate different card numbers.
    """

    @staticmethod
    def validate_id_card_number(id_num: str) -> bool:
        """
        Validates the format of an ID card being "ARD######". Returns
        True if it follows the format.
        :return: a bool, True if the id follows the format above.
        """
        return re.search("^ARD[0-9]{6}$", id_num) is not None

    @staticmethod
    def validate_credit_card_number(id_num: str) -> bool:
        """
        Validates the format of a credit card being 16 digits string.
        Returns True if it follows the format.
        :return: a bool, True if the id follows the format above.
        """
        return re.search("^[0-9]{16}$", id_num) is not None


if __name__ == "__main__":
    # Valid
    card = IDCard("ID 1", "ARD123456", datetime.now() + timedelta(days=1))
    print(card)
    print("Access ID 1:", card.access_card(), "\n")

    # Invalid ID
    card = IDCard("ID 2", "abcxyz", datetime.now() + timedelta(days=1))
    print(card)
    print("Access ID 2:", card.access_card(), "\n")

    # Expired
    card = IDCard("ID 3", "ARD123456", datetime.now() - timedelta(days=1))
    print(card)
    print("Access ID 3:", card.access_card(), "\n")

    # Valid
    card = CreditCard("Credit 1", "1234123412341234",
                      datetime.now() + timedelta(days=1), 10)
    print(card)
    print("Access Credit 1:", card.access_card(), "\n")

    # Invalid ID
    card = CreditCard("Credit 2", "1234 1234 1234",
                      datetime.now() + timedelta(days=1), 10)
    print(card)
    print("Access Credit 2:", card.access_card(), "\n")

    # Expired
    card = CreditCard("Credit 3", "1234123412341234",
                      datetime.now() - timedelta(days=1), 10)
    print(card)
    print("Access Credit 3:", card.access_card(), "\n")
