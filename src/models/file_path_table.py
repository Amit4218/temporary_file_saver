from datetime import datetime

from sqlalchemy import Column, DateTime, String

from src.db.db import Base


class FilePaths(Base):
    __tablename__ = "file_paths"
    
    short_id = Column(String, primary_key=True, unique=True, nullable=False, index=True)
    asset_id = Column(String, unique=True, nullable=False)
    public_id = Column(String, unique=True, nullable=False)
    resource_type = Column(String, nullable=False)
    secure_url = Column(String, unique=True, nullable=False)
    original_filename = Column(String, nullable=False)
    format = Column(String, nullable=False)
    height = Column(String, nullable=True, )
    width = Column(String, nullable=True)
    created_at = Column(DateTime(), default=datetime.now, nullable=False)