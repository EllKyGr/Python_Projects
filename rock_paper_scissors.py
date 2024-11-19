import random as ra


def choice_comparison(u_choice: str, pc_choice: str, options: list) -> bool:
    """
    Compares pc and player elections

    :param u_choice: User's choice
    :type u_choice: str
    :param pc_choice: random choice made by the program
    :type pc_choice: str
    :param options: the three possible choices
    :type options: list
    """
    if ((u_choice == options[0] and pc_choice == options[1]) or
            (u_choice == options[1] and pc_choice == options[2]) or
            (u_choice == options[2] and pc_choice == options[0])):
        return True
    else:
        return False


def match() -> list[int]:
    """
    Game execution

    :return: The score of both players
    :rtype: list[int]
    """
    user_victories: int = 0
    pc_victories: int = 0
    pc_choice: str | None = None
    options: list[str] = ["rock", "paper", "scissors"]
    while True:
        users_choice: str = input("Rock, paper, scissors! ").lower()
        if users_choice == 'q':
            break
        elif users_choice not in options:
            print("Invalid entry.")
            continue
        # pc_choice = choice(ra.randint(0, 2))
        pc_choice = options[ra.randint(0, 2)]
        print(pc_choice)

        if users_choice == pc_choice:
            print("Draw!")
        elif choice_comparison(users_choice, pc_choice, options):
            print("PC wins!")
            pc_victories += 1
        else:
            print("User wins!")
            user_victories += 1

    results: list[int] = [pc_victories, user_victories]

    return results


def main() -> None:
    print("Enter q to end the game")
    final_score = match()
    print(f"Final score\nPC: {final_score[0]}\nUser: {final_score[1]}")


if __name__ == "__main__":
    main()
