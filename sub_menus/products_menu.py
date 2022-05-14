"""
Author Names : Varun Sahni, Junyuan Chen
Folder Name: sub_menus
File Name: products_menu.py
Date and time completed: 2022-01-03 23:30
Assignment Name: Company Database Project
TODO: Create all of the functions along with the main products menu, in which the functions will be used. Examples of the functions include updating, deleting, searching for and adding products.
"""
import re
import search_functions
from sub_menus import sales_menu
from classes.product_class import Product
import uiutils
import error_testing
import security


def view_sales_with_product(product):
    """
    Outputs all sales associated with a product

    Arguments:
        product (Product object) - the product to use to view sales
    """
    print(uiutils.green("Sales:\n"))
    sales, quantities = product.load_sales()
    if len(sales):
        for i in range(len(sales)):
            print(uiutils.magenta("Sale: ") + f"{sales[i]}")
            print(uiutils.magenta("Quantity sold: ") + f"{quantities[i]}\n")
    else:
        print(uiutils.yellow("No sales for this product."))


def individual_menu():
    """
    The individual product menu. User can update the name, price and stock, delete the product and then change the database and return to the main product menu when done. This menu will have different functionailty depending on the access level.
    """
    options = [
        "View Sales With Product",
        "Change Name",
        "Change Price",
        "Change Stock",
        None,
        uiutils.red("Destroy Product"),
        "Back to Inventory"
    ]
    product = error_testing.input_product_id("Please enter the id of the product")
    done = False

    print(f"\nProduct {product}")
    print(f"Stock: {product.stock}\n")
    while not done:

        # implement hiding/changing menu option
        # functionailty changes depending on access
        if security.USER.permission == 0:
            view_sales_with_product(product)
            return

        if product.is_deleted:
            options[4] = uiutils.green("Undelete Product")
        else:
            options[4] = uiutils.red("Delete Product")


        choice = uiutils.display_menu_with_choice(options)
        if choice == 1:
            view_sales_with_product(product)
            continue

        elif choice == 2:
            product.name = input("Enter the new name:\n").strip()
        elif choice == 3:
            product.price = error_testing.input_number("Enter the new price", False)
        elif choice == 4:
            product.stock = error_testing.input_number("Enter the new stock")
        elif choice == 5:
            product.is_deleted = 1 - product.is_deleted  # toggle
        elif choice == 6:
            really = error_testing.killswitch(
                f"Are you sure? This will {uiutils.underline('permanently')} "
                f"remove {uiutils.underline('all')} data (including sales) "
                f"associated with this product!"
            )
            if really:
                product.destroy()
                print(uiutils.red(f"Product {product} destroyed."))
                return
            else:
                print("Cancelled.")
        else:
            return
        product.save()
        print(f"\nProduct {product}")
        print(f"Stock: {product.stock}\n")


def match_products_using_sales():
    """
    Find all of the products which were sold in certain sales which the user wants to search for

    Returns:
        (list) - the list of products (no repeats) which were sold in the sales
    """
    products = []
    sales = sales_menu.search_sales_menu()
    for sale in sales:
        products.extend(sale.load_products()[0])
    products.sort(key=lambda x: x.id)
    results = []
    for p in products:
        if p not in results:
            results.append(p)
    return results


def search_products_menu():
    """
    The search products menu. It allows the user to search for products using the name, sales, price, quantity or stock. It will implement one of the search functions or check all of the Product objects for a certain condition.

    Returns:
        (list) - of Product objects which match the condition the user wants to use to search

    """
    print("Show products where:")
    choice = uiutils.display_menu_with_choice([
        "Products that have a sale whose...",
        "Product name matches...",
        "Product name starts with...",
        "Total quantity sold is in range...",
        "Product price in range...",
        "Product stock is in the range..."
    ])

    if choice == 1:
        return match_products_using_sales()
    elif choice == 2:
        regex = error_testing.get_user_regex()
        return [p for p in Product.load_all() if re.search(regex,p.name)]
    elif choice == 3:
        string_checker = input("Product name starts with the string:\n").title().strip()
        return Product.load_where("name LIKE ?", [f"{string_checker}%"])
    elif choice == 4:
        return search_functions.match_quantity_of_products(Product, "total quantity sold")

    elif choice == 5:
        return search_functions.match_number_range(Product, 'price', False)

    else:
        return search_functions.match_number_range(Product, 'stock')


def display_search_products_menu():
    """
    The display searched products menu. Allows user to view and choose any of the matched products to do more actions with them by calling product_menu on the chosen product. User can return to main product menu when done
    """

    matched = search_products_menu()
    print(uiutils.magenta("\nMatching products:"))
    if len(matched):
        uiutils.display_menu(matched)
    else:
        print(uiutils.yellow("No matches."))


def new_product_menu():
    """
    The new product menu. User can create a new Product object by choosing a name, stock and price. The object will then be used to insert a product into the product table in the database"""
    product = Product.new()
    product.name = input("Enter the name:\n").strip()
    print()
    product.price = error_testing.input_number("Enter the price", False)
    product.stock = error_testing.input_number("Enter the stock")
    product.save()
    print(uiutils.green(f"Product {product} created."))


def view_products_menu():
    """ Show all products. """
    products = Product.load_all()
    print(f"There are {len(products)} products.")
    uiutils.display_menu(products)


def products_menu():
    """
    The main product menu. The user can view all of the products and pick one of them to do an action on it using individual_menu, search for products using a condition, create a new product or return to the main menu.
    """

    options = [
        "View Products",
        "Individual Product Actions",
        "Search Products",
        "New Product",
        "Back to Main Menu"
    ]
    # hide/change menu options rather than create additional choices to imlement security
    # also reduce the need of messages and journal logs
    if security.USER.permission == 0:
        options[1] = "Additional Product Info"
    done = False
    while not done:
        choice = uiutils.display_main_menu_with_choice(options, "Product Menu")
        if choice == 1:
            view_products_menu()
        elif choice == 2:
            individual_menu()
        elif choice == 3:
            display_search_products_menu()
        elif choice == 4 and security.check_manager():
            new_product_menu()
        elif choice == 5:
            return
