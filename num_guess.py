import random as ra


def verify_number(entry: str) -> bool:
    return entry.isdigit()


def guess_num(top, num) -> None:
    print(f"I'm thinking of a number between 1 and {top}.", end=' ')
    while True:
        guess: str = input("Guess! ")

        if verify_number(guess):
            guess_int: int = int(guess)
            if guess_int == 0:
                print("Enter numbers above zero!")
                continue
        else:
            print("Only enter digits!")
            continue

        if guess_int == num:
            print("Good job!")
            break
        elif guess_int > num:
            print("To high!")
        else:
            print("To low!")


def main() -> None:
    while True:
        top = input("Enter top of the range: ")
        if verify_number(top):
            num = ra.randint(1, int(top))
            break
        else:
            print("Only enter positive digits!")
            continue

    guess_num(top, num)


if __name__ == "__main__":
    main()
