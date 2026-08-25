import secrets

from fastapi import UploadFile, status

from src.db.db import Session
from src.exceptions import *
from src.models.file_path_table import FilePaths
from src.utils.settings import settings


def validate_file(file: UploadFile) -> None:
    
    if not file.file or not file.filename:
        raise UploadFileNotFoundError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Oops did you forget to upload a file?"
        )
        
        
    if file.size and file.size > settings.MAX_FILE_SIZE:
        raise FileSizeLimitExceedError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="File size exceeds the limit of 25mb"
        )
        

def generate_short_id(db_session: Session) -> str:
    
    while True:
        
        generated_id  = secrets.token_urlsafe(5)
        result = db_session.query(FilePaths).filter(FilePaths.short_id == generated_id).first()
        if not result:    
            return generated_id