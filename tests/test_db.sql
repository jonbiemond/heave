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