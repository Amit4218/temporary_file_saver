from datetime import datetime

from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict


class RouteNotFoundResponse(JSONResponse):
    def __init__(self):
        super().__init__(
            status_code=404,
            content={"detail": "Route not found"},
        )


class BaseResponse(BaseModel):
    status: str | int
    message: str

class HealthCheckResponse(BaseResponse):
    ...
    

class FileUploadResponse(BaseModel):
    status: str
    url: str | None = None
    
    
class FilePathsResponse(BaseModel):
    
    model_config = ConfigDict(from_attributes=True)
    
    short_id: str
    resource_type: str
    secure_url: str
    original_filename: str
    format: str | None = None
    height: int |  None = None
    width: int | None = None
    created_at: datetime
    
class FileStatsResponse(BaseModel):
    status: str
    data: FilePathsResponse | None = None
    url: str | None = None
    

class FileDetailsNotFoundResponse(BaseModel):
    status: str
    message: str 