"""
Author Names : Varun Sahni, Junyuan Chen
Folder Name: classes
File Name: sale_class.py
Date and time completed: 2022-01-07 12:45
Assignment Name: Company Database Project
TODO: Create a class to represent the sales SQL table which has many useful methods and can create Sale instances.
"""

import datetime
from classes import abstract_class, employee_class, product_class
from classes.abstract_class import use_cursor


class Sale(abstract_class.SQLTable):
    """
    Sale class will create instances of Sale. Each sale will have a unique id, date, time and the id of the cashier.

    Sale class will override all of the abstract methods from the SQLTable class using their own implementation.

    This class will also have the load_products method, which can be used to give a list all of the products sold in a Sale.
    """

    def __init__(self, id, date, time, cashier_id):
        """
        Initialize the attributes of each Sale object.
        To create an instance of a Sale, enter the following arguments:
            id (int) - the unique sale id
            date (str) - the date of the sale
            time (str) - the time of the sale
            cashier_id (int) - the unique id of the cashier
        """
        self.id = id
        self.date = date
        self.time = time
        self.cashier_id = cashier_id

    def __str__(self):
        """
        return string representation using the id, cashier Employee object name, date and time

        Returns:
            (str) - the string representation
        """
        return f'[ID: {self.id}]  Cashier: {self.load_cashier().name} <{self.date} {self.time}>'

    # what if u load a sale object, and called save() by mistake
    @use_cursor
    def save(self, cur):
        """
        Insert a new row to the sales table using a Sale object. Get the sale id from the table (autogenerated) to be used when printing the sale's info.
        This method will only be used for insertions, and an error will be raised if an existing sale is being saved, as sales cannot be updated.

        Arguments:
            cur (sqlite3 Cursor object) - the cursor to be used to interact with the sql tables

        """
        assert self.id is None, "Sales cannot be updated"
        cur.execute(
            "INSERT INTO sales (date, time, cashier_id) "
            "VALUES (?, ?, ?)",
            [self.date, self.time, self.cashier_id]
        )
        self.id = cur.lastrowid

    def load_cashier(self):
        return employee_class.Employee.load(self.cashier_id)

    @use_cursor
    def set_products(self, quantity_and_id_list, cur):
        """
        Set all products named by `ids` to be associated with this sales in the join table.

        Arguments:
            quantity_and_id_list (list) - a list of product id and quantity tuples to associate with this sale
            cur (sqlite3 Cursor object) - the cursor to be used to interact with the sql tables
        """
        sql = "INSERT INTO sales_products (sale_id, product_id, quantity_sold) VALUES (?, ?, ?)"
        for id, quantity in quantity_and_id_list:
            cur.execute(sql, [self.id, id, quantity])

    @staticmethod
    def load(id):
        """
        Load a Sale object using the id and the load_where method. Raise KeyError if the id does not exist in the table

        Arguments:
            id (int) - the sale id

        Returns:
            (Sale object) - the sale reprsenting the row
        """
        sale = Sale.load_where("id = ?", [id])
        if sale:
            return sale[0]
        raise KeyError(id)

    @staticmethod
    def new():
        """
        Create a new Sale object using placeholder values. The date and time will be autogenerated.

        Returns:
            (Sale object) - the newly created Sale object
        """
        now = datetime.datetime.now() - datetime.timedelta(hours = 5)
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        return Sale(None, date_str, time_str, None)

    @use_cursor
    def destroy(self, cur):
        """
        Delete a row from the table

        Arguments:
            cur (sqlite3 Cursor object) - the cursor to be used to interact with the sql tables
        """
        cur.execute("DELETE FROM sales WHERE id = ?", [self.id])

    @staticmethod
    def load_all():
        """
        Load all of the sales in the table by calling the load_where method

        Returns:
            result (list) - a list containing the Sale objects
        """
        return Sale.load_where("1")

    @staticmethod
    @use_cursor
    def load_where(where, args=[], cur=None):
        """
        Load Sale objects representing rows which meet a certain condition

        Arguments:
            where (str) - the 'type' of condition which is being checked (for eg: date > ?)
            args (list) - a list containing the values used to check in the condition (for eg: [2022-01-05])
            cur (sqlite3 Cursor object) - the cursor to be used to interact with the sql tables

        Returns:
            (list) - a list of Sale objects that meet the condition
        """
        result = []
        cur.execute(
            f"SELECT id, date, time, cashier_id FROM sales WHERE {where}",
            args
        )
        for data in cur.fetchall():
            id, date, time, cashier_id = data
            result.append(Sale(id, date, time, cashier_id))
        return result

    @staticmethod
    def load_many(ids):
        """
        Load multiple Sale objects/rows using a list of ids and load_where

        Arguments:
            ids - the list of ids to use to load objects

        Returns:
            (list) - a list of Sale objects, one for every id
        """
        args = ", ".join(["?"] * len(ids))
        return Sale.load_where(f"id IN ({args})", ids)

    @use_cursor
    def load_products(self, cur):
        """
        Load all of the Product objects and quantity of each product sold in the sale

        Arguments:
            cur (sqlite3 Cursor object) - the cursor to be used to interact with the sql tables

        Returns:
            (tuple) - a tuple containing the products and quantities

        """
        cur.execute(
            "SELECT product_id, quantity_sold FROM sales_products WHERE sale_id = ?",
            [self.id]
        )
        data = cur.fetchall()
        products = []
        quantities = []
        for id, quantity in data:
            products.append(product_class.Product.load(id))
            quantities.append(quantity)

        return products, quantities