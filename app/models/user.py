from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Uuid
import uuid
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    oauth_accounts = relationship("OauthAccount", back_populates="user", cascade="all, delete-orphan")
    refresh_token = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")



class OauthAccount(Base):
    __tablename__ = "oauth_accounts"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False, ondelete="CASCADE")
    provider = Column(String, nullable=False)
    provider_account_id = Column(String, nullable=False)

    user = relationship("User", back_populates="oauth_accounts")




class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    token = Column(String, nullable=False, primary_key=True)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False, ondelete="CASCADE")
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_revoked = Column(Boolean, default=False)

    user = relationship("User", back_populates="refresh_tokens")