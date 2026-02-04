import os

from flask import Flask, render_template, request, send_from_directory
from flask_apscheduler import APScheduler

from config import db
from core.save_file import save_file_in_server
from utils.constants import DATABASE_URL, HOST_URL, MAX_FILE_SIZE, TEMP_FOLDER
from utils.task_scheduler import start_background_tasks

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
scheduler = APScheduler()


db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/api", methods=["GET"])
def api():
    return render_template("api.html", domain_name=HOST_URL)


@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


@app.route("/upload", methods=["POST"])
def upload():
    result, error = save_file_in_server(request=request)

    if error:
        return render_template("error.html", error=error)

    return render_template(
        "preview.html", file_url=result["url"], file_name=result["name"]
    )


@app.route("/file/<folder>/<filename>", methods=["GET"])
def get_file(folder, filename):
    folder_path = os.path.join(TEMP_FOLDER, folder)

    if not os.path.exists(os.path.join(folder_path, filename)):
        return render_template("error.html", error="Item Not Found!")

    return send_from_directory(folder_path, filename)


@app.route("/api/v1/upload", methods=["POST"])
def api_upload():
    result, error = save_file_in_server(request=request)

    if error:
        return render_template("error.html", error=error)

    res_structure = {
        "status": "Success",
        "File_url": result["url"],
    }

    return res_structure, 200


if __name__ == "__main__":
    start_background_tasks(scheduler=scheduler, app=app)
    app.run(host="0.0.0.0")
