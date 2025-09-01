import logging
from sqlalchemy.orm import Session
from typing import List,Optional
from models.book import Book
from schemas.book import  BookUpdate

logger=logging.getLogger(__name__)

class BookRepository:
    def __init__(self,db:Session):
        self.db=db

    def create(self,title:str,author:str,description:str | None) -> Book:
        try:
            book= Book(title=title,author=author,description=description)
            self.db.add(book)
            self.db.commit()
            self.db.refresh(book)
            return book
        except Exception as ex:
            self.db.rollback()
            logger.exception("Failed to create book")
            raise

    def get(self,book_id:int) -> Optional[Book]:
        return self.db.query(Book).filter(Book.id==book_id).first()

    def list(self, skip: int, limit: int) -> List[Book]:
        return self.db.query(Book).order_by(Book.id.desc()).offset(skip).limit(limit).all()

    def update(self,book_id:int,book_update:BookUpdate) -> Optional[Book]:
        try:
            book=self.get(book_id) 
            if book is None:
              raise ValueError(f"Book with id {book_id} not found") 
            
                # Convert Pydantic model to dict, skip None fields
            update_data = book_update.model_dump(exclude_unset=True)

            # Apply updates dynamically
            for key, value in update_data.items():
                setattr(book, key, value)

            self.db.commit()
            self.db.refresh(book)
            return book
        except Exception as ex:
            self.db.rollback()
            logger.exception("Failed to update book")
            raise

    def delete(self, book_id:int) -> bool:
        try:
            book=self.get(book_id)
            if not book:
                return False
            self.db.delete(book)
            self.db.commit() 
            return True
        except Exception as ex:
            self.db.rollback()
            logger.exception("Failed to delete book")
            raise