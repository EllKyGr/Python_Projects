from typing import Any
from random import randint

# Program that allows the user to bet money by:
# - Making a deposit
# - Make a bet, i.e., match one, two or three of the slots
# - Spin wheel
# - Asses the results
# - If there's a match the multiply the current value by x
# - if no match the bet is loss and whatever amount was, reduced it from total
# - User then can choose to play again or withdraw
# - If user looses all the money the game ends


def initial_deposit() -> int:
    """
    The starting funds for the game.

    :return: the monetary value needed to play the game.
    :rtype: int
    """
    while True:
        deposit: Any = input("Enter money: ")
        if not deposit.isdigit():
            print("Invalid entry.")
            continue
        deposit = int(deposit)
        if deposit > 100:
            break
        else:
            print("Initial deposit must be at least $100.00")

    print(f"You have ${deposit} in your account.")

    return deposit


def set_bet(deposit: int) -> list[int]:
    """
    Set the amount of money the user is willing to bet.

    :return: the bet and remaining quantity from the original funds.
    :rtype: list[int]
    """
    while True:
        bet: Any = input("How much would you want to bet? ")
        if not bet.isdigit():
            print("Invalid entry.")
            continue
        bet = int(bet)
        deposit -= bet
        break

    print(f"You're bet is ${bet}")

    return [bet, deposit]


def user_choices() -> list[str]:
    """
    Users input for the bet comparison. Might me removed at the end.

    :return: slot values selected by the user 1, 2 or 3.
    :rtype: list[str]
    """
    # Which symbols (3?) per slot (3 too), i.e., 1-1-1 or 3-1-3
    user_bet: list[str] = []
    count: int = 0
    while count < 3:
        slot: str = input(f"Slot number {count + 1}: ")
        if slot not in ["1", "2", "3"]:
            print("Invalid")
            continue
        user_bet.append(slot)
        count += 1

    return user_bet


def pull_lever() -> list[str]:
    """
    Generates a random combination in comparison to the user selection. This
    might be take solely place with previous function.

    :return: the random values for every slot
    :rtype: list[str]
    """
    options: list[str] = ["1", "2", "3"]
    pc_bet: list[str] = []
    while True:
        pull: str = input("Pull the lever! (Enter) ")
        if pull != "":
            continue
        # Make the machine output a value in order to compare with user choice
        for _ in range(3):
            outcome: int = randint(int(min(options)), int(max(options)))
            pc_bet.append(str(outcome))
        break

    print(f"{pc_bet[0]} | {pc_bet[1]} | {pc_bet[2]}")

    return pc_bet


def jackpot(bet: int, deposit: int) -> int:
    """
    Compares user input with the random generated options in order to determine
    specific earnings based on matching slots. If all slots match the earnings
    are doubled; first and third matches gives one and half, anything else
    yields no earnings.

    :param bet: users bet
    :type bet: int
    :param deposit: current funds from user
    :type deposit: int
    :return: new value from deposit
    :rtype: int
    """
    # Which combinations are the winner ones?
    # All the same -> 2x times earnings => bet of 100 returns 200
    # First and third -> 1.5x times earnings => bet of 100 returns 150
    # Anything else -> 0 earnings => bet of 100 returns nothing
    user_bet, pc_bet = user_choices(), pull_lever()
    if user_bet == pc_bet:
        print("Winner!")
        bet *= 2
    elif user_bet[0] == pc_bet[0] and user_bet[2] == pc_bet[2]:
        print("Winner!")
        bet = round(bet * 1.5)
    else:
        print("Looser!")
        bet = 0

    deposit += bet
    return deposit


def bet_or_cash(funds: int) -> int:
    """
    Gives the option for the user to keep gambling or cash out as long as the
    user still has funds.

    :param funds: current funds from the user
    :type fund: int
    :return: modified funds value
    :rtype: int
    """
    # It will only ask once for the initial funding, said value is later used
    # for the rest of the gambling experience
    while True:
        if funds == 0:
            print("Game over!")
            break
        choice: str = input("Play or quit [P/Q] ").lower()
        if choice == "q":
            break
        elif choice == "p":
            bet, deposit = set_bet(funds)
            new_funds: int = jackpot(bet, deposit)
            funds = new_funds
            print(f"You're new funds are ${funds}")
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
    funds: int = initial_deposit()
    earnings: int = bet_or_cash(funds)
    if earnings > 0:
        print(f"You're final earnings are ${earnings}")
    else:
        print("You ran out of funds, best of luck next time!")


def main() -> None:
    start_game()


if __name__ == "__main__":
    main()
