from collections.abc import Sequence
from datetime import datetime, timedelta

from sqlalchemy import select

from logger import app_logger
from src.db.db import Session, get_db
from src.models.file_path_table import FilePaths
from src.services.cloudinary_service import cloudinary_service


def delete_expired_files(expired_files: Sequence[FilePaths] ,db: Session,) -> None:
    
    deleted_count = 0
    
    for file in expired_files:
        
        deleted = cloudinary_service.delete_file(
            id=str(file.public_id),
            type=str(file.resource_type),
        )
        
        app_logger.info(f"[CRON] attempted to delete file: {deleted}")

        if deleted:
            deleted_count += 1
            db.delete(file)

    app_logger.info("[CRON] file clean-up successfull total file deleted: %s", deleted_count)
    db.commit()


def search_expired_files_and_delete() -> None:
    """Find and delete files older than 60 minutes."""

    db = next(get_db())

    try:
        expired_time = datetime.now() - timedelta(minutes=60)  # noqa: DTZ005

        query = select(FilePaths).where(
            FilePaths.created_at <= expired_time
        )

        expired_files = db.execute(query).scalars().all()
        
        if not expired_files:
            app_logger.info("[CRON] no files found for cleanup, exiting now...")
            return

        delete_expired_files(expired_files, db)

    except Exception:
        db.rollback()
        app_logger.exception("[CRON] error ocurred during file clean ups!")
        raise

    finally:
        db.close()