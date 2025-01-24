"""A classic tick tack toe program
"""
from random import choice

CIRCLE: str = "O"
EX: str = "X"
# From 0 to 8, ordered as the numeric keypad
BOARD: dict[int, str] = {
    6: '',
    7: '',
    8: '',
    3: '',
    4: '',
    5: '',
    0: '',
    1: '',
    2: ''
}
# Vertical, horizontal, diagonal cases in order to meet victory conditions
COMBINATION_SLOTS: dict[int, list[int]] = {
    0: [0, 1, 2],  # Lower horizontal
    1: [3, 4, 5],  # Middle horizontal
    2: [6, 7, 8],  # Upper horizontal
    3: [0, 3, 6],  # Left vertical
    4: [1, 4, 7],  # Middle vertical
    5: [2, 5, 8],  # Right vertical
    6: [0, 4, 8],  # Diagonal right to left
    7: [2, 4, 6],  # Diagonal left to right
}


def output_board(board: dict[int, str]):
    """
    Visual board representation

    :param board: data structure representing every slot, empty or not
    :type board: dict[int, str]
    """
    count: int = 0
    jump: tuple[int, int] = (3, 6)
    for slot in board.values():
        if slot != '':
            print(f"|{slot}|", end=" ")
        else:
            print("| |", end=" ")

        count += 1
        if count in jump:
            print()
    print()


def assess_combination(board: dict[int, str],
                       symbol: str) -> tuple[bool, str | None]:
    """
    Assess victory condition

    :param board: data structure representing every slot, empty or not
    :type board: dict[int, str]
    :param symbol: 'X' or 'O'
    :type: str
    :return: True and symbol representing the player, or None, depending if
             the three in a row pattern was met
    :rtype: tuple[bool, str | None]
    """
    players: dict[str, int] = {EX: 0, CIRCLE: 0}
    got_winner: bool = False
    winner: str | None = None

    for combination in COMBINATION_SLOTS.values():
        for slot, sym in board.items():
            if slot not in combination or sym == '':
                continue
            if slot in combination and sym == EX:
                players[EX] += 1
            elif slot in combination and sym == CIRCLE:
                players[CIRCLE] += 1

        if players[symbol] == 3:
            got_winner = True
            winner = symbol
            break

        players[EX] = 0
        players[CIRCLE] = 0

    return got_winner, winner


def player_turn(move: int, symbol: str, board: dict[int, str],
                free_slots: list[int], taken_slots: list[int]) -> str | None:
    """
    Registers player slot choice and verifies if there's a winner after it

    :param move: user or pc slot choice
    :type move: int
    :param symbol: 'X' or 'O'
    :type symbol: str
    :param board: data structure representing every slot, empty or not
    :type board: dict[int, str]
    :param free_slots: available spaces after every turn
    :type free_slots: list[int]
    :param taken_slots: slots taken from previous variable
    :type taken_slots: list[int]
    :return: winner's symbol or None
    :rtype: str | None
    """
    board[move] = symbol
    free_slots.remove(move)
    taken_slots.append(move)

    got_winner, winner = assess_combination(board, symbol)

    if got_winner is True:
        return winner

    return None


def tick_tack_toe() -> None:
    """
    Flow control for the game. Sets from the beginning each symbol for both
    players and who starts the game. After every player turn evaluates if, with
    the current slots occupied, there is a winner.
    """
    first_player: str = EX if input("Choose 'X' or 'O' ") == EX else CIRCLE
    second_player: str = CIRCLE if first_player == EX else EX
    turn: str = '1' if input("Who goes first? [X/O] ") == first_player else '2'

    current_board: dict[int, str] = BOARD.copy()
    free_slots: list[int] = list(range(9))
    occupied_slots: list[int] = []
    user_turn, pc_turn = None, None

    while len(free_slots) > 0:
        if turn == '1':
            move: int = int(input("Make move: ")) - 1
            if move in occupied_slots:
                print("Slot already covered. Choose another.")
                continue
            if move not in free_slots:
                print('No such slot available')
                continue
            user_turn = player_turn(move, first_player, current_board,
                                    free_slots, occupied_slots)
            turn = '2'
        elif turn == '2':
            print('Second player move')
            pc_turn = player_turn(choice(free_slots), second_player,
                                  current_board, free_slots, occupied_slots)
            turn = '1'

        output_board(current_board)

        if not user_turn is None or not pc_turn is None:
            print(
                f"The winner is {user_turn if not user_turn is None else pc_turn}"
            )
            break
    else:
        print("Draw")


def main() -> None:
    """
    Runs the program 'n' number of times
    """
    while True:
        try:
            matches: int = int(input("How many matches? "))
            break
        except ValueError:
            print("Only enter positive integers!")
            continue
    for _ in range(matches):
        tick_tack_toe()


if __name__ == '__main__':
    main()
