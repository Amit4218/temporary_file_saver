import cloudinary
import cloudinary.uploader
from fastapi import UploadFile, status
from pydantic import BaseModel

from src.exceptions import CloudinaryFileUploadError
from src.utils.settings import settings


class UpladFileResponse(BaseModel):
    asset_id: str 
    public_id: str
    resource_type: str
    secure_url: str
    width: int
    height: int
    format:str


class CloudinaryService:
    def __init__(self) -> None:
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
            secure=True,
        )

        self.cloudinary = cloudinary

    def upload_user_file(self, file: UploadFile, id:str) -> UpladFileResponse:
        
        response = self.cloudinary.uploader.upload(
            file=file.file,
            resource_type="auto",
            public_id=id
        )
        
        if not response["secure_url"]:
            raise CloudinaryFileUploadError(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error uploading file to cloudinary!"
            )
        
        return UpladFileResponse(**response)
        
        
    def delete_file(self, id:str, type:str) -> bool:
        response = self.cloudinary.uploader.destroy(
            public_id=id,
            resource_type=type
        )
        
        return response["result"] == "ok"
    
    
cloudinary_service = CloudinaryService()