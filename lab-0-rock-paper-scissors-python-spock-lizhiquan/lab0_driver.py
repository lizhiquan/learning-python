"""
This module serves as the starting point of the program, including code
that interacts with the user and prints to the console.
"""
from game import simulate_game


def simulate_tournament(p1: str, p2: str, num_rounds: int) -> str:
    """
    Simulates a tournament between player 1 and player 2 with a given
    number of rounds and returns the winner's name.
    :param p1: a str, the name of player 1
    :param p2: a str, the name of player 2
    :param num_rounds: an int, a number of rounds, must be > 0 and odd
    :return: a str, the name of the winner
    """
    # Number of win games
    p1_win_count = 0
    p2_win_count = 0
    # Start the tournament
    for i in range(num_rounds):
        winner = simulate_game(p1, p2)
        print(f'Round {i + 1}: Player {winner} won!')
        if winner == p1:
            p1_win_count += 1
        else:
            p2_win_count += 1
    # Compare the final result and return the winner
    if p1_win_count > p2_win_count:
        return p1
    else:
        return p2


def print_game_menu() -> int:
    """
    Prints the game menu and gets user's selection.
    :return: an int, the selected option from the user
    """
    print('Please select a tournament mode:')
    print('1. Best of 3')
    print('2. Best of 5')
    print('3. Best of 7')
    print('4. Quit')
    return int(input('Your selection: '))


def print_tournament_history(data: list):
    """
    Prints the tournament history to the console.
    :param data: a list, contains tuples of winner name and number of
                 rounds
    """
    print("\nTournament logs:")
    for i, (winner, num_rounds) in enumerate(data):
        print(f'{i + 1}. {winner} is the winner of {num_rounds} rounds')


def main():
    """
    Welcomes players, gets inputs and drives the game.
    """
    print('Welcome to the Game Rock Paper Scissors Python or Spock!')
    p1 = input('Enter the name of player 1: ')
    p2 = input('Enter the name of player 2: ')
    tournament_history = []

    while True:
        mode = print_game_menu()
        if mode == 1:
            num_rounds = 3
        elif mode == 2:
            num_rounds = 5
        elif mode == 3:
            num_rounds = 7
        else:
            break
        winner = simulate_tournament(p1, p2, num_rounds)
        print(f'Player {winner} is the winner of this game!', end='\n\n')
        tournament_history.append((winner, num_rounds))

    if len(tournament_history) > 0:
        print_tournament_history(tournament_history)
    print('Bye!~')


if __name__ == '__main__':
    main()
