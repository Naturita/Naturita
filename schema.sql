DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS sales;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    price TEXT,
    quantity_unit TEXT,
    extra_info TEXT,
    image_url TEXT
);

CREATE TABLE sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    total REAL NOT NULL,
    items TEXT NOT NULL, -- JSON string
    customer_info TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
