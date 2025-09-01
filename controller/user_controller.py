from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.user import UserCreate ,UserLogin
from  service.user_service import UserService, AuthError
from repositories.base import get_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserCreate)
def register(user: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        return service.register_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        token = service.login_user(user)
        return {"access_token": token, "token_type": "bearer"}
    except AuthError as e:
        raise HTTPException(status_code=401, detail=str(e))
