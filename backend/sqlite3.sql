-- WRITE DATABASE SCHEMAS HERE
-- NOTE: There can be a lot of syntax differences between MySQL and sqlite3

DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);

-- Main products table
CREATE TABLE IF NOT EXISTS products (
    ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
    ProductName TEXT NOT NULL,
    ProductBrand TEXT,
    Gender TEXT,
    Price INTEGER,
    NumImages INTEGER,
    Description TEXT,
    PrimaryColor TEXT
);

-- Shirts table, referencing ProductID from products
CREATE TABLE IF NOT EXISTS shirts (
    ProductID INTEGER PRIMARY KEY,
    FOREIGN KEY (ProductID) REFERENCES products(ProductID)
);

-- Pants table, referencing ProductID from products
CREATE TABLE IF NOT EXISTS pants (
    ProductID INTEGER PRIMARY KEY,
    FOREIGN KEY (ProductID) REFERENCES products(ProductID)
);

-- Accessories table, referencing ProductID from products
CREATE TABLE IF NOT EXISTS accessories (
    ProductID INTEGER PRIMARY KEY,
    FOREIGN KEY (ProductID) REFERENCES products(ProductID)
);

-- Shoes table, referencing ProductID from products
CREATE TABLE IF NOT EXISTS shoes (
    ProductID INTEGER PRIMARY KEY,
    FOREIGN KEY (ProductID) REFERENCES products(ProductID)
);

-- Outerwear table, referencing ProductID from products
CREATE TABLE IF NOT EXISTS outerwear (
    ProductID INTEGER PRIMARY KEY,
    FOREIGN KEY (ProductID) REFERENCES products(ProductID)
);

-- Dresses table, referencing ProductID from products
CREATE TABLE IF NOT EXISTS dresses (
    ProductID INTEGER PRIMARY KEY,
    FOREIGN KEY (ProductID) REFERENCES products(ProductID)
);

-- Formals table, referencing ProductID from products
CREATE TABLE IF NOT EXISTS formals (
    ProductID INTEGER PRIMARY KEY,
    FOREIGN KEY (ProductID) REFERENCES products(ProductID)
);
