# Player roll a die adding every outcome to its score. First one reaches a
# limit, i.e., 50 win. If any one gets a 1 score is lowered to 0. Player choose
# when to stop the strike unless getting a one.
import random as ra
from typing import Any


def roll() -> int:
    """
    Emulates the roll of a dice

    :return: Random value from 1 to 6
    :rtype: int
    """
    min, max = 1, 6
    dice: int = ra.randint(min, max)
    return dice


def player_name() -> str:
    """
    Assigns name to each player

    :return: Players name
    :rtype: str
    """
    name: str = input("Enter player name: ").title()
    return name


def player_rolls(player: str, current_score: int) -> int:
    """
    User 'rolls' the dice until reaches a score of '50', presses 'q'
    or gets a '1'

    :param player: Name of the player
    :type player: str
    :param current_score: The local score value subjected to change
    :type current_score: int
    :return: Final score based on rolls
    :rtype: int
    """
    strike: int = 0
    while True:
        if (current_score + strike) >= 50:
            # print("Reached!")
            break
        choice: str = input(f"{player} rolls! ").lower()
        if choice == "":
            dice: int = roll()
            print(player, "got:", dice, end=" ")
            if dice > 1:
                strike += dice
                print(strike)
            else:
                strike = 0
                print(strike)
                break
        elif choice == "q":
            print(player, "goes out")
            break
        else:
            print("Invalid entry")

    current_score += strike
    print(player + "'s new score:", current_score)

    return current_score


def turn_based(players: dict, turn: int) -> str:
    """
    Defines who starts rolling and returns player with the highest score

    :param players: Dictionary containing number of player as key (upto 4),
                    with name and base score as values
    :type players: dict
    :param turn: determines which player starts rolling
    :type turn: int
    :return: Player with highest score
    :rtype: str
    """
    winner: Any = None
    active: bool = True
    while active:
        # Verifies until there's a winner
        for items in players.values():
            if items[1] >= 50:
                winner = items[0]
                active = False

        # Runs as many players are
        for _ in range(len(players)):
            players[turn][1] = player_rolls(players[turn][0], players[turn][1])
            # Equality of both values restart the turn for further rounds
            if turn == len(players):
                turn = 1
            else:
                turn += 1

    return winner


def start_the_game() -> None:
    """
    Initializes the game by asking the players name and outputs the winner
    """
    players: dict = {}
    while True:
        n_players: str = input("Enter number of players (2-4): ")
        if not n_players.isdigit():
            print("Enter only numbers.")
            continue
        if 2 <= int(n_players) <= 4:
            for n in range(int(n_players)):
                name: str = player_name()
                score: int = 0
                players[n + 1] = [name, score]
            break
        else:
            print("Invalid number of players.")

    turn: int = ra.randint(1, len(players))

    print("Press 'enter' to roll or 'q' to end the bet.")
    winner: str = turn_based(players, turn)
    print("The winner is", winner + "!")


def main() -> None:
    start_the_game()


if __name__ == "__main__":
    main()
