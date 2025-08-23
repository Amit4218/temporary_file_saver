from db.db import search_expired_files, SLEEP_TIME
import time
import os


def delete_files():

    try:

        while True:

            file_paths = search_expired_files()

            if not file_paths or file_path == []:
                time.sleep(SLEEP_TIME)

            for file_path in file_paths:

                if not os.path.exists(file_path):
                    continue
                else:
                    os.remove(file_path)

            time.sleep(SLEEP_TIME)

    except Exception as e:
        print(e)
