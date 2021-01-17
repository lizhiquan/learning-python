"""
Lab 4 code. Simulate a card manager application to demonstrate multiple
inheritance. Classes contained:
- CardManager
- CardMenu
"""
from task2_cards import Card
from task2_cards import IDCard
from task2_cards import TransitCard
from task2_cards import GiftCard


class CardManager:
    """
    The CardManager class maintains a dictionary of cards (Referenced via
    their respective Card ID's). The class provides an interface to:
    - add a card
    - remove a card
    - find a card
    - validate all cards
    """

    def __init__(self):
        self.wallet_cards = {}

    def add_card(self, card: Card) -> bool:
        """
        Add a card to the dictionary of cards maintained if a card with the
        same id does not exist already.
        :param card: A Card Object
        :prerequisite: card must have a unique card id.
        :return: True, if card was added, False otherwise
        """
        if card.card_id not in self.wallet_cards:
            self.wallet_cards[card.card_id] = card
            return True
        return False

    def remove_card(self, card_id: str) -> bool:
        """
        Remove the card with the specified id from this CardManager
        instance.
        :param card_id: a string, the card id of the card to be removed
        :return: True, if card was removed, False if not found
        """
        if card_id in self.wallet_cards:
            del self.wallet_cards[card_id]
            return True
        return False

    def find_card(self, card_id: str) -> Card:
        """
        Find and return a reference to the Card object that has the card
        id specified.
        :param card_id: a string, the card id of the card that is being
        searched for.
        :return: The Card object if found, None otherwise.
        """
        return self.wallet_cards.get(card_id, None)

    def validate_cards(self):
        """
        Iterates through each card in the card dictionary and validates the
        card.
        :return: a list of tuples, where each tuple is of the format
        (card_id: str, valid_status: bool)
        """
        results = []
        for card in self.wallet_cards.values():
            results.append((card.card_id, card.validate_card()))
        return results

    def __str__(self):
        formatted_str = "----- Card Manager -----"
        for card in self.wallet_cards.values():
            formatted_str = f"{formatted_str}\n" \
                            f"--- Card: {card.card_id} ---\n" \
                            f"{card}"
        return formatted_str


class CardMenu:
    """
    The menu driver that controls the card management application.
    Responsible for querying the user for input and passing the flow of
    control to the right class based on user input.

    To add support for other derived card types, add an extra entry to the
    card_type_menu dictionary for each derived card type in the __init__()
    method.
    """

    def __init__(self, card_manager: CardManager):
        self.card_type_menu = {
            1: (IDCard, "ID Card"),
            2: (TransitCard, "Transit Card"),
            3: (GiftCard, "Gift Card"),
            4: (None, "Back")
        }
        self.card_manager = card_manager

    def prompt_card_type_menu(self):
        """
        Display the list of card types supported and prompt the user to
        make a choice amongst them.
        :return: The class that represents the card type picked,
        None otherwise.
        """
        user_choice = None
        while user_choice not in self.card_type_menu:
            for key, value in self.card_type_menu.items():
                print(f"{key}: {value[1]}")
            user_choice = int(input("Enter your choice:"))
            if user_choice not in self.card_type_menu:
                print("Invalid choice")
                continue
        return self.card_type_menu[user_choice][0]

    def add_card_prompts(self):
        """
        Prompt the user to enter card details and add the card to the
        CardManager.
        """
        print("Select the card type that you wish to add.")
        card_type = self.prompt_card_type_menu()
        fields = card_type.get_fields()
        input_data = {}
        print("Enter the following data:")
        for key, value in fields.items():
            data = input(f"{value}: ")
            input_data[key] = data
        card = card_type(**input_data)
        if self.card_manager.add_card(card):
            print("")
            print("-"*5, "Card Added!", "-"*5)
            print(card)
            print("-"*15)
        else:
            print("Card with same id already exists!")

    def remove_card_prompts(self):
        """
        Prompt the user for the card id and  attempt to remove it from the
        CardManager.
        """
        card_id = input("Enter the Card ID of the card you wish to "
                        "remove: ")
        card_removed = self.card_manager.remove_card(card_id)
        if card_removed:
            print(f"Card: {card_id} removed successfully!")
        else:
            print(f"Card: {card_id} cannot be removed, card not found.")


    def find_card_prompts(self):
        """
        Prompt the user for a card id and attempt to find the card with the
        matching id in the CardManager.
        :return:
        """
        card_id = input("Enter the Card ID of the card you wish to "
                        "find: ")
        result = self.card_manager.find_card(card_id)
        print("-" * 5, "Result", "-" * 5)
        if result:
            print(result)
        else:
            print(f"Card {card_id} not found!")

    def execute_menu(self):
        """
        Drive the program by displaying the main menu, prompt the user
        for a choice and execute the appropriate behavior based on the
        choice.
        """
        user_choice = None
        while user_choice != 6:
            print("\n")
            print("-"* 15)
            print("Lab 6 Menu")
            print("-"* 15)
            print("1. Add a card")
            print("2. Remove a card")
            print("3. Validate cards")
            print("4. Find a card")
            print("5. View all cards")
            print("6. Exit")
            user_choice = int(input("Enter your choice:"))
            if not 1 <= user_choice <= 6:
                print("Invalid choice")
                continue

            if user_choice == 1:
                self.add_card_prompts()
            elif user_choice == 2:
                self.remove_card_prompts()
            elif user_choice == 3:
                results = self.card_manager.validate_cards()
                for card_id, is_valid in results:
                    print(f"Card ID: {card_id}, Valid: {is_valid}")
            elif user_choice == 4:
                self.find_card_prompts()
            elif user_choice == 5:
                print(self.card_manager)
            elif user_choice == 6:
                print("Bye!")


def main():
    card_manager = CardManager()
    menu = CardMenu(card_manager)
    menu.execute_menu()


if __name__ == '__main__':
    main()
