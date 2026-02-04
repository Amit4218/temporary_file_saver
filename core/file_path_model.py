from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from config import db


class Filepath(db.Model):  # ty:ignore[unsupported-base]
    __tablename__ = "file_paths"

    file_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now, nullable=False, index=True, primary_key=True
    )
