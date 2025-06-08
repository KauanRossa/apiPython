import sqlite3

def connector():
    return sqlite3.connect("database.db")

def create_table():
    conn = connector()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            useremail TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            categ INTEGER,
            weight INTEGER,
            mass TEXT,
            qtde INTEGER NOT NULL,
            active INTEGER DEFAULT 1
        )
    """)

    conn.commit()
    conn.close()