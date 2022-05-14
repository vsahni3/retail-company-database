"""
Author Names : Varun Sahni, Junyuan Chen
Folder Name: sub_menus
File Name: employees_menu.py
Date and time completed: 2022-01-01 11:55
Assignment Name: Company Database Project
TODO: Create all of the functions along with the main employees menu, in which the functions will be used. Examples of the functions include updating, deleting, searching for and adding employees.
"""

import getpass
import re

from classes.employee_class import Employee
import uiutils
import error_testing
import security
import search_functions


def choose_password(employee, prompt):
    """
    Change password menu.

    Arguments:
        employee (Employee object) - the employee whose password will be changed
    """

    password = getpass.getpass(f"{prompt}\n")
    employee.set_salted_hash(security.calculate_hash(employee.id, password))
    print(uiutils.green(f"Password updated\n"))


def choose_manager(employee, prompt):
    """
    Ask the user to pick a manager from the list of existing managers or no manager as the employee's new manager

    Arguments:
        employee (Employee object) - the employee whose manager will be changed
    """

    print(f"{prompt}")

    managers = Employee.load_where("permission > ? AND id != ?", [0, employee.id])

    managers.append(None)
    choice = uiutils.display_menu_with_choice(managers) - 1
    if managers[choice] is None:
        employee.manager_id = None
    else:
        employee.manager_id = managers[choice].id


def choose_permission(employee, prompt):
    """
    Change the permission of an employee

    Arguments:
        employee (Employee object) - the employee whose permission will be changed
    """
    permissions = [
        'Standard Employee',
        'Manager',
        'Owner'
    ]
    print(f"\n{prompt}")
    print(f"\nCurrent permission is {uiutils.underline(permissions[employee.permission])}\n")
    employee.permission = uiutils.display_menu_with_choice(permissions) - 1


def individual_menu():
    """
    The individual employee menu. User can update or delete the employee and then change the database or return to the main employee menu when done. This menu will have different functionailty depending on the access level.
    """

    options = [
        "Change Name",
        "Change Email",
        "Change Phone Number",
        "Change Position",
        "Change Manager",
        "Change Salary",
        uiutils.yellow("Change Password"),
        uiutils.yellow("Change Permission"),
        uiutils.red("Delete Employee"),
        "Back to Employee Information"
    ]
    employee = error_testing.input_employee_id('Enter the id of the employee')
    employee.output_info()
    done = False

    # implement hiding/changing menu option
    # functionailty changes depending on access
    while not done and security.USER.permission == 2:
        choice = uiutils.display_menu_with_choice(options)
        if choice == 1:
            employee.name = input("Enter the new name:\n").strip().title()
        elif choice == 2:
            employee.email = error_testing.input_email("Enter the new email")
        elif choice == 3:
            employee.phone_number = error_testing.input_phone_number("Enter the new phone number")
        elif choice == 4:
            employee.position = input("Enter the new position:\n").strip()
        elif choice == 5:
            choose_manager(employee, "Choose the new manager")
        elif choice == 6:
            employee.salary = error_testing.input_number("Enter the new salary")
        elif choice == 7:
            choose_password(employee, "Enter the new password:")
        elif choice == 8:
            choose_permission(employee, "Enter the new permission")
        elif choice == 9:
            if error_testing.killswitch("Are you sure?"):
                employee.destroy()
                print(uiutils.red(f"Employee {employee} deleted."))
                # Current employee deleted
                # Can no longer edit current employee
                return
            else:
                print("Cancelled.")
        else:
            return
        employee.save()
        employee.output_info()


def search_employees_menu():
    """
    The search employees menu. It allows the user to search for employees using the name, salary or hire date. It will implement one of the search functions or check all of the Employee objects for a certain condition.

    Returns:
        (list) - of Employee objects which match the condition the user wants to use to search
    """

    print("Show employees where:")
    choice = uiutils.display_menu_with_choice([
        "Name matches...",
        "Last name starts with...",
        "First name starts with...",
        "Salary is in the range...",
        "Hire date is in the range..."
    ])
    if choice <= 2:
        if choice == 1:
            regex = error_testing.get_user_regex()

        else:
            string_checker = input("Last name starts with the string:\n").lower().capitalize().replace(" ", "")
            regex = f'.+ {string_checker}[^ ]*$'

        return [e for e in Employee.load_all() if re.search(regex, e.name)]

    elif choice == 3:
        string_checker = input("First name starts with the string:\n").lower().capitalize().replace(" ", "")
        return Employee.load_where("name LIKE ?", [f"{string_checker}%"])

    elif choice == 4:
        return search_functions.match_number_range(Employee, 'salary')

    else:
        return search_functions.match_date_range(Employee, 'hire date')


def display_search_employees_menu():
    """
    The display searched sales menu. Allows user to view and choose any of the matched employees to perform specific actions on them or return to the main sales menu.
    """

    matched = search_employees_menu()
    print(uiutils.magenta("\nMatching employees:\n"))
    if len(matched):
        uiutils.display_menu(matched)
    else:
        print(uiutils.yellow('No matches'))


def new_employee_menu():
    """
    The new employee menu. User can create a new Employee object by choosing the attributes to create it. The object will then be used to insert an employee into the employee table in the database.
    """
    print(uiutils.magenta("Add New Employee:\n"))
    employee = Employee.new()
    employee.name = input("Enter the name:\n").strip().title()
    employee.email = error_testing.input_email("Enter the email")
    employee.phone_number = error_testing.input_phone_number("Phone Number")
    employee.position = input("\nEnter the position:\n").strip()
    choose_permission(employee, "Enter the permission level")
    choose_manager(employee, "Choose the manager:")
    employee.salary = error_testing.input_number("Enter the salary")
    employee.save()
    choose_password(employee, "Enter the password:")
    employee.save()
    print(uiutils.green(f"Employee {employee} added."))


def view_employees_menu():
    """ Show all employees. """
    employees = Employee.load_all()
    print(f"\nThere are {len(employees)} employees.")
    uiutils.display_menu(employees)


def employees_menu():
    """
    The employee menu. The user can view all of the employees and pick one of them to do an action on it using individual_menu, search for employees using a condition, create a new employee or return to the main menu.
    """
    options = [
        "View Employees",
        "Individual Employee Actions",
        "Search Employees",
        "New Employee",
        "Back to Main Menu"
    ]
    # hide/change menu options rather than create additional choices to imlement security
    # also reduce the need of messages and journal logs
    if security.USER.permission == 1:
        options[1] = "Additional Employee Info"
    done = False
    while not done:
        choice = uiutils.display_main_menu_with_choice(options, "Employee Menu")
        if choice == 1:
            view_employees_menu()
        elif choice == 2:
            individual_menu()
        elif choice == 3:
            display_search_employees_menu()
        elif choice == 4 and security.check_owner():
            new_employee_menu()
        elif choice == 5:
            return