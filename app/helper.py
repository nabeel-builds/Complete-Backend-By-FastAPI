from pwdlib import PasswordHash
import jwt
from app.config.app_config import getAppConfig
from datetime import datetime, timezone, timedelta

def hashPassword(password: str) -> str:
    password_hash = PasswordHash.recommended()
    return password_hash.hash(password)

def verifyPassword(password: str, hashed_password: str) -> bool:
    password_hash = PasswordHash.recommended()
    return password_hash.verify(password, hashed_password)

def createAccessToken(data: dict, expiresInMinutes: int = 30) -> str:
    config = getAppConfig()
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expiresInMinutes)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, config.secret_key, algorithm=config.algorithm or "HS256")
    return encode_jwt

def decodeAccessToken(token: str) -> dict:
    config = getAppConfig()
    payload = jwt.decode(token, config.secret_key, algorithms=[config.algorithm or "HS256"])
    return payload
    