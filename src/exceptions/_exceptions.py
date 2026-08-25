from fastapi import HTTPException


class BaseFileUploadException(HTTPException):
    def __init__(self, status_code: int, detail: str | None = None) -> None:
        super().__init__(status_code, detail)


class UploadFileNotFoundError(BaseFileUploadException):
    ...

class FileSizeLimitExceedError(BaseFileUploadException):
    ...
    
class CloudinaryFileUploadError(BaseFileUploadException):
    ...