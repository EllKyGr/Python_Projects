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


def max_time_measure(hour: int = 0, minute: int = 0, second: int = 0) -> bool:
    """
    Prevents user to enter invalid time values

    :param hour: User entry value
    :type hour: int
    :param minute: User entry value
    :type minute: int
    :param second: User entry value
    :type second: int
    :return: True | False
    :rtype: bool
    """
    if hour > HR_LIMIT:
        return False
    if minute > MIN_LIMIT:
        return False
    if second > SEC_LIMIT:
        return False

    return True


def set_hours():
    """
    Return hours and lesser time values if applicable

    :return: List containing user entered values
    :rtype: list[int]
    """
    while True:
        user_hours = input("How many hours: ")
        if not user_hours.isdigit():
            print("Invalid. Only enter numbers!")
            continue
        if max_time_measure(hour=int(user_hours)) is False:
            print("Timer cannot be set higher than 24 hrs!")
            continue
        hours, minutes, seconds = set_minutes()
        hours = int(user_hours)
        break

    return [hours, minutes, seconds]


def set_minutes():
    """
    Return minutes and seconds. Hour value is set 0 by default.

    :return: List containing user entered values
    :rtype: list[int]
    """
    while True:
        user_minutes = input("How many minutes: ")
        if not user_minutes.isdigit():
            print("Invalid. Only enter numbers!")
            continue
        if max_time_measure(minute=int(user_minutes)) is False:
            print("Value exceed max number of minutes!")
            continue
        hours, minutes, seconds = set_seconds()
        minutes = int(user_minutes)
        break

    return [hours, minutes, seconds]


def set_seconds():
    """
    Return seconds. Hour and minutes values are set '0' by default.

    :return: List containing user entered values
    :rtype: list[int]
    """
    while True:
        user_seconds = input("How many seconds: ")
        if not user_seconds.isdigit():
            print("Invalid. Only enter numbers!")
            continue
        if max_time_measure(minute=int(user_seconds)) is False:
            print("Value exceed max number of seconds!")
            continue
        seconds = int(user_seconds)
        break

    return [0, 0, seconds]


def set_time_values() -> list[int]:
    """
    Ask and arrange user required time lapse

    :return: list containing time values for every field
    :rtype: list[int]
    """
    user_input: str | None = None
    timer: list[int] = [0, 0, 0]
    while True:
        user_input = input("Enter hours, minutes or seconds [H/M/S] ")
        if user_input == "H":
            timer = set_hours()
        elif user_input == "M":
            timer = set_minutes()
        elif user_input == "S":
            timer = set_seconds()
        else:
            print("Invalid command!")
            continue
        break

    return timer


def start_chronometer(user_set_time: list[int]):
    """
    Outputs initial timer before starting countdown

    :param user_set_time: return value from `set_time_values()`
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

    :param user_timer: return value from `set_time_values()`
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
    user_set_time: list[int] = set_time_values()
    start_chronometer(user_set_time)
    chronometer(user_set_time)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted!")

# print(LINE_UP, end=LINE_CLEAR)
