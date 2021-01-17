"""
This module contains all the logic of the game Rock Paper Scissor Python
Spock.
"""
from enum import IntEnum
from random import choice


class Choice(IntEnum):
    """
    Represents a player choice.
    """
    ROCK = 0
    PAPER = 1
    SCISSORS = 2
    PYTHON = 3
    SPOCK = 4


defeat_choices_mapper = {
    Choice.ROCK: [Choice.SCISSORS, Choice.PYTHON],
    Choice.PAPER: [Choice.ROCK, Choice.SPOCK],
    Choice.SCISSORS: [Choice.PAPER, Choice.PYTHON],
    Choice.PYTHON: [Choice.SPOCK, Choice.PAPER],
    Choice.SPOCK: [Choice.SCISSORS, Choice.ROCK]
}


def random_choice() -> Choice:
    """
    Returns a random choice in the Choice enum structure.
    :return: a Choice enum
    """
    return choice(list(Choice))


def simulate_game(p1: str, p2: str) -> str:
    """
    Simulates a game by randomizing the choices for player 1 and player
    2, then returns the winner for this game.
    :param p1: a str, the name of player 1
    :param p2: a str, the name of player 2
    :return: a str, the winner of the game
    """
    while True:
        p1_choice = random_choice()
        p2_choice = random_choice()

        # Tie, again!
        if p1_choice == p2_choice:
            continue

        # We have a clear winner here
        if p2_choice in defeat_choices_mapper[p1_choice]:
            return p1
        else:
            return p2
