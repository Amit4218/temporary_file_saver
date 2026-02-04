import os
import uuid

from utils.constants import TEMP_FOLDER


def create_folder_for_file():
    try:
        if not os.path.exists(TEMP_FOLDER):
            os.mkdir(TEMP_FOLDER)

        unique_folder_name = str(uuid.uuid4())
        folder_path = os.path.join(TEMP_FOLDER, unique_folder_name)
        os.makedirs(folder_path, exist_ok=True)

        return (folder_path, unique_folder_name)
    except Exception as e:
        return f"<h1>{e}</h1>"
