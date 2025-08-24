from datetime import datetime, timedelta
import sqlite3


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
            INSERT INTO file_paths (file_name, path) 
            VALUES (?, ?)
            """,
            (filename, path),
        )

        connection.commit()
        connection.close()

    except Exception as e:
        print(e)


def search_expired_files():

    try:

        old_files_paths = []

        cursor, connection = connect_to_database()

        # searching the db for file paths where the creation has exceeded 60 minutes

        cursor.execute(
            """
            SELECT * 
            FROM file_paths
            WHERE created_at <= datetime('now', '-60 minutes') 
            """
        )

        rows = cursor.fetchall()
        for row in rows:
            old_files_paths.append(row[2])

        connection.close()

        return old_files_paths

    except Exception as e:
        print(e)


def clean_db_records():

    try:

        cursor, connection = connect_to_database()

        cursor.execute(
            """
        DELETE FROM file_paths WHERE created_at <= datetime('now', '-60 minutes')
        """
        )

        connection.commit()
        connection.close()

    except Exception as e:
        print(e)
