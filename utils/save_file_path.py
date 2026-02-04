from config.database import db
from core.file_path_model import Filepath


def save_file_path(filename, path):
    """Saves the filename and path to the database file_path table"""
    file_record = Filepath(file_name=filename, path=path)

    db.session.add(file_record)
    db.session.commit()
    db.session.refresh(file_record)
