-- Author Names: Varun Sahni, Junyuan Chen
-- File Name: schema.sql
-- Date and time completed: 2021-12-15 10:05
-- Assignment Name: Company Database Project
-- TODO: Create the tables to store data for employees, products and sales


BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    salted_hash TEXT NOT NULL,
    permission INTEGER NOT NULL DEFAULT 0 CHECK (permission >= 0),
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    hire_date TEXT NOT NULL,
    position TEXT NOT NULL,
    salary INTEGER NOT NULL CHECK (salary > 0),
    manager_id INTEGER,
    FOREIGN KEY (manager_id) REFERENCES employees(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price FLOAT NOT NULL CHECK (price > 0),
    stock INTEGER NOT NULL CHECK (stock >= 0),
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    cashier_id INTEGER NOT NULL,
    FOREIGN KEY (cashier_id) REFERENCES employees(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS sales_products (
    sale_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity_sold INTEGER NOT NULL CHECK (quantity_sold > 0),
    PRIMARY KEY (sale_id, product_id),
    FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Speed things up.
CREATE INDEX IF NOT EXISTS sales_idx ON sales_products(sale_id);
CREATE INDEX IF NOT EXISTS products_idx ON sales_products(product_id);

COMMIT;
