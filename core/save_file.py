import os

from werkzeug.utils import secure_filename

from utils.check_file_size import check_file_size
from utils.constants import HOST_URL
from utils.create_folder_for_file import create_folder_for_file
from utils.save_file_path import save_file_path


def save_file_in_server(request):
    if "file" not in request.files:
        return None, "Oops did you forget to upload a file?"

    file = request.files["file"]

    if file.filename == "":
        return None, "No file was found"

    file_size = check_file_size(file)

    if file_size:
        return None, "File exceeds 30 MB limit"

    folder_path, folder_id = create_folder_for_file()
    file_name = secure_filename(file.filename)
    file_path = os.path.join(folder_path, file_name)
    file.save(file_path)

    file_url = f"{HOST_URL}/file/{folder_id}/{file_name}"

    path = f"{folder_path}/{file_name}"

    save_file_path(filename=file_name, path=path)

    result = {"url": file_url, "name": file_name}

    return result, None
