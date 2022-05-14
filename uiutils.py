"""
Author Names : Varun Sahni, Junyuan Chen
File Name: uiutils.py
Date and time completed: 2022-01-06 2:05
Assignment Name: Company Database Project
TODO: Create all of the functions that will act as utilities to enhance the user interface
"""

import error_testing


def red(text: str):
    """
    Format text in red

    Returns
        (str) - the red text
    """
    return f"\x1b[31m{text}\x1b[39m"


def green(text: str):
    """
    Format text in green

    Returns
        (str) - the green text
    """
    return f"\x1b[32m{text}\x1b[39m"


def yellow(text: str):
    """
    Format text in yellow

    Returns
        (str) - the yellow text
    """
    return f"\x1b[33m{text}\x1b[39m"


def blue(text: str):
    """
    Format text in blue

    Returns
        (str) - the blue text
    """
    return f"\x1b[34m{text}\x1b[39m"


def magenta(text: str):
    """
    Format text in magenta

    Returns
        (str) - the magenta text
    """
    return f"\x1b[35m{text}\x1b[39m"


def cyan(text: str):
    """
    Format text in cyan

    Returns
        (str) - the cyan text
    """
    return f"\x1b[36m{text}\x1b[39m"


def underline(text: str):
    """
    Underline text

    Returns
        (str) - the underlined text
    """
    return f"\x1b[4m{text}\x1b[24m"


def strikethrough(text: str):
    """
    Format text with a strike through it

    Returns
        (str) - the text with a strike through it
    """
    return f"\x1b[9m{text}\x1b[29m"


def display_menu(choices: list):
    """
    Display a menu

    Arguments:
        choices (list) - a list of choices
    """
    idx_len = 1 + (len(choices) // 10)
    for (i, choice) in enumerate(choices):
        print(f"{str(i + 1).rjust(idx_len)} - {cyan(choice)}")


def display_menu_with_choice(choices: list):
    """
    Display a menu and ask for user choice.

    Arguments:
        choices (list) - a list of choices

    Returns
        (int) - the choice, starting from 1 until the length of the choices
    """
    print(green("\nWhat do you want to choose?"))
    display_menu(choices)
    print()
    return error_testing.input_number_in_range(len(choices))

def display_main_menu_with_choice(choices: list, title):
    """
    Display a main menu and ask for user choice.

    Arguments:
        choices (list) - a list of choices

    Returns
        (int) - the choice, starting from 1 until the length of the choices
    """
    print(yellow('\n' + 30 * "*"))
    print(yellow(title.center(30)))
    print(yellow(30 * "*"))
    print(magenta('Please make your selection:'))
    display_menu(choices)
    print(yellow(30 * "*" + '\n'))
    return error_testing.input_number_in_range(len(choices))

