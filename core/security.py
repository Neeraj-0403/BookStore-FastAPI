from datetime import datetime, timedelta
from typing import Optional
from jose import jwt,JWTError
from passlib.context import CryptContext
from core.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer,HTTPBearer, HTTPAuthorizationCredentials
from repositories.base import SessionLocal,get_db
import repositories.user_repository as repo


pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="users/login")

def create_access_token(subject:str, expires_minutes:Optional[int]=None) -> str:
    if expires_minutes is None:
        expires_minutes=settings.JWT_ACCESS_TOKEN_EXPIRES_MIN
    expire=datetime.now() +timedelta(minutes=expires_minutes)
    payload={"sub":subject,"exp":expire}
    return jwt.encode(payload,settings.JWT_SECRET,algorithm=settings.JWT_ALGORITHM)

def decode_token(token:str) -> Optional[str]:
    try:
        payload=jwt.decode(token,settings.JWT_SECRET,algorithms=settings.JWT_ALGORITHM)
        return payload
    except JWTError as ex:
        return None

def hash_password(password:str) -> bool:
    try:
        return pwd_context.hash(password)
    except Exception as ex:
        raise RuntimeError(f"Error hashing password: {ex}") from ex
    

def verify_password(plain:str,hashed:str) -> bool:
    return pwd_context.verify(plain,hashed)
 
# http bearer
bearer_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: SessionLocal = Depends(get_db),
):
    token = credentials.credentials
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    user = repo.UserRepository(db).get_by_email(payload.get("sub"))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user