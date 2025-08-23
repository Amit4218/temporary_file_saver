import sqlite3
import os


def connect_to_database():
    try:

        connection = sqlite3.connect("filePath.db")
        return (connection.cursor(), connection)

    except Exception as e:
        print(f"Error in Connecting to db: {e}")


def create_table():

    try:

        cursor, connection = connect_to_database()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS file_paths (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_name TEXT DEFAULT '',
                path TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        connection.commit()
        connection.close()

    except Exception as e:
        print(f"Error in creating the table: {e}")


def save_file_path(filename, path):
    try:

        cursor, connection = connect_to_database()

        cursor.execute(
            """
            INSERT INTO file_paths (filename, path) VALUES ( ?, ?)

            """,
            (filename, path),
        )

        connection.commit()
        connection.close()

    except Exception as e:
        print(e)


save_file_path("test.txt", "/temp/test")
