from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import timezone, datetime
import jwt

from app.db.session import get_db
from app.models.user import User, RefreshToken
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse
from app.core.security import verify_password
from app.services.auth_service import create_user, create_user_tokens
from app.core.config import settings

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Register a new user.
    """
    return await create_user(db, user_in)


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """
    Authenticate a user and return access and refresh tokens.
    """
    query = select(User).where(User.email == form_data.username)
    result = await db.execute(query)
    user = result.scalars().first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return await create_user_tokens(db, str(user.id))


@router.post("/refresh", response_model=Token)
async def refresh_token( refresh_token: str, db: AsyncSession = Depends(get_db)):
    """
    Refresh access and refresh tokens using a valid refresh token.
    """
    query = select(RefreshToken).where(RefreshToken.token == refresh_token, RefreshToken.is_revoked == False)
    result = await db.execute(query)
    token_record = result.scalars().first()

    if not token_record or token_record.expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authentiacte": "Bearer"}
        )
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token_record.is_revoked = True
    await db.commit()

    return await create_user_tokens(db, user_id)
    