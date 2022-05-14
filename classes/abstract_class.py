"""
Author Names : Varun Sahni, Junyuan Chen
Folder Name: classes
File Name: abstract_class.py
Date and time completed: 2022-01-05 12:45
Assignment Name: Company Database Project
TODO: Create an abstract class with various abstract methods to  which the other classes for the SQL tables will inherit from
"""

import functools


CON = None


def use_cursor(f):
    """ Pass a database cursor as argument `cur` to `f`. """
    # Make help() aware that decorated() is a wrapper
    # around f() so it will display the correct docstring
    # and function signature.  Nothing magic here.
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        cur = CON.cursor()
        try:
            return f(*args, **kwargs, cur=cur)
        finally:
            CON.commit()
            cur.close()

    return decorated


class SQLTable():
    """
    SQLTable class is an abstract class and is not meant to be
    instantiated. It only serves as a factory class which
    other classes can inherit from to create classes for the sales table, employees table or products table.

    The purpose of using a class to represent each table is to create an interface to interact with in order to not directly interact with the sql tables. Having each object represent a row also allows us to use various methods on the row for additional functionality.

    Instances of the child classes will all have a unique id.

    Apart from the save method, all of the methods will be abstract methods and must be overridden. The purpose of having these abstract methods is to create an interface so the method name is known and can be interacted with.

    Instances of the child classes will all have a string representation They will be used to either _insert in the corresponding sql table or _update it, these methods must only be called by the save method. There will be a method to delete an object/row from the table, and create new objects with placeholder values.

    You can load an object/row from the table using the id Multiple objects can be returned in a list using load_where which searches for objects/rows which meet a certain condition, load_many, which always searches using a list of ids, or load_all, which just loads all of the objects from the corresponding the sql table.
    """

    def __eq__(self, other):
        """
        Checks equality between objects of the same class using the id
        """
        return self.__class__ == other.__class__ and self.id == other.id

    def save(self):
        """
        Save changes made to the databse. If the object does not yet have an id, the object will be used to _insert into the databse, otherwise it will be used to _update the database
        """
        if self.id is None or self.id == 0:
            self._insert()
        else:
            self._update()

    def _insert(self, cur):
        """
        Insert an object into the table

        Arguments:
            cur (sqlite3 Cursor object) - the cursor to be used to interact with the sql tables
        """
        raise NotImplementedError

    def _update(self, cur):
        """
        Use an object to update a row in the table

        Arguments:
            cur (sqlite3 Cursor object) - the cursor to be used to interact with the sql tables
        """
        raise NotImplementedError

    @use_cursor
    def destroy(self, cur):
        """Delete a row from the table"""
        raise NotImplementedError

    @staticmethod
    def new():
        """
        Create a new object with placeholder values to represent a table's row

        Returns:
            (custom object) - an object representing the row with placeholder values
        """
        raise NotImplementedError

    @staticmethod
    @use_cursor
    def load(id):
        """
        Load an object representing a row using the id

        Arguments:
            id (int) - the employee id

        Returns:
            (custom object) - a single object representing the row
        """
        raise NotImplementedError

    @staticmethod
    def load_all():
        """
        Load an object for each row in the database

        Returns:
            (list) - a list of the objects, one for every single row
        """
        raise NotImplementedError

    @staticmethod
    def load_where(where, args, cur):
        """
        Load objects representing rows which meet a certain condition

        Arguments:
            where (str) - the 'type' of condition which is being checked (for eg: price > ?)
            args (list) - a list containing the values used to check in the condition (for eg: [50])
            cur (sqlite3 Cursor object) - the cursor to be used to interact with the sql tables

        Returns:
            (list) - a list of objects that meet the condition
        """
        raise NotImplementedError

    @staticmethod
    def load_many(ids):
        """
        Load multiple objects/rows using a list of ids

        Arguments:
            ids - the list of ids to use to load objects

        Returns:
            (list) - a list of objects, one for every id
        """
        raise NotImplementedError
