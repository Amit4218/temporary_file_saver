from flask import Flask, render_template, request, send_from_directory, abort
from werkzeug.utils import secure_filename
from db.db import create_table, save_file_path
from clean_up_files import delete_files
from dotenv import load_dotenv
import threading
import uuid
import os

app = Flask(__name__)
load_dotenv()
ROOT_FOLDER = "temp"  # root directory for the folders and files
HOST_URL = os.getenv("HOST_BASE_URL")
MAX_FILE_SIZE = 30 * 1024 * 1024


def func():
    try:
        if not os.path.exists(ROOT_FOLDER):
            os.mkdir(ROOT_FOLDER)
        unique_folder_name = str(uuid.uuid4())
        folder_path = os.path.join(ROOT_FOLDER, unique_folder_name)
        os.makedirs(folder_path, exist_ok=True)
        return (folder_path, unique_folder_name)
    except Exception as e:
        return f"<h1>{e}</h1>"


def check_file_size(file):

    file.stream.seek(0, 2)
    size = file.stream.tell()

    file.stream.seek(0)

    if size > MAX_FILE_SIZE:
        return True

    return False


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api")
def api():
    return render_template("api.html", domain_name=HOST_URL)


@app.route("/upload", methods=["POST"])
def upload():

    try:

        if request.method == "POST":

            if "file" not in request.files:
                raise Exception("Oops did you forget to upload a file?")

            file = request.files["file"]

            if file.filename == "":
                raise Exception("No file was found")

            file_size = check_file_size(file)

            if file_size:
                raise Exception("File exceeds 30 MB limit")

            if file:
                folder_path, folder_id = func()
                file_name = secure_filename(file.filename)
                file_path = os.path.join(folder_path, file_name)
                file.save(file_path)

                file_url = f"{HOST_URL}/file/{folder_id}/{file_name}"

                path = f"{folder_path}/{file_name}"

                save_file_path(filename=file_name, path=path)

                return render_template(
                    "preview.html", file_url=file_url, file_name=file_name
                )

    except Exception as err:
        return render_template("error.html", error=err)


@app.route("/file/<folder>/<filename>", methods=["GET"])
def get_file(folder, filename):
    try:

        if request.method == "GET":

            folder_path = os.path.join(ROOT_FOLDER, folder)

            if not os.path.exists(os.path.join(folder_path, filename)):
                abort(404)

            return send_from_directory(folder_path, filename)
    except Exception as err:
        return render_template("error.html", error=err)


@app.route("/api/v1/upload", methods=["POST"])
def api_upload():
    try:

        if request.method == "POST":

            if "file" not in request.files:
                return "File not found", 404

            file = request.files["file"]

            file_size = check_file_size(file)

            if file_size:
                return "File exceeds 30 MB limit"

            if file:
                folder_path, folder_id = func()
                file_name = secure_filename(file.filename)
                file_path = os.path.join(folder_path, file_name)
                file.save(file_path)

                file_url = f"{HOST_URL}/file/{folder_id}/{file_name}"

                path = f"{folder_path}/{file_name}"

                save_file_path(filename=file_name, path=path)

                res_structure = {
                    "status": "Success",
                    "File_url": file_url,
                }

                return res_structure, 200

    except Exception as e:
        print(e)


def main():

    create_table()

    clean_up = threading.Thread(target=delete_files, daemon=True)
    clean_up.start()

    app.run(port=3000)


if __name__ == "__main__":
    main()
