from pwdlib import PasswordHash

def hashPassword(password: str) -> str:
    password_hash = PasswordHash.recommended()
    return password_hash.hash(password)

def verifyPassword(password: str, hashed_password: str) -> bool:
    password_hash = PasswordHash.recommended()
    return password_hash.verify(password, hashed_password)