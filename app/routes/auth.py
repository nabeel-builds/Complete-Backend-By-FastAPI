from fastapi import APIRouter, Depends
from app.models.auth import Register
from sqlalchemy.orm import Session
from typing import Annotated
from app.db.db import get_db
from app.db.schemas.user_schema import UserSchema
from fastapi.responses import JSONResponse
from app.helper import hashPassword

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
        password = hashPassword(data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "user": new_user}