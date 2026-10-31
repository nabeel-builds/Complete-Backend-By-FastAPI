from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from datetime import datetime, timezone

from app.models.user import User, RefreshToken
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, create_access_token, create_refresh_token

async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    # Check if the user already exists
    result = await db.execute(select(User).where(User.email == user_in.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )


    # Hash the password
    hashed_password = get_password_hash(user_in.password)


    # Create a new user instance
    new_user = User(
        email = user_in.email,
        hashed_password = hashed_password,
        is_active = True,
        is_verified = False,
    )


    # Add the new user to the database
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user




async def create_user_token(db: AsyncSession, user_id: User) -> dict:
    # Create access and refresh tokens
    access_token = create_access_token(data={"sub": user_id})
    refresh_token = create_refresh_token(data={"sub": user_id})

    # Store the refresh token in the database
    