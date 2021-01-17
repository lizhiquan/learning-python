from person import Person
from datetime import datetime
from cards import Card
from cards import CardGenerator


class Wallet:
    """
    This class is responsible for managing user's cards. It allows the
    user to add, remove, or search a card.
    """

    def __init__(self):
        """
        Initializes a Wallet object with an empty cards dictionary.
        """
        self.cards = {}

    def add_card(self, card: Card) -> None:
        """
        Stores the card to the cards dictionary.
        :return: None
        """
        self.cards[card.id_number] = card

    def remove_card(self, card_number) -> Card:
        """
        Searches the given card number and removes the card from the
        cards dictionary. Returns the instance of that card if it was
        found and removed. Returns None otherwise.
        :return: a Card if it was found and removed, None otherwise
        """
        return self.cards.pop(card_number, None)

    def search_card(self, card_number) -> Card:
        """
        Searches for the card from the cards dictionary. Returns the
        instance of that card if it was found. Returns None otherwise.
        :return: a Card if it was found, None otherwise
        """
        return self.cards.get(card_number, None)

    def __iter__(self):
        """
        Responsible for returning a new instance of an iterator. This
        allows for the use of the iter() function and the for loop
        syntax.
        :return: a CardIterator
        """
        return CardIterator(list(self.cards.values()))


class CardIterator:
    """
    An iterator which iterates over all the Card objects and returns the
    details and the validity of each card.
    """

    def __init__(self, cards: list):
        """
        Initializes the iterator with a reference to the cards.
        :param cards: a list of type Card
        """
        self.cards = cards
        self.current_index = 0

    def __next__(self) -> str:
        """
        Responsible for iterating to the next element in the iterable
        and returning that. If there are no more elements to iterate
        over, it raises the StopIteration error.
        :return: a str, if there are still cards to iterate over,
                 raise StopIteration otherwise.
        """
        if self.current_index == len(self.cards):
            raise StopIteration()
        card = self.cards[self.current_index]
        self.current_index += 1
        validity = datetime.now() < card.expiry_date
        return f"{card}\n" \
               f"Validity: {validity}"

    def __iter__(self):
        """
        Responsible for returning a new instance of an iterator. This
        allows for the use of the iter() function and the for loop
        syntax.
        :return: a CardIterator
        """
        return CardIterator(self.cards)


class Driver:
    """
    An object of type driver is responsible for running the Lab 2 Card
    Simulation program. It presents a list of menu options to the user
    that will let the user add, remove and search for cards in their
    wallet.
    """

    def __init__(self):
        """
        Initializes a Driver object.
        """
        self.person = None
        self.wallet = Wallet()

    def setup(self):
        """
        Initialize the Person attribute of this object. Prompts the user for
        the persons name and date of birth.
        """
        name = input("Enter the name of the individual who's cards will be "
                     "managed: ")
        dob_str = input("Enter the date of birth of the individual in the "
                        "format YYYY/MM/DD: ")
        dob_list = dob_str.split("/")
        dob = datetime(int(dob_list[0]), int(dob_list[1]), int(dob_list[2]))
        self.person = Person(name, dob)

    def get_menu_choice(self) -> int:
        """
        Presents the menu to the user, prompts and returns the choice.
        :return: an int, user's choice
        """
        print("Welcome to the Lab 2 Driver.")
        print("----------------------------")
        print("1. Add a card")
        print("2. Remove a card")
        print("3. Search for a card")
        print("4. Print all cards")
        print("5. Access a card")
        print("6. Exit")
        choice = int(input("Enter your choice (1-6): "))
        return choice

    def add_card(self) -> None:
        """
        Presents add card menu, creates a new card from user input and
        adds it to the wallet.
        :return: None
        """
        card = CardGenerator.execute_add_card_menu(self.person.name)
        self.wallet.add_card(card)
        print("A card was added successfully!")
        print(card, "\n")

    def remove_card(self) -> None:
        """
        Takes the ID number of a card as input from the user, searches
        and removes the card from the wallet and shows the result.
        :return: None
        """
        card_number = input("Enter card number to remove: ")
        card = self.wallet.remove_card(card_number)
        if card:
            print("The card was removed successfully!")
            print(card, "\n")
        else:
            print("Card not found!\n")

    def search_card(self) -> None:
        """
        Takes the ID number of a card as input from the user, searches
        for the card from the wallet and show the result.
        :return: None
        """
        card_number = input("Enter card number to search: ")
        card = self.wallet.search_card(card_number)
        if card:
            print(card, "\n")
        else:
            print("Card not found!\n")

    def print_cards(self) -> None:
        """
        Prints all cards in the wallet.
        :return: None
        """
        for cardInfo in self.wallet:
            print(cardInfo, "\n")

    def access_card(self) -> None:
        """
        Takes the ID number of a card as input from the user, searches
        for the card from the wallet and accessed it if exists.
        :return: None
        """
        card_number = input("Enter card number to access: ")
        card = self.wallet.search_card(card_number)
        if card:
            if card.access_card():
                print("Card was accessed successfully!\n")
            else:
                print("Failed to access the card!\n")
        else:
            print("Card not found!\n")

    def simulate(self) -> None:
        """
        Simulates the program by presenting the main menu and handles
        user's choice.
        :return: None
        """
        choice = -1
        while choice != 6:
            choice = self.get_menu_choice()
            if choice == 1:
                self.add_card()
            elif choice == 2:
                self.remove_card()
            elif choice == 3:
                self.search_card()
            elif choice == 4:
                self.print_cards()
            elif choice == 5:
                self.access_card()
            elif choice != 6:
                print("Invalid choice!\n")
        print("Exiting Program")


if __name__ == '__main__':
    driver = Driver()
    driver.setup()
    driver.simulate()
