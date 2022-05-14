"""
Author Names : Varun Sahni, Junyuan Chen
Folder Name: sub_menus
File Name: sales_menu.py
Date and time completed: 2022-01-04 8:30
Assignment Name: Company Database Project
TODO: Create all of the functions along with the main sales menu,
in which the functions will be used. Examples of the functions
include searching for and adding sales and viewing the products
sold in a sale.
"""

import uiutils
import error_testing
import search_functions
import security
from classes.employee_class import Employee
from classes.sale_class import Sale
from sub_menus import products_menu

def view_products_with_sale(sale):
    """
    Outputs all products associated with a sale

    Arguments:
        sale (Sale object) - the sale to use to view products
    """
    print("\nProducts associated with the sale:\n")
    products, quantities = sale.load_products()
    if len(products):
        for i in range(len(products)):
            print(uiutils.magenta("Product:") + f" {products[i]}")
            print(uiutils.magenta("Quantity sold:") + f" {quantities[i]}\n")
        total_cost = sum([products[i].price * quantities[i] for i in range(len(products))])
        print(f"The total cost is ${uiutils.yellow(total_cost)}")
    else:
        print("There are no stored products associated with the sale. All of the products sold have been destroyed permanently by the company.")


def individual_menu():
    """
    The individual sale menu. User view the products sold, delete the sale and return to the main product menu when done. This menu will have different functionailty depending on the access level.
    """
    options = [
        "View Products in Sale",
        uiutils.red("Delete Invalid Sale"),
        "Return to Sales Menu"
    ]
    sale = error_testing.input_sale_id("Please input a sale ID")
    print("Sale:")
    print(sale)
    print("\nCashier:")
    print(sale.load_cashier())

    # implement hiding/changing menu option
    # functionailty changes depending on access
    if security.USER.permission == 0:
        view_products_with_sale(sale)
        return

    done = False
    while not done:
        choice = uiutils.display_menu_with_choice(options)
        if choice == 1:
            view_products_with_sale(sale)

        elif choice == 2 and security.check_manager():
            really = error_testing.killswitch(
                f"Are you sure? This will {uiutils.underline('permanently')} "
                f"remove {uiutils.underline('all')} data (including products) "
                f"associated with this sale!"
            )
            if really:
                sale.destroy()
                print(uiutils.red(f"Sale {sale} destroyed."))
                return
            else:
                print("Cancelled.")
        elif choice == 3:
            done = True


def match_sales_using_products():
    """
    Find all of the sales which included certain products which the user wants to search for

    Returns:
        (list) - the list of sales (no repeats) which included the products
    """
    sales = []
    products = products_menu.search_products_menu()
    for product in products:
        sales.extend(product.load_sales()[0])
    sales.sort(key=lambda x: x.id)
    results = []
    for s in sales:
        if s not in results:
            results.append(s)
    return results


def search_sales_menu():
    """
    The search sales menu. It allows the user to search for sales using the products in the sale, a date or a time. It will implement one of the search functions or check all of the Product objects for a certain condition.

    Returns:
        (list) - of Sale objects which match the condition the user wants to use to search
    """

    print("Show sales where:")
    choice = uiutils.display_menu_with_choice([
        "Sales that have a product whose...",
        "Number of items sold is in range...",
        "Sale date is in range...",
        "Time is in range..."
    ])
    if choice == 1:
        return match_sales_using_products()
    elif choice == 2:
        return search_functions.match_quantity_of_products(Sale, "number of items sold")
    elif choice == 3:
        return search_functions.match_date_range(Sale, "date")
    else:
        return search_functions.match_time_range(Sale, "time")


def display_search_sales_menu():
    """
    The display searched sales menu. Allows user to view and choose any of the matched sales to view the products associated with it or return to the main sales menu
    """
    matched = search_sales_menu()
    print(uiutils.magenta("\nMatching Sales:"))
    if len(matched):
        uiutils.display_menu(matched)
    else:
        print(uiutils.yellow("No matches."))


def new_sale_menu():
    """
    The new sale menu. User can create a new Sale object by choosing a cashier and products. The date and time will be auto generated. The object will then be used to insert a sale into the sale table in the database.
    """

    sale = Sale.new()
    if security.USER.permission >= 1:
        cashiers = Employee.load_where('permission = ?', [0])
        print('Choose the cashier')
        cashier_choice = uiutils.display_menu_with_choice(cashiers) - 1
        sale.cashier_id = cashiers[cashier_choice].id
    else:
        # auto choose cashier
        sale.cashier_id = security.USER.id
    quantity_and_id_list = []
    done = False
    while not done:
        product = error_testing.input_product_id("Enter the id of the product sold", for_sale=True)
        quantity_sold = error_testing.input_quantity(product, "Please enter the quantity sold")
        product.stock -= quantity_sold
        product.save()
        quantity_and_id_list.append((product.id, quantity_sold))
        print(f'Product: {product} ')
        print('Successfully added\n')
        done = error_testing.killswitch("Are you finished with adding products?")

    sale.save()
    sale.set_products(quantity_and_id_list)
    # NOTE Not a bug: set_products() inserts rows into the join table.
    # To insert into the join table, one must have an sale_id first.
    # Thus, save() first, then set_products().

    print(uiutils.green(f"Sale {sale} created."))


def view_sales_menu():
    """ Show all sales. """
    sales = Sale.load_all()
    print(f"\nThere are {len(sales)} sales.")
    uiutils.display_menu(sales)


def sales_menu():
    """
    The main sales menu. The user can view all of the sales and pick one of them to view the products associated with it, search for sales using a condition, create a new sale or return to the main menu.
    """

    options = [
        "View Sales",
        "Individual Sale Actions",
        "Search Sales",
        "New Sales",
        "Return to Main Menu"
    ]
    # hide/change menu options rather than create additional choices to imlement security
    # also reduce the need of messages and journal logs
    if security.USER.permission == 0:
        options[1] = "Additional Sale Info"
    done = False
    while not done:
        print()
        choice = uiutils.display_main_menu_with_choice(options, "Sale Menu")
        if choice == 1:
            view_sales_menu()
        elif choice == 2:
            individual_menu()
        elif choice == 3:
            display_search_sales_menu()
        elif choice == 4:
            new_sale_menu()
        elif choice == 5:
            return