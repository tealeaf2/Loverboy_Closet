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
    Material TEXT DEFAULT NULL,
    FOREIGN KEY (ProductID) REFERENCES products(ProductID)
);

CREATE VIEW IF NOT EXISTS shirts_view AS
SELECT products.*, shirts.ProductID AS ShirtProductID, shirts.Material
FROM products
JOIN shirts ON products.ProductID = shirts.ProductID;

-- Pants table, referencing ProductID from products
CREATE TABLE IF NOT EXISTS pants (
    ProductID INTEGER PRIMARY KEY,
    WaistLength FLOAT DEFAULT 0,
    FOREIGN KEY (ProductID) REFERENCES products(ProductID)
);

CREATE VIEW IF NOT EXISTS pants_view AS
SELECT products.*, pants.ProductID AS PantProductID, pants.WaistLength
FROM products
JOIN pants ON products.ProductID = pants.ProductID;

-- Accessories table, referencing ProductID from products
CREATE TABLE IF NOT EXISTS accessories (
    ProductID INTEGER PRIMARY KEY,
    SizeinCM FLOAT DEFAULT 0,
    FOREIGN KEY (ProductID) REFERENCES products(ProductID)
);

CREATE VIEW IF NOT EXISTS accessories_view AS
SELECT products.*, accessories.ProductID AS AccessoryProductID, accessories.SizeinCM
FROM products
JOIN accessories ON products.ProductID = accessories.ProductID;

-- Shoes table, referencing ProductID from products
CREATE TABLE IF NOT EXISTS shoes (
    ProductID INTEGER PRIMARY KEY,
    Comfort TEXT DEFAULT NULL,
    FOREIGN KEY (ProductID) REFERENCES products(ProductID)
);

CREATE VIEW IF NOT EXISTS shoes_view AS
SELECT products.*, shoes.ProductID AS ShoeProductID, shoes.Comfort
FROM products
JOIN shoes ON products.ProductID = shoes.ProductID;

-- Outerwear table, referencing ProductID from products
CREATE TABLE IF NOT EXISTS outerwear (
    ProductID INTEGER PRIMARY KEY,
    Thickness TEXT DEFAULT NULL,
    FOREIGN KEY (ProductID) REFERENCES products(ProductID)
);

CREATE VIEW IF NOT EXISTS outerwear_view AS
SELECT products.*, outerwear.ProductID AS OuterwearProductID, outerwear.Thickness
FROM products
JOIN outerwear ON products.ProductID = outerwear.ProductID;

-- Dresses table, referencing ProductID from products
CREATE TABLE IF NOT EXISTS dresses (
    ProductID INTEGER PRIMARY KEY,
    Design TEXT DEFAULT NULL,
    FOREIGN KEY (ProductID) REFERENCES products(ProductID)
);

CREATE VIEW IF NOT EXISTS dresses_view AS
SELECT products.*, dresses.ProductID AS DressProductID, dresses.Design
FROM products
JOIN dresses ON products.ProductID = dresses.ProductID;

-- Formals table, referencing ProductID from products
CREATE TABLE IF NOT EXISTS formals (
    ProductID INTEGER PRIMARY KEY,
    Pockets INTEGER DEFAULT 0,
    FOREIGN KEY (ProductID) REFERENCES products(ProductID)
);

CREATE VIEW IF NOT EXISTS formals_view AS
SELECT products.*, formals.ProductID AS FormalProductID, formals.Pockets
FROM products
JOIN formals ON products.ProductID = formals.ProductID;