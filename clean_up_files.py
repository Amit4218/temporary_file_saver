import time
import os
import logging
from db.db import search_expired_files, clean_db_records

SLEEP_TIME = 3600  # 60 minutes


def delete_files():
    while True:
        try:
            file_paths = search_expired_files()

            for file_path in file_paths:
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)

                    folder = os.path.dirname(file_path)
                    if os.path.isdir(folder) and not os.listdir(folder):
                        os.rmdir(folder)

                except Exception as e:
                    logging.exception(f"Failed to delete {file_path}: {e}")

            clean_db_records()

        except Exception as e:
            logging.exception(f"Error in delete_files loop: {e}")

        time.sleep(SLEEP_TIME)
