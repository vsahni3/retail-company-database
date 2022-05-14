"""
Author Names : Varun Sahni, Junyuan Chen
File Name: security.py
Date and time completed: 2022-01-05 11:05
Assignment Name: Company Database Project
TODO: Create all of the functions that will be used to ensure security protocls are followed for the program.
"""

import sys
import time
import getpass
import hashlib

from classes.employee_class import Employee
import uiutils
import error_testing

USER = None


def journal_log(msg):
    """
    Log an appropriate message to the journal

    Arguments:
        msg (str) - the appropriate message
    """
    with open("journal.log", "a", encoding="utf-8") as journal:
        journal.write(f"[{time.time()}] {msg}\n")


def calculate_hash(id, password):
    """
    Calculate the salted hash of the employee's password using their id as the salt to create unique passwords

    Arguments:
        id (int) - the employee id
        password (str) - the employee password
    """
    # hash password
    pwd_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    salted = f"{id}$${pwd_hash}".encode("utf-8")
    # hash password with salt (id) added
    return hashlib.sha256(salted).hexdigest()


def no_permission():
    """
    Print an appropriate message and log the incident
    when an employee tries to do an action they don't
    have access for.
    """
    journal_log(
        f"check_permission: User {USER.id} ({USER}) "
        f"does not have necessary permissions."
    )
    print(uiutils.red("You do not have necessary permissions."))
    print(uiutils.red("This incident will be reported."))
    print(uiutils.red("Expect the FBI..."))


def login():
    """
    Force the user of the program to login in the beginning using their id and password to verify their status as a Waldo's Shoes employee
    """
    global USER
    for _ in range(5):
        print(uiutils.yellow("\nLogin required."))
        id = error_testing.input_number("ID")
        pwd = getpass.getpass()
        salted_hash = calculate_hash(id, pwd)
        try:
            user = Employee.load(id)
            assert user.get_salted_hash() == salted_hash
        except:
            journal_log(f"login: Login failed with ID {id}")
            # Don't tell them whether the ID or the password is wrong
            print(uiutils.red("\nThe login is invalid."))
            print(uiutils.red("This incident will be reported.\n"))
        else:
            USER = user
            print()
            return

    msg = "Maximum retries (5) exceeded."
    journal_log(f"login: {msg}")
    print(uiutils.red(msg))
    sys.exit("Program Has Ended.")


def check_manager():
    """
    Check if an employee has the access level of a manager or above

    Returns:
        (bool) - True if they have at least the permission of a manager, False if not.
    """
    if USER.permission >= 1:
        return True
    no_permission()
    return False


def check_owner():
    """
    Check if the user has the access level of / is the owner

    Returns:
        (bool) - True if they have the permission of the owner, False if not.
    """
    if USER.permission >= 2:
        return True
    no_permission()
    return False
