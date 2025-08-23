from datetime import datetime, timedelta
import sqlite3



SLEEP_TIME = 86400  # 24 hours in seconds


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

        old_files = []

        cursor, connection = connect_to_database()

        # searching the db for file paths where the creation has exceeded 1 day (<=) -1 day

        cursor.execute(
            """
            SELECT * 
            FROM file_paths
            WHERE created_at <= datetime('now', '-1 day') 
            """
        )

        rows = cursor.fetchall()
        for row in rows:
            created_at = datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S")

            # Check if the file is 1 day old or more
            if created_at <= datetime.now() - timedelta(days=1):
                old_files.append(row[2])

        connection.close()

        return old_files

    except Exception as e:
        print(e)


