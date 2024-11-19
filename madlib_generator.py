from typing import Set


# fill the gaps in a story based in words given by the user
def file_content(file: str) -> list[str]:
    """
    Read the story from a file

    :param file: file holding the file
    :type file: str
    :return: a short story
    :rtype: list[str]
    """
    content: list = []
    with open(file) as fl:
        content = fl.read().split("\n")

    return content


def extract_placeholders(file: str) -> list:
    """
    Retrieves and stores the placeholders for later replacement with user input

    :param file: file holding the file
    :type file: str
    :return: list containing file content, placeholders and users choices
    :rtype: list[list, list, dict]
    """
    user_choices: dict[str, str] = {}
    placeholders: Set[str] = set()  # Reduces time iteration later
    content: list = file_content(file)
    for line in content:
        if line == '':
            continue
        words: list = line.split(" ")
        for word in words:
            # From every line of the file, extract the <placeholder>
            if word.startswith("<"):
                end_bracket: int = word.find(">")
                # Save the placeholder for later replacement
                placeholders.add(word[:end_bracket + 1])
                # For readability
                placeholder: str = word[1:end_bracket]
                if placeholder not in user_choices:  # Prevents overwriting
                    user_entry = input(f"Enter a {placeholder}: ")
                    user_choices[placeholder] = user_entry

    return [content, placeholders, user_choices]


def output_mad_lib(content: list, placeholders: list,
                   user_choices: dict) -> None:
    """
    Shows to the user the final story

    :param content: the file content
    :type content: list[str]
    :param placeholders: extracted from the file and surrounded by `<>`
    :type placeholder: list[str]
    :param user_choices: related users input to placeholders value
    :type user_choices: dict[str, str]
    """
    for line in content:
        if line == '':
            continue
        for ph in placeholders:
            # Straight forward access to users choice
            inside_bracket: str = ph[1:ph.find(">")]
            if ph not in line:
                continue
            line = line.replace(ph, user_choices[inside_bracket])
        # No need to substitute in file, preserving the original format
        print(line)


def main() -> None:
    content, placeholders, user_choices = extract_placeholders("story.txt")
    output_mad_lib(content, placeholders, user_choices)


if __name__ == "__main__":
    main()
