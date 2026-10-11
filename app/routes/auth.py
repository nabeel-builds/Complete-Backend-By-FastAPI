from fastapi import APIRouter, Depends
from app.models.auth import Register, Login
from sqlalchemy.orm import Session
from typing import Annotated
from app.db.db import get_db
from app.db.schemas.user_schema import UserSchema
from fastapi.responses import JSONResponse
from app.helper import hashPassword, verifyPassword, createAccessToken

router = APIRouter(prefix="/auth")

@router.post("/register")
def register(data: Register, db:Annotated[Session, Depends(get_db)]):
    # Checking if user with the same email is already exists or not
    existing_user = db.query(UserSchema).filter(UserSchema.email == data.email).first()
    if existing_user:
        return JSONResponse({"message": "User already exists with this email"}, status_code=400)

    # Create new user
    new_user = UserSchema(
        name = data.name,
        email = data.email,
        hashed_password = hashPassword(data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "user": new_user}


@router.post("/login")
def login(data:Login, db:Annotated[Session, Depends(get_db)]):
    user = db.query(UserSchema).filter(UserSchema.email == data.email).first()
    if not user or not verifyPassword(data.password, user.hashed_password):
        return JSONResponse(
            {"message": "Inavlid email or password"}, status_code=401
        )

    payload = {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }

    token = createAccessToken(payload)
    payload["access_token"] = "Bearer"+token
    
    return {"message": "Login Successful", "data": payload}