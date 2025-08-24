from db.db import search_expired_files, clean_db_records
import time
import os

SLEEP_TIME = 3600  # 60 minutes in seconds


def delete_files():

    try:

        while True:

            file_paths = search_expired_files()

            if not file_paths:
                time.sleep(SLEEP_TIME)

            for file_path in file_paths:

                if not os.path.exists(file_path):
                    continue
                else:
                    os.remove(f"{file_path}")
                    split_path = file_path.split("/")
                    folder = os.path.join(f"{split_path[0]}/{split_path[1]}")
                    os.rmdir(folder)

            clean_db_records()

            time.sleep(SLEEP_TIME)

    except Exception as e:
        print(e)
