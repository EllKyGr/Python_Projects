# Create a text based slot machine
from random import choice
from typing import Any
from time import sleep

MAX_LINES: int = 3
MIN_LINES: int = 1
MAX_BET: int = 100
MIN_BET: int = 5
REELS: int = 3
ROWS: int = 3

# 10 symbols in total per reel
SYMBOLS = {
    "cherry": {
        "unicode": "\U0001F352",
        "count": 1,
        "value": 2,
    },
    "tangerine": {
        "unicode": "\U0001F34A",
        "count": 1,
        "value": 2,
    },
    "lemon": {
        "unicode": "\U0001F34B",
        "count": 1,
        "value": 2,
    },
    "peach": {
        "unicode": "\U0001F351",
        "count": 1,
        "value": 2,
    },
    "grapes": {
        "unicode": "\U0001F347",
        "count": 1,
        "value": 2,
    },
    "watermelon": {
        "unicode": "\U0001F349",
        "count": 1,
        "value": 2,
    },
    "bell": {
        "unicode": "\U0001F514",
        "count": 1,
        "value": 3,
    },
    "seven": {
        "unicode": "7\uFE0F\u20E3 ",
        "count": 1,
        "value": 4,
    },
    "cash": {
        "unicode": "\U0001F4B0",
        "count": 1,
        "value": 5,
    },
    "diamond": {
        "unicode": "\U0001F48E",
        "count": 1,
        "value": 6,
    },
}


def initial_deposit() -> int:
    """
    The starting funds in order to play.

    :return: the monetary value needed to play the game.
    :rtype: int
    """
    while True:
        deposit: Any = input("Enter money: ")
        if not deposit.isdigit():
            print("Invalid entry.")
            continue
        deposit = int(deposit)
        if deposit >= 100:
            break
        else:
            print("Initial deposit must be at least $100.00")

    print(f"You have ${deposit} in your account.")

    return deposit


def set_bet(funds: int, lines: int) -> list[int]:
    """
    Set the amount of money the user is willing to bet.

    :param funds: current credit of user
    :type lines: int
    :param funds: number of lines bet on by user
    :type lines: int
    :return: the bet and remaining funds.
    :rtype: list[int]
    """
    while True:  # Save the first bet value if you don't want to change it
        bet: Any = input("How much would you want to bet on each line? ")
        if not bet.isdigit():
            print("Invalid entry.")
            continue
        bet = int(bet)
        # Rigged amount of bet per line
        if MIN_BET <= bet <= MAX_BET:
            total_bet: int = lines * bet
            if total_bet > funds:
                print(f"Insufficient funds for bet.\nCurrent funds: ${funds}")
                continue
            break
        else:
            print(f"Bet must be between ${MIN_BET} - ${MAX_BET}")

    funds -= total_bet

    print(f"You're bet is ${bet} in {lines} lines.\nTotal bet ${total_bet}\n")

    return [total_bet, funds]


def predefined_symbols(symbols: dict, reels: int, rows: int) -> list[list]:
    """
    Random generated matrix composed of three reels containing the slot symbols

    :param symbols: associated symbol with its unicode representation, count
                    and value
    :type symbols: dict[str, dict]
    :param reels: constant value of total reels
    :type reels: int
    :param rows: constant value of total rows
    :type rows: int
    :return: matrix containing the reels
    :rtype: list[list]
    :example:
    >>> [['🍉', '🍋', '🍊'], ['🔔', '🍊', '🍒'], ['🍒', '🍑', '🔔']]
    """
    total_reels: list[list] = []
    list_of_symbols: list[str] = []
    for sym in symbols.values():
        list_of_symbols.append(sym["unicode"])
    for _ in range(reels):
        inner_reel: list = []
        current_list_of_symbols: list[str] = list_of_symbols[:]
        for _ in range(rows):
            symbol: str = choice(current_list_of_symbols)
            current_list_of_symbols.remove(symbol)
            inner_reel.append(symbol)

        total_reels.append(inner_reel)

    return total_reels


def output_spin(spin: list[list]) -> None:
    """
    Visual representation of the spin after users action

    :param spin: matrix representing the three reels from the slot machine
    :type spin: list[list]
    :return: None
    :example:
    >>> \n
        🍉 | 🔔 | 🍒\n
        🍋 | 🍊 | 🍑\n
        🍊 | 🍒 | 🔔
    """
    for reel in range(len(spin)):
        for idx, value in enumerate(spin):
            if idx != len(spin) - 1:
                print(value[reel], end=" | ")
            else:
                print(value[reel], end="")
            sleep(0.07)

        print()


def pull_lever() -> list[list]:
    """
    A "spin" takes place generating three different reels with random symbols

    :return: the random values for every slot
    :rtype: list[str]
    """
    while True:
        pull: str = input("Pull the lever! (Enter) \n")
        if pull != "":
            continue
        reel_outcome: list[list] = predefined_symbols(SYMBOLS, REELS, ROWS)
        output_spin(reel_outcome)
        print()
        break

    return reel_outcome


def jackpot(all_reels: list[list], bet: int, lines: int) -> list:
    """
    Assess the combinations from the spin in order to return, if any, earnings.

    :param all_reels: a group of three random generated reels inside a matrix
    :type all_reels: list[list]
    :param bet: the users bet
    :type bet: int
    :param lines: lines selected by the user upon which the bet takes place
    :type lines: int
    :return: the total earnings after the spin
    :rtype: int
    """
    winning_lines: list = []
    earnings: int = 0
    # Since bet is based on lines, it will only iterate accordingly
    for line in range(lines):
        # Based on the first reel compare to the following reel, same position,
        # (idx 0, 1, 2) if it is the same symbol. Break if not
        symbol: str = all_reels[0][line]
        for reel in all_reels:
            symbol_to_check: str = reel[line]
            if symbol != symbol_to_check:
                break
        else:
            earnings += bet * multiplier_bonus(symbol)
            winning_lines.append(line)

    print("Jackpot!" if earnings > 0 else "Not a chance!")

    return [earnings, winning_lines]


def bet_or_cash(funds: int) -> int:
    """
    Gives the option for the user to keep gambling or cash out as long as the
    user still has funds.

    :param funds: current funds from the user
    :type fund: int
    :return: modified funds value
    :rtype: int
    """
    while True:
        if funds == 0:
            print("Game over!")
            break
        choice: str = input("Play or quit [P/Q] ").lower()
        if choice == "q":
            break
        elif choice == "p":
            lines: int = get_number_lines()
            bet, current_funds = set_bet(funds, lines)
            new_funds, w_lines = jackpot(pull_lever(), bet, lines)
            funds = current_funds + new_funds
            print(f"You're new funds are ${funds}.")
            print("You won on lines", *w_lines)
        else:
            continue
    return funds


def start_game() -> None:
    """
    Initializes the game by stating the base funding and outputs the final
    earnings if any.

    :return: None
    :rtype: NoneType
    """
    print("Starting Jackpot")
    # Ask once for the initial balance
    funds: int = initial_deposit()
    earnings: int = bet_or_cash(funds)
    if earnings > 0:
        print(f"You're final funds are ${earnings}")
    else:
        print("You ran out of funds, best of luck next time!")


def main() -> None:
    start_game()


if __name__ == "__main__":
    main()
