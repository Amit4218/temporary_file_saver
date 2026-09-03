from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import Depends, FastAPI, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from logger import app_logger
from src.db.db import Base, Session, engine, get_db
from src.http_response_models.responses import *
from src.models.file_path_table import FilePaths
from src.services.cloudinary_service import cloudinary_service
from src.utils.background_job import search_expired_files_and_delete
from src.utils.settings import settings
from src.utils.validations import generate_short_id, validate_file


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        search_expired_files_and_delete,
        trigger="interval",
        minutes=1,
        id="db_check_and_files_clean_up",
        replace_existing=True,
    )

    scheduler.start()

    app_logger.info("[CRON] scheduler started")

    try:
        yield
    finally:
        scheduler.shutdown()
        app_logger.info("[CRON] scheduler shutting down")
        
        
app = FastAPI(lifespan=lifespan, docs_url=None, openapi_url=None, redoc_url=None)
Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return RouteNotFoundResponse()



@app.get("/api/health")
async def root() -> HealthCheckResponse:
    return HealthCheckResponse(status="ok", message="Service is running")



@app.post("/api/v1/upload")
async def upload(
    file: UploadFile,
    db: Session = Depends(get_db) # noqa: B008
) -> FileUploadResponse: 
    
    validate_file(file)
    
    short_id = generate_short_id(db_session=db)
    
    result = cloudinary_service.upload_user_file(file, id=short_id)
    
    file_details = FilePaths(
        short_id=short_id,
        asset_id=result.asset_id,
        public_id=result.public_id,
        resource_type=result.resource_type,
        secure_url=result.secure_url,
        original_filename=file.filename,
        format=result.format,
        height=result.height,
        width=result.width
    )
    
    db.add(file_details)
    db.commit()
    
    final_url = f'{settings.HOST_URL}/f/{short_id}'
    
    return FileUploadResponse(status="success", url=final_url)


@app.get("/f/{id}/",response_model_exclude_none=True)
async def get_file(
    id:str,
    stats: bool = False,
    db: Session = Depends(get_db) # noqa: B008
) -> FileStatsResponse | FileDetailsNotFoundResponse:  
    
    if not stats:
        file_url = db.execute(db.query(FilePaths.secure_url).where(FilePaths.short_id == id)).scalar()
        
        if file_url:
            return FileStatsResponse(status="success", data=None, url=file_url)
    
    
    if stats:
        file_stats = db.execute(db.query(FilePaths).where(FilePaths.short_id == id)).scalar()
        
        
        if  file_stats:
            data = FilePathsResponse.model_validate(file_stats)
            
            return FileStatsResponse(
                status="success",
                data=data,
                url=None
            )
    
    return FileDetailsNotFoundResponse(status="fail", message="File not found")