# Ask a question, don't allow to pass if answer incorrect, calculate how long
# it takes to answer it
import random as ra  # for operands
import time

# Constants
OPERATORS = ["+", "-", "*"]
MIN_OPERAND = 3
MAX_OPERAND = 12
TOTAL_PROBLEMS = 10


def generate_problem() -> tuple:
    """Generates a random expression for the user

    Returns:
        tuple: contains the random expression with its answer.
    """
    left = ra.randint(MIN_OPERAND, MAX_OPERAND)
    right = ra.randint(MIN_OPERAND, MAX_OPERAND)
    operator = ra.choice(OPERATORS)

    expression = str(left) + " " + operator + " " + str(right)
    # print(expression)  # num operator num => 4 - 9
    answer = eval(expression)  # Evaluates as Python expression, using a string

    return expression, answer


def test() -> int:
    """Executes the test

    Returns:
        int: total score of user.
    """
    score: int = 0
    for n in range(TOTAL_PROBLEMS):
        expr, result = generate_problem()
        while True:
            answer = input(f"Problem #{n + 1}\n{expr} = ")
        # if answer is converted to int but wrong input is given the program
        # will crash. Since input is already a string compared with the result
        # as a string, by not been the same it will just keep asking the right
        # answer
            if answer == str(result):
                score += 1
                break
            else:
                continue

    return score


def start_program(t_problems: int) -> None:
    """Initialize the program

    Args:
        t_problems (int): Total number of problems which conforms the test
    Returns:
        NoneType: None
    """
    print("-" * 80)
    start_test: int = int(time.time())
    score: int = test()
    finish_test: int = int(time.time())
    print("-" * 80)
    total_time: int = finish_test - start_test
    print(f"You finish the test in {total_time} seconds\n"
          f"You're final score is:", (score * 100 / t_problems))


def main() -> None:
    input("Press enter to start")
    start_program(TOTAL_PROBLEMS)


if __name__ == "__main__":
    main()
