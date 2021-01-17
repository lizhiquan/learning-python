"""
Contains the class definitions for all Card Types alongside any
interfaces or supporting classes that they might use.
"""
from abc import ABC, abstractmethod
from datetime import date


class ExpiryDate:
    """
    Describes an expiry date for a card. Contains a property called
    "expired" that validates the expiry date with the system clock.
    """

    def __init__(self, expiry_day, expiry_month, expiry_year):
        """
        Initialize an ExpiryDate with data that describes a expiry date
        :param expiry_day: a string that represents a number from 1-31
        :param expiry_month: a string that represents a number from 1-12
        :param expiry_year: a string that represents a 4-digit year.
        """
        self._expiry_date = date(int(expiry_year), int(expiry_month),
                                 int(expiry_day))

    @property
    def expired(self):
        """
        A property that calculates the expiry status of a card with
        respect to system clock.
        :return: True if the expiry date has passed, False otherwise
        """
        if date.today() >= self._expiry_date:
            return True
        return False

    def __str__(self):
        return f"Expiry Date: {self._expiry_date}"


class ContactDetails:
    """
    Represents a collection of contact details of an individual that
    owns a card.

    The class models a name, date of birth, address,
    email, and a telephone number. Of these only the name is mandatory as
    different cards will require different details. The rest are optional
    and initialize to None if not provided.
    """

    field_map = {
        "name": "Name",
        "date_of_birth": "Date of Birth",
        "address": "Address",
        "email": "E-mail",
        "tel_number": "Telephone Number"
    }
    """ 
    A dictionary to map attributes to their string representations
    """

    def __init__(self, name, date_of_birth=None, address=None, email=None,
                 tel_number=None):
        self.name = name
        self.date_of_birth = date_of_birth
        self.address = address
        self.email = email
        self.tel_number = tel_number

    def get_details(self):
        """
        :return: Returns a dictionary of the string representation
        of attributes and their value, if initialized.
        """
        details = {}
        for key, value in self.__dict__.items():
            if value:
                details[self.field_map[key]] = value
        return details


class Card(ABC):
    """
    An abstract base class that represents a class. In the event that
    this class is one of many being inherited, inherit this class last.
    By default all cards have a issuer name, and a card id.
    """

    def __init__(self, issuer_name, card_id, **kwargs):
        """
        Initializes a card.
        :param issuer_name: a string
        :param card_id: a string
        :param kwargs: a dictionary of named arguments and values. This
        is to provide support in the event of multiple inheritance and
        complex super() MRO calls. Usually contains the attributes of
        other interfaces that have been implemented.
        """
        self._issuer_name = issuer_name
        self._card_id = card_id
        super().__init__(**kwargs)

    @property
    def card_id(self):
        """
        Read only property of the _card_id attribute, which should not
        be set outside the constructor.
        :return: a string
        """
        return self._card_id

    @abstractmethod
    def validate_card(self):
        """
        Contains the logic to check if a card is valid or note. The
        exact algorithm would vary card to card.
        :return:
        """
        pass

    @classmethod
    @abstractmethod
    def get_fields(cls):
        """
        :return: Returns a dictionary of attributes and their string
        representations to allow a Menu class to dynamically initialize
        the class using kwargs.
        """
        fields = {
            "issuer_name": "Issuer Organization",
            "card_id": "Card ID"
        }
        return fields

    @abstractmethod
    def __str__(self):
        return f"Issuer Name: {self._issuer_name}\n" \
               f"Card ID: {self.card_id}"


class IDCard(Card):
    """
    An ID card here refers to a card issued by the government or a school
    and has an ID that begins with the letter A followed by numbers.

    This class inherits the Card base class.
    """

    def __init__(self, name, dob_year, dob_month, dob_day, expiry_day,
                 expiry_month, expiry_year, **kwargs):
        """
        Initializes an ID card.
        :param name: a string
        :param dob_year: a string
        :param dob_month: a string
        :param dob_day: a string
        :param expiry_day: a string that represents a number from 1-31
        :param expiry_month: a string that represents a number from 1-12
        :param expiry_year: a string that represents a 4-digit year.
        :param kwargs: a dictionary of named arguments and values. This
        is to provide support in the event of multiple inheritance and
        complex super() MRO calls. Usually contains the attributes of
        other interfaces that have been implemented.
        """
        date_of_birth = date(int(dob_year), int(dob_month), int(dob_day))
        self.contact_details = ContactDetails(name=name,
                                              date_of_birth=date_of_birth)
        self.expiry_date = ExpiryDate(expiry_day, expiry_month, expiry_year)
        super().__init__(**kwargs)

    def validate_card(self):
        """
        Validates an ID card. An ID card is valid if it is not expired
        and has a card id following the format A###### where # is a
        number.
        :return: True if valid, False otherwise
        """
        if not self.expiry_date.expired and self.card_id[:1] == "A" and \
                self.card_id[1:].isdigit():
            return True
        return False

    @classmethod
    def get_fields(cls):
        """
        :return: Returns a dictionary of attributes and their string
        representations to allow a Menu class to dynamically initialize
        the class using kwargs.
        """
        fields = super().get_fields()
        fields["name"] = "Name"
        fields["dob_year"] = "Date of Birth Year"
        fields["dob_month"] = "Date of Birth Month"
        fields["dob_day"] = "Date of Birth Day"
        fields["expiry_year"] = "Expiry Year"
        fields["expiry_month"] = "Expiry Month"
        fields["expiry_day"] = "Expiry Day"
        return fields

    def __str__(self):
        formatted = f'{super().__str__()}\n' \
                    f'{self.expiry_date}'
        for key, value in self.contact_details.get_details().items():
            formatted = f"{formatted}\n{key}: {value}"
        return formatted


class BalanceCard(Card):
    """
    A balance card here refers to a card that has a balance amount.

    This class inherits the Card base class.
    """

    def __init__(self, balance: str, **kwargs):
        """
        Initializes a BalanceCard.
        :param balance: a string, the balance of the card
        :param kwargs: a dictionary of named arguments and values. This
        is to provide support in the event of multiple inheritance and
        complex super() MRO calls. Usually contains the attributes of
        other interfaces that have been implemented.
        """
        self.balance = float(balance)
        super().__init__(**kwargs)

    @abstractmethod
    def validate_card(self) -> bool:
        """
        Validates a balance card. A balance card is valid if its balance
        is not less than 0.
        :return: True if valid, False otherwise
        """
        return self.balance >= 0

    @classmethod
    @abstractmethod
    def get_fields(cls) -> dict:
        """
        :return: Returns a dictionary of attributes and their string
        representations to allow a Menu class to dynamically initialize
        the class using kwargs.
        """
        fields = super().get_fields()
        fields['balance'] = 'Balance'
        return fields

    @abstractmethod
    def __str__(self):
        return f'{super().__str__()}\n' \
               f'Balance: {self.balance}'


class TransitCard(BalanceCard):
    """
    A transit card here refers to a card that is used for the transit
    system. It has money as its balance in addition to contact
    information (name and email). The card ID of this card begins with
    the letter 'T' and be followed by digits (eg: T123456).

    This class inherits the BalanceCard class.
    """

    def __init__(self, name: str, email: str, monthly_pass: str, **kwargs):
        """
        Initializes a TransitCard.
        :param name: a string
        :param email: a string
        :param monthly_pass: a string, y or n
        :param kwargs: a dictionary of named arguments and values. This
        is to provide support in the event of multiple inheritance and
        complex super() MRO calls. Usually contains the attributes of
        other interfaces that have been implemented.
        """
        self.has_monthly_pass = monthly_pass == 'y'
        self.contact_details = ContactDetails(name, email=email)
        super().__init__(**kwargs)

    def validate_card(self) -> bool:
        """
        Validates a transit card. A transit card is valid if it has a
        balance ≥ 0 and it's card_id must begin with the letter 'T' and
        be followed by digits (eg: T123456).
        :return: True if valid, False otherwise
        """
        return super().validate_card() and self.card_id[:1] == "T" and \
            self.card_id[1:].isdigit()

    @classmethod
    def get_fields(cls) -> dict:
        """
        :return: Returns a dictionary of attributes and their string
        representations to allow a Menu class to dynamically initialize
        the class using kwargs.
        """
        fields = super().get_fields()
        fields['name'] = 'Contact Name'
        fields['email'] = 'Contact Email'
        fields['monthly_pass'] = 'Has Monthly Pass (y/n)'
        return fields

    def __str__(self):
        formatted = f'{super().__str__()}\n' \
                    f'Has monthly pass: {self.has_monthly_pass}'
        for key, value in self.contact_details.get_details().items():
            formatted = f"{formatted}\n{key}: {value}"
        return formatted


class GiftCard(BalanceCard):
    """
    A gift card here refers to a card that has a balance and an expiry
    date. The card ID of this card begins with the letter 'G' and be
    followed by digits (eg: G123456).

    This class inherits the BalanceCard class.
    """

    def __init__(self, expiry_day, expiry_month, expiry_year, **kwargs):
        """
        Initializes a GiftCard.
        :param expiry_day: a string that represents a number from 1-31
        :param expiry_month: a string that represents a number from 1-12
        :param expiry_year: a string that represents a 4-digit year.
        :param kwargs: a dictionary of named arguments and values. This
        is to provide support in the event of multiple inheritance and
        complex super() MRO calls. Usually contains the attributes of
        other interfaces that have been implemented.
        """
        self.expiry_date = ExpiryDate(expiry_day, expiry_month, expiry_year)
        super().__init__(**kwargs)

    def validate_card(self) -> bool:
        """
        Validates a gift card. A gift card is valid if it has a
        balance ≥ 0 and not be expired and have a card_id hat begins
        with the letter 'G' and be followed by digits (eg: G123456).
        :return: True if valid, False otherwise
        """
        return super().validate_card() and not self.expiry_date.expired and \
            self.card_id[:1] == "G" and self.card_id[1:].isdigit()

    @classmethod
    def get_fields(cls) -> dict:
        """
        :return: Returns a dictionary of attributes and their string
        representations to allow a Menu class to dynamically initialize
        the class using kwargs.
        """
        fields = super().get_fields()
        fields["expiry_year"] = "Expiry Year"
        fields["expiry_month"] = "Expiry Month"
        fields["expiry_day"] = "Expiry Day"
        return fields

    def __str__(self):
        return f'{super().__str__()}\n' \
               f'{self.expiry_date}'
