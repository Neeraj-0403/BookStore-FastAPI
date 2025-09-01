
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
import logging

class UserRepository:
    """Repository layer for user persistence."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, user: UserCreate) -> User:
        try:
            """Create a new user in the database."""
            db_user = User(
                username=user.username,
                email=user.email,
                password_hash=user.password
            )
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            logging.debug("User created successfully")
            return db_user
        except Exception as ex:
            raise RuntimeError(f"Error user repository: {ex}") from ex

    def get_by_id(self, user_id: int) -> User | None:
        """Retrieve a user by id."""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> User | None:
        """Retrieve a user by email."""
        return self.db.query(User).filter(User.email == email).first()

    def list(self, skip: int = 0, limit: int = 10) -> list[User]:
        """List users with pagination."""
        return self.db.query(User).offset(skip).limit(limit).all()

    def delete(self, user_id: int) -> bool:
        """Delete a user by id."""
        db_user = self.get_by_id(user_id)
        if not db_user:
            return False
        self.db.delete(db_user)
        self.db.commit()
        return True
