-- WRITE DATABASE SCHEMAS HERE
-- NOTE: There can be a lot of syntax differences between MySQL and sqlite3

DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    ProductID INTEGER PRIMARY KEY,
    ProductName TEXT,
    ProductBrand TEXT,
    Gender TEXT,
    Price INTEGER,
    NumImages INTEGER,
    Description TEXT,
    PrimaryColor TEXT
);