import sqlite3

"""
    TYPE user:
    0 - user
    1 - vendor
    2 - admin

    ACTIVE user/item:
    0 - inactive
    1 - active
"""

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
            password TEXT NOT NULL,
            type INTEGER DEFAULT 0,
            token TEXT,
            active INTEGER DEFAULT 1
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
            quantity INTEGER NOT NULL,
            active INTEGER DEFAULT 1
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS addresses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            street TEXT NOT NULL,
            number INTEGER,
            complement TEXT,
            neighborhood TEXT NOT NULL,
            city TEXT NOT NULL,
            state TEXT NOT NULL,
            zip_code TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            active INTEGER DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cartitem (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cart_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (cart_id) REFERENCES cart (id),
            FOREIGN KEY (item_id) REFERENCES items (id)
        )
    """)

    """ Criar tabela de endereco por cliente, varios enderecos por cliente """

    conn.commit()
    conn.close()