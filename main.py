from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import Depends, FastAPI, UploadFile

from logger import app_logger
from src.db.db import Base, Session, engine, get_db
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


@app.get("/api/healthz")
async def root() -> dict:
    return {"status":"ok"}


@app.post("/api/v1/upload")
async def upload(file: UploadFile, db: Session = Depends(get_db)): # noqa: B008
    
    validate_file(file)
    
    short_id = generate_short_id(db_session=db)
    
    result = cloudinary_service.upload_user_file(file, id=short_id)
    
    file_details = FilePaths(
        short_id=short_id,
        asset_id=result.asset_id,
        public_id=result.public_id,
        resource_type=result.resource_type,
        secure_url=result.secure_url
    )
    
    db.add(file_details)
    db.commit()
    
    final_url = f'{settings.HOST_URL}/{short_id}'
    
    return {"status":"success", "url":final_url}


@app.get("/{id}")
async def get_file(id:str, db: Session = Depends(get_db)): # noqa: B008
    file_url = db.execute(db.query(FilePaths.secure_url).where(FilePaths.short_id == id)).scalar()
    if file_url:
        return {"status":"success","url":file_url}
    
    return {"status":"fail", "url":None}