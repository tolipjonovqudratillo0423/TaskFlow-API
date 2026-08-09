import jwt


from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash

from app.core.config import settings

def set_password(plain_password: str) -> str:
    
    password_hash = PasswordHash.recommended()
    
    hashed = password_hash.hash(plain_password)
    
    return hashed


def check_password(plain_password, hashed: str) -> bool:
    
    password_hash = PasswordHash.recommended()
    
    return password_hash.verify(plain_password, hashed)


def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_minutes)
    payload = {"sub": str(user_id), "exp": expire, "type": "access"}
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")


def create_refresh_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.refresh_token_minutes)
    payload = {"sub": str(user_id), "exp": expire, "type": "refresh"}
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")


