from sqlalchemy import Integer, String, Boolean, DateTime, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column
from app.db.db import Base
from datetime import datetime, timezone

class UserSchema(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(VARCHAR(100), nullable=False, index=True)
    email: Mapped[str] = mapped_column(VARCHAR(191), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, onupdate=datetime.now(timezone.utc))
