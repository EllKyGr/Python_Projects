"""A clock alarm that takes user input (how much time the clock will run) and
outputs dynamically time passing, i.e. replaces old time remaining with current
over printing as a list. It also provides sound cues.
"""

import time

LINE_UP: str = "\033[1A"
LINE_CLEAR: str = "\x1b[2K"
HR_LIMIT: int = 24
MIN_LIMIT: int = 59
SEC_LIMIT: int = 59


def check_unit(unit: str, value: int, timer: list[int]) -> bool | None:
    """
    Verifies if entered value by user do not exceed time limit

    :param unit: name of time unit
    :type unit: str
    :param value: numerical value entered by user
    :type value: int
    :param timer: list containing the time unit values
    :type timer: list[int]

    :return: True | None
    :rtype: bool | NoneType
    """
    valid: bool | None = None

    match unit:
        case 'hours':
            if value <= HR_LIMIT:
                timer.append(int(value))
                valid = True
        case 'minutes':
            if value <= MIN_LIMIT:
                timer.append(int(value))
                valid = True
        case 'seconds':
            if value <= SEC_LIMIT:
                timer.append(int(value))
                valid = True

    return valid


def register_valid_time(set_unit: str) -> list[int]:
    """
    Establish values for every field

    :param set_units: highest user entered time unit
    :type set_units: str
    :return: list containing default time units or entered by user
    :rtype: list[int]
    """
    measure: list[str] = ["hours", "minutes", "seconds"]
    timer: list[int] = []
    if set_unit == 'H':
        measure = measure[:]
    elif set_unit == 'M':
        measure = measure[1:]
        timer += [0]
    else:
        measure = measure[2:]
        timer += [0, 0]

    for unit in measure:
        while True:
            value = input(f"Enter {unit}: ")
            if not value.isdigit():
                print("Invalid. Only enter numbers!")
                continue
            if not check_unit(unit, int(value), timer) is True:
                print(f"Value exceed max number of {unit}!")
                continue
            break

    return timer


def set_time_lapse() -> list[int]:
    """
    Ask and arrange user required time lapse

    :return: list containing time values for every field
    :rtype: list[int]
    """
    user_input: str | None = None
    timer: list[int] = []
    while True:
        user_input = input("Enter hours, minutes or seconds [H/M/S] ")
        if user_input == "H":
            timer = register_valid_time('H')
        elif user_input == "M":
            timer = register_valid_time('M')
        elif user_input == "S":
            timer = register_valid_time('S')
        else:
            print("Invalid command!")
            continue
        break

    return timer


def start_chronometer(user_set_time: list[int]):
    """
    Outputs initial timer before starting countdown

    :param user_set_time: return value from `set_time_lapse()`
    :type user_set_time: list[int]
    """
    str_hour = "0" + str(user_set_time[0]) if user_set_time[0] < 10 else str(
        user_set_time[0])
    str_min = "0" + str(user_set_time[1]) if user_set_time[1] < 10 else str(
        user_set_time[1])
    str_sec = "0" + str(user_set_time[2]) if user_set_time[2] < 10 else str(
        user_set_time[2])

    for _ in range(2):
        print(f"\a{str_hour}:{str_min}:{str_sec}", end="\r")
        print(end=LINE_CLEAR)
        time.sleep(0.5)


def chronometer(user_timer: list[int]) -> None:
    """
    Outputs chronometer's countdown

    :param user_timer: return value from `set_time_lapse()`
    :type user_timer: list[int]
    """
    hours, minutes, seconds = user_timer
    while True:
        str_hour = "0" + str(hours) if hours < 10 else str(hours)
        str_min = "0" + str(minutes) if minutes < 10 else str(minutes)
        str_sec = "0" + str(seconds) if seconds < 10 else str(seconds)
        print(f"{str_hour}:{str_min}:{str_sec}", end="\r")
        print(end=LINE_CLEAR)
        time.sleep(1)
        # Ends chronometer
        if seconds == 0 and minutes == 0:
            if hours > 0:
                hours -= 1
                minutes = MIN_LIMIT + 1
            else:
                break

        if seconds > 0:
            seconds -= 1
        else:
            minutes -= 1 if minutes > 0 else 0
            seconds -= (-SEC_LIMIT) if minutes > -1 else 0

    for _ in range(3):
        print("\aTime's up!", end="\r")
        print(end=LINE_CLEAR)
        time.sleep(0.75)


def main() -> None:
    """
    Executes main functions
    """
    user_set_time: list[int] = set_time_lapse()
    start_chronometer(user_set_time)
    chronometer(user_set_time)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted!")
