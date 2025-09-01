from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from typing import List
from core.security import get_current_user

from service.book_service import BookService,NotFoundError
from schemas.book import BookCreate ,BookUpdate
from schemas.user import UserRead
from repositories import base
from domain.book_entity import BookEntity

router= APIRouter(prefix="/books",tags=["Books"])

@router.post("/",response_model=BookCreate)
def create_book(book: BookCreate,db :Session=Depends(base.get_db), current_user: UserRead = Depends(get_current_user)):
    try:
        service=BookService(db)
        return service.create_book(book)
    except Exception as ex:
         raise HTTPException(status_code=400,detail=str(ex))


@router.get("/{book_id}", response_model=BookEntity)
def get_book(book_id: int, db: Session = Depends(base.get_db), current_user: UserRead = Depends(get_current_user)):
    service = BookService(db)
    try:
        return service.get_book(book_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/", response_model=List[BookEntity])
def list_books(skip: int = 0, limit: int = 10, db: Session = Depends(base.get_db), current_user: UserRead = Depends(get_current_user)):
    service = BookService(db)
    return service.get_book_list(skip=skip, limit=limit)

@router.put("/{book_id}", response_model=BookEntity)
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(base.get_db), current_user: UserRead = Depends(get_current_user)):
    service = BookService(db)
    try:
        return service.update_book(book_id, book)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{book_id}", response_model=dict)
def delete_book(book_id: int, db: Session = Depends(base.get_db), current_user: UserRead = Depends(get_current_user)):
    service = BookService(db)
    try:
        response= service.delete_book(book_id)
        return response
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))