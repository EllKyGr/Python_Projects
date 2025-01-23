"""Creates random passwords based on user desired length, numbers
and special characters"""

from string import ascii_letters, digits, punctuation
from random import choice, shuffle

ALL_LETTERS: list[str] = list(ascii_letters)
NUMBERS: list[str] = list(digits)
SPECIAL_CHARS: list[str] = list(punctuation)


def pass_gen(length: int, numbers: bool = True, special: bool = True) -> str:
    """
    Generates password

    :param length: desired size for password
    :type length: int
    :param numbers: default True, False if user won't require numbers
    :type numbers: bool
    :param special: default True, False if user won't require special characters
    :type special: bool
    :return: random password
    :rtype: str
    """
    characters: list[str] = []
    while len(characters) < length:
        shuffle(ALL_LETTERS)
        characters.append(choice(ALL_LETTERS))
        if numbers:
            shuffle(NUMBERS)
            characters.append(choice(NUMBERS))
        if special:
            shuffle(SPECIAL_CHARS)
            characters.append(choice(SPECIAL_CHARS))

    shuffle(characters)
    password: str = ''.join(reversed(''.join(characters)))

    return password


def user_requirements() -> None:
    """
    Asks for password requirements
    """
    options: tuple[str, str] = ('Y', 'N')
    while True:
        length: str = input("Enter length of password: ")
        if not length.isdigit():
            print("Enter a positive integer!")
            continue

        numbers: str | bool = input("Add numbers [Y/N]: ")
        if numbers in options:
            numbers = numbers == 'Y'
        else:
            continue

        special: str | bool = input("Add special characters [Y/N]: ")
        if special in options:
            special = special == 'Y'
        else:
            continue

        break

    print(pass_gen(int(length), numbers, special))


def main():
    """Run main function"""
    user_requirements()


if __name__ == '__main__':
    main()
