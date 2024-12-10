CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year TEXT,
    status TEXT DEFAULT 'unread',
    cover_image TEXT,
    summary TEXT
);
