from sqlalchemy import Column, String, Integer, Boolean, VARCHAR, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.db.db import Base
from datetime import datetime, timezone

class TodoSchema(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    content: Mapped[str] = mapped_column(String, nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, onupdate=datetime.now(timezone.utc))