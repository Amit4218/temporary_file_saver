import os
from datetime import datetime, timedelta

from sqlalchemy import select

from config.database import db
from core.file_path_model import Filepath


def delete_files(file_paths) -> None:
    for file_path in file_paths:
        if os.path.exists(file_path):
            os.remove(file_path)

        folder = os.path.dirname(file_path)
        if os.path.isdir(folder) and not os.listdir(folder):
            os.rmdir(folder)


def search_expired_files_and_delete() -> None:
    """Searches for file whose created_at exceeds 60 minutes and deletes it."""

    expired_time = datetime.now() - timedelta(minutes=60)

    expired_files = (
        db.session.execute(select(Filepath).where(Filepath.created_at <= expired_time))
        .scalars()
        .all()
    )

    if not expired_files:
        return

    file_paths = [fp.path for fp in expired_files]

    delete_files(file_paths)

    for fp in expired_files:
        db.session.delete(fp)

    db.session.commit()
