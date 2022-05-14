"""
Author Names : Varun Sahni, Junyuan Chen
File Name: search_functions.py
Date and time completed: 2022-01-02 12:30
Assignment Name: Company Database Project
TODO: Create all of the functions which will be used to match values in a range that a user wants to use to search for employees, products or sales
"""

import error_testing
from classes.sale_class import Sale

def match_range(the_class, field, function, is_integer=False, is_zero_valid=False):
    """
    Match objects using any field (for eg. price) within a range of values.

    Arguments:
        the_class (custom class) - the class to search in
        field (int, float or str) - the field to search in the range
        function (function) - the function to validate the inputs
        is_integer (bool) - whether the field is an integer or not (only used for numerical inputs)
        is_zero_valid (bool) - whether 0 is accepted or not (only used for numerical inputs)

    Returns:
        (list) - list of the_class objects which are in the range
    """

    prompt1 = f"Enter the lower bound of the {field} range"
    prompt2 = f"\nEnter the upper bound of the {field} range"

    # only call with is_integer argument if the function is error_testing.input_number
    if function == error_testing.input_number:
        value1 = function(prompt1, is_integer, is_zero_valid)
        value2 = function(prompt2, is_integer, is_zero_valid)
    else:
        value1 = function(prompt1)
        value2 = function(prompt2)
    field = field.replace(" ", "_")
    return the_class.load_where(f"{field} BETWEEN ? AND ?", [value1, value2])


def match_date_range(the_class, field):
    """
    Match objects using a date within a range of dates.

    Arguments:
        the_class (custom class) - the class to search in
        field (str) - the field to search in the range

    Returns:
        (list) - list of the_class objects which are in the range
    """
    return match_range(the_class, field, error_testing.input_date)


def match_number_range(the_class, field, is_integer=True, is_zero_valid=True):
    """
    Match objects using a number within a range of numbers.

    Arguments:
        the_class (custom class) - the class to search in
        field (int or float) - the field to search in the range
        is_integer (bool) - whether the field is an integer or not

    Returns:
        (list) - list of the_class objects which are in the range
    """
    return match_range(the_class, field, error_testing.input_number, is_integer, is_zero_valid)


def match_time_range(the_class, field):
    """
    Match objects using a time within a range of time.

    Arguments:
        the_class (custom class) - the class to search in
        field (str) - the field to search in the range

    Returns:
        (list) - list of the_class objects which are in the range
    """
    return match_range(the_class, field, error_testing.input_time)


def match_quantity_of_products(class_name, prompt):
    """
    Either match sales in a range using the quantity of items sold or products in a range using the total quantity sold to date

    Arguments:
        class_name (custom class) - the class to use to match (Sale or Product)
        prompt (str) - the string added to the prompt to get user input

    Returns:
        (list) - a list of products or sales that match the condition

    """
    values = class_name.load_all()
    value1 = error_testing.input_number(f"Enter the lower bound of the {prompt} range", True, True)
    value2 = error_testing.input_number(f"Enter the upper bound of the {prompt} range", True, True)
    if class_name == Sale:
        return [v for v in values if sum(v.load_products()[1]) in range(value1, value2 + 1)]
    else:
        return [v for v in values if sum(v.load_sales()[1]) in range(value1, value2 + 1)]
