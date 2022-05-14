"""
Author Names: Varun Sahni, Junyuan Chen
File Name: main.py
Date and time completed: 2022-01-06 14:45
Assignment Name: Company Database Project
TODO: Create the main program with the main menu which will act as the entry point for all of the other functions
"""

import sys
import sqlite3

import uiutils
import security
from classes import abstract_class
from sub_menus import employees_menu, products_menu, sales_menu


COMPANY_NAME = "Waldo's Shoes"
DATABASE_PATH = "data.db"

def main_menu():
    """The main menu. The other functions will be called through this function."""

    options = [
        "Employees Information",
        "Products Information",
        "Sales Information",
        "Quit"
    ]

    done = False
    while not done:
        choice = uiutils.display_main_menu_with_choice(options, "Main Menu")
        if choice == 1 and security.check_manager():
            employees_menu.employees_menu()
        elif choice == 2:
            products_menu.products_menu()
        elif choice == 3:
            sales_menu.sales_menu()
        elif choice == 4:
            return


def main():
    """ The main function. """
    welcome = f"Welcome to the {COMPANY_NAME} Database System."
    print(uiutils.blue(welcome))
    con = sqlite3.connect(DATABASE_PATH)

    try:
        # By default, sqlite3 does NOT enforce foreign key constraints,
        # and will also ignore CASCADE directives.
        # Must manually turn on foreign keys
        con.execute("PRAGMA foreign_keys = ON")
        cur = con.execute("PRAGMA foreign_keys")
        if cur.fetchone()[0] == 0:
            # For some versions, foreign keys are not available at all.
            # But `PRAGMA foreign_keys = ON` will not error out, it will
            # silently become no-op. Must manually verify it's enabled.
            print(uiutils.red(
                "This version of SQLite3 is NOT "
                "compiled with foreign key support."
            ))
            sys.exit(1)
        cur.close()
        abstract_class.CON = con
        security.login()
        main_menu()
        print(uiutils.blue("\nBye!"))
    finally:
        con.close()


if __name__ == "__main__":
    main()
