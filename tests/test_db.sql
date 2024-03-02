/*SQLite schema and data to use for testing.*/

CREATE TABLE IF NOT EXISTS user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

INSERT INTO user (username, email, password) VALUES
  ("john.doe", "johndoe@example.com", "yourSecurePassword"),
  ("jane.smith", "janesmith@example.com", "anotherSecurePassword"),
  ("bob.johnson", "bob.johnson@example.com", "superSecurePassword");

ATTACH DATABASE ':memory:' AS 'sales';

CREATE TABLE sales.record (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  product TEXT UNIQUE NOT NULL,
  amount REAL NOT NULL
);

INSERT INTO sales.record (product, amount) VALUES
  ("Painted tile coaster", "3.50"),
  ("Silver bracelet", "18.00");