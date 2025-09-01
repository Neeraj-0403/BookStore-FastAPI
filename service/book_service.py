import logging 
from typing import List,Optional
from sqlalchemy.orm import Session
from core.exceptions import NotFoundError
from domain.book_entity import BookEntity
from schemas.book import BookCreate,BookUpdate
from repositories.book_repository import BookRepository

logger= logging.getLogger(__name__)

class BookService:

    def __init__(self, db:Session):
        self.repo=BookRepository(db)
        self.db=db
        self._logger=logger

    def create_book(self,book:BookCreate) -> BookEntity:
        if not book.title and not book.author:
            raise ValueError("Both title and author are required")
        
        try:
            book=self.repo.create(title=book.title,author=book.author,description=book.description)
            self._logger.info("Book created", extra={"book_id":book.id,"title":book.title})
            return BookEntity(id=book.id,title=book.title,description=book.description,author=book.author, created_at=book.created_at)
        except Exception:
            self._logger.exception("Failed to create book in the service")
            raise
    
    def get_book(self, book_id:int) -> BookEntity:
        book = self.repo.get(book_id)
        if not book :
            self._logger.debug("Book not found", extra={"book_id":book_id})
            raise NotFoundError("Book not found")
        return BookEntity(id=book.id,title=book.title,description=book.description,author=book.author,created_at=book.created_at)

    def get_book_list(self,skip:int, limit:int) -> List[BookEntity]:
        books = self.repo.list(skip=skip, limit=limit)
        if not books :
            self._logger.debug("Book list are not found in the service")
            raise NotFoundError("Book list are not found in the service")
        return [BookEntity(id=book.id,title=book.title,description=book.description,author=book.author, created_at=book.created_at)
            for book in books
            ]
    
    def delete_book(self , book_id:int) -> dict:
        book=self.repo.delete(book_id)
        if not book:
            self._logger.debug("Book not found",extra={"book_id":book_id})
            raise NotFoundError("Book not found")
        return {"message": f"Book with id {book_id} deleted successfully."}
    
    def update_book(self,book_id:int,book:BookUpdate) -> BookEntity: 
        book = self.repo.update(book_id, book)
        try:
            if not book:
                self._logger.debug("Book not found")
            return BookEntity(id=book.id,title=book.title,description=book.description,author=book.author, created_at=book.created_at)
        except Exception:
                self._logger.exception("Failed to update book in the service")
                raise
