from flask import Flask, render_template, request, send_from_directory, abort
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import uuid
import os

app = Flask(__name__)
ROOT_FOLDER = "temp"
load_dotenv()


def func():
    try:
        unique_folder_name = str(uuid.uuid4())
        folder_path = os.path.join(ROOT_FOLDER, unique_folder_name)
        os.makedirs(folder_path, exist_ok=True)
        return (folder_path, unique_folder_name)
    except Exception as e:
        return f"<h1>{e}</h1>"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    try:

        if request.method == "POST":

            if "file" not in request.files:
                raise Exception("Oops did you forget to upload a file?")

            file = request.files["file"]

            if file.filename == "":
                raise Exception("No file was found")

            if file:
                folder_path, folder_id = func()
                file_name = secure_filename(file.filename)
                file_path = os.path.join(folder_path, file_name)
                file.save(file_path)

                file_url = f"{os.getenv('HOST_BASE_URL')}/file/{folder_id}/{file_name}"

                html = f"<h3><a href={file_url} target='_blank'>{file_url}</a></h3>"

                return render_template("preview.html")

    except Exception as err:
        return render_template("error.html", error=err)


@app.route("/file/<folder>/<filename>", methods=["GET"])
def get_file(folder, filename):
    try:

        if request.method == ["GET"]:

            folder_path = os.path.join(ROOT_FOLDER, folder)

            if not os.path.exists(os.path.join(folder_path, filename)):
                abort(400)

            return send_from_directory(folder_path, filename)
    except Exception as err:
        return render_template("error.html", error=err)


if __name__ == "__main__":
    app.run(port=3000, debug=True)
