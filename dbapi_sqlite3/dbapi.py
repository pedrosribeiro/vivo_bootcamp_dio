import sqlite3
from pathlib import Path

ROOT_PATH = Path(__file__).parent

conn = sqlite3.connect(ROOT_PATH / "clients.db")

cursor = conn.cursor()
cursor.row_factory = sqlite3.Row


def transaction(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
            conn.commit()
        except Exception as e:
            print(
                f"\nException: {e}, Function: {func.__name__}, Args: {args, kwargs}\n"
            )
            conn.rollback()

    return wrapper


@transaction
def create_table(conn, cursor):
    cursor.execute(
        "CREATE TABLE clients (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(100), email VARCHAR(150) UNIQUE);"
    )


@transaction
def insert_entry(conn, cursor, name, email):
    data = (name, email)
    cursor.execute("INSERT INTO clients (name, email) VALUES (?, ?);", data)


@transaction
def insert_entries(conn, cursor, data):
    cursor.executemany("INSERT INTO clients (name, email) VALUES (?, ?);", data)


@transaction
def update_entry(conn, cursor, name, email, id):
    data = (name, email, id)
    cursor.execute("UPDATE clients SET name=?, email=? WHERE id=?;", data)


@transaction
def delete_entry(conn, cursor, id):
    data = (id,)
    cursor.execute("DELETE FROM clients WHERE id=?;", data)


def retrieve_client(conn, cursor, id):
    cursor.execute("SELECT * FROM clients WHERE id=?", (id,))
    return cursor.fetchone()


def retrieve_clients(conn, cursor):
    return cursor.execute("SELECT * FROM clients;")


""""
insert_entries(
    conn,
    cursor,
    [
        ("Maria", "maria@test.com"),
        ("Marina", "marina@test.com"),
        ("Guilherme", "guilherme@test.com"),
    ],
)
"""

insert_entry(conn, cursor, "Pedro", "pedro@test2.com")

clients = retrieve_clients(conn, cursor)
for client in clients:
    print(dict(client))
