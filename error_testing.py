"""
Author Names : Varun Sahni, Junyuan Chen
File Name: error_testing.py
Date and time completed: 2022-01-02 12:30
Assignment Name: Company Database Project
TODO: Create all of the functions which will be used to error test and return user input.
"""

import re
import datetime

import uiutils
from classes.product_class import Product
from classes.employee_class import Employee
from classes.sale_class import Sale

def input_number(prompt="", is_integer=True, is_zero_valid=False):
    """
    Return number inputted by the user after converting it to either an integer or float, only when it is valid

    Arguments:
        prompt (str) - the prompt when asking the user for input
        is_integer (bool) - boolean whose value depends on whether the user input needs to be a float or integer

    Returns:
        current_num (int) or (float) - a valid integer or float, depending on what is needed, entered by the user
  """
    is_valid = False
    while not is_valid:
        current_num = input(f"{prompt}:\n")
        try:
            if is_integer:
                msg = f"Please enter a {uiutils.underline('valid')} integer.\n"
                current_num = int(current_num)
            else:
                msg = f"Please enter a {uiutils.underline('valid')} number.\n"
                current_num = round(float(current_num), 2)
            if not is_zero_valid:
                1 / current_num
            assert current_num >= 0
        except ValueError:
            print(uiutils.yellow(msg))
        except ZeroDivisionError:
            msg = "Please do not enter 0\n"
            print(uiutils.yellow(msg))
        except:
            msg = "Please enter a positive number\n"
            print(uiutils.yellow(msg))
        else:
            print()
            is_valid = True

    return current_num


def input_quantity(product, prompt=""):
    """
    Return a valid quantity for a product sold entered by the user

    Arguments:
        product (Product object) - the product that is being sold
        prompt (str) - the prompt when asking the user for input

    Returns:
        current_num (int) - the quantity entered by the user after converting it to an integer
    """

    current_num = input_number(f"{prompt}")
    while current_num > product.stock:
        msg = "You cannot sell more than the product's stock\n"
        print(uiutils.yellow(msg))
        current_num = input_number(f"{prompt}")
    return current_num


def input_number_in_range(upper_bound: int):
    """
    Return number in a given range inputted by the user after converting it to either an integer, only when it is valid

    Arguments:
        upper_bound - the upper bound of the number range (lower will always be 1)
    Returns:
        number (int) - a valid integer in a range entered by the user
  """
    number = input_number("Please enter your choice")
    while number > upper_bound:
        msg = f"Please enter a number between 1 and {upper_bound}:\n"
        print(uiutils.yellow(msg))
        number = input_number("Please enter your choice:")
    return number


def input_date(prompt=""):
    """
    Return date inputted by the user only when it is valid

    Arguments:
        prompt (str) - the prompt when asking the user for input

    Returns:
        the_date (str) - a valid date entered by the user
  """
    is_date_valid = False
    while not is_date_valid:
        the_date = input(f"{prompt} (yyyy-mm-dd):\n").strip()
        try:
            datetime.datetime.strptime(the_date, "%Y-%m-%d")

        except:
            msg = "Please enter a valid date\n"
            print(uiutils.yellow(msg))

        else:
            is_date_valid = True
            the_date = the_date.split("-")
            for i in range(1, len(the_date)):
                if len(the_date[i]) == 1:
                    the_date[i] = "0" + the_date[i]
            the_date = "-".join(the_date)

    return the_date


def input_time(prompt=""):
    """
    Return time inputted by the user only when it is valid

    Arguments:
        prompt (str) - the prompt when asking the user for input

    Returns:
        the_time (str) - a valid time entered by the user
  """
    is_time_valid = False
    while not is_time_valid:
        the_time = input(f"{prompt} (hh:mm:ss):\n").strip()
        try:
            datetime.datetime.strptime(the_time, "%H:%M:%S")

        except Exception:
            msg = "Please enter a valid time\n"
            print(uiutils.yellow(msg))

        else:
            is_time_valid = True
            the_time = the_time.split(":")
            for i in range(len(the_time)):
                if len(the_time[i]) == 1:
                    the_time[i] = "0" + the_time[i]

            the_time = ":".join(the_time)
    return the_time


def validate_input(prompt, regex, input_type):
    """
    Return user input validated using a regex only when it is valid (this function will always be called by other functions)

    Arguments:
        prompt (str) - the prompt when asking the user for input
        regex (str) - the regex to use to match
        input_tupe (str) - the type of input which is being validated

    Returns:
        user_input (str) - a valid input entered by the user
  """
    user_input = input(f"\n{prompt}:\n").strip()
    while not re.search(regex, user_input):
        msg = f"Please enter a valid {input_type}\n"
        print(uiutils.yellow(msg))
        user_input = input(f"{prompt}:\n").strip()
    return user_input


def input_email(prompt=""):
    """
    Return user input for email by calling validate_input for validation

    Arguments:
        prompt (str) - the prompt when asking the user for email input

    Returns:
        (str) - a valid email entered by the user
  """
    return validate_input(prompt, r"^[\w.+-]+@[a-zA-Z\d]+\.[a-zA-Z]+$", "email")


def input_phone_number(prompt=""):
    """
    Return user input for phone number by calling validate_input for validation

    Arguments:
        prompt (str) - the prompt when asking the user for phone number input

    Returns:
        (str) - a valid phone number entered by the user
  """
    return validate_input(prompt, r"^(\+\d{1,2} )?(\(\d{3}\)|\d{3})[-. ]?\d{3}[-. ]?\d{4}$", "phone number")


def input_product_id(prompt, for_sale=False):
    """
    Return product whose id is inputted by the user only when it is valid

  Arguments:
    prompt (str) - the prompt when asking the user for input for product id
    for_sale (bool) - whether the product id is being entered as for in a sale or not

  Returns:
    product (Product object) - the product whose id will be entered by the user
  """
    is_product_id_valid = False
    while not is_product_id_valid:
        product_id = input_number("Please enter the product id")
        try:
            product = Product.load(product_id)
            if for_sale:
                assert not product.is_deleted
                if product.stock <= 0:
                    raise ValueError

        except ValueError:
            msg = "This product is deleted and thus unavailable.\n"
            print(uiutils.yellow(msg))

        except Exception:
            msg = "Please enter the id of an existing product\n"
            print(uiutils.yellow(msg))
        else:
            is_product_id_valid = True
    return product


def input_employee_id(prompt=""):
    """
    Return employee whose id is inputted by the user only when it is valid

  Arguments:
    prompt (str) - the prompt when asking the user for input for employee id

  Returns:
    employee (Employee object) - the employee whose id will be entered by the user
  """
    is_employee_id_valid = False
    while not is_employee_id_valid:
        employee_id = input_number(f'{prompt}')
        try:
            employee = Employee.load(employee_id)
        except:
            msg = "Please enter the id of an existing employee\n"
            print(uiutils.yellow(msg))
        else:
            is_employee_id_valid = True
    return employee

def input_sale_id(prompt=""):
    """
    Return sale whose id is inputted by the user only when it is valid

  Arguments:
    prompt (str) - the prompt when asking the user for input for sale id

  Returns:
    sale (Sale object) - the sale whose id will be entered by the user
  """
    is_sale_id_valid = False
    while not is_sale_id_valid:
        sale_id = input_number(f'{prompt}')
        try:
            sale = Sale.load(sale_id)
        except:
            msg = "Please enter the id of an existing sale\n"
            print(uiutils.yellow(msg))
        else:
            is_sale_id_valid = True
    return sale

def killswitch(prompt=""):
    """
    Makes sure user input is valid and checks whether user wants to continue doing something

    Arguments:
        prompt (str) - the prompt when asking whether the user wants to continue doing something

    Returns:
        True or False (bool) - depending on whether user wants to continue doing something
    """
    killswitch_dict = {
        "y": True,
        "n": False
    }

    keep_looping = input(uiutils.magenta(f"{prompt} (y/n):\n")).lower()
    while keep_looping not in ["y", "n"]:
        print("Please entter a valid choice\n")
        keep_looping = input(uiutils.magenta(f"{prompt}(y/n):\n")).lower()
    print()

    return killswitch_dict[keep_looping]


def get_user_regex():
    """
    Return a regex to match a string inputted by the user only when it is valid

  Arguments:
    prompt (str) - the prompt when asking the user for input for the regex

  Returns:
    regex (str) - the valid regex entered by the user
  """
    is_valid = False
    while not is_valid:
        try:
            regex = input(f"Please enter a regex to use to search:\n").strip()
            re.compile(regex)

        except:
            msg = f"Please input a {uiutils.underline('valid')} regex.\n"
            print(uiutils.yellow(msg))
        else:
            is_valid = True
    return regex
