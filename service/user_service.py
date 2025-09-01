from sqlalchemy.orm import Session
from repositories.user_repository import UserRepository
from schemas.user import UserCreate,UserLogin
from domain.user_entity import UserEntity
from core.security import create_access_token, verify_password, hash_password
import logging 

logger = logging.getLogger(__name__)

class AuthError(Exception):
    pass

class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def register_user(self, user: UserCreate) -> UserEntity:
        existing = self.repo.get_by_email(user.email)
        if existing:
            logger.warning(f"User already exists: {user.email}")
            raise ValueError("User already exists")
        user.password = hash_password(user.password)
        new_user = self.repo.create(user)
        logger.info(f"User registered: {new_user.email}")
        return new_user

    def login_user(self, user: UserLogin) -> str:
        try:
            db_user = self.repo.get_by_email(user.email)
            if not db_user or not verify_password(user.password, db_user.password_hash):
                logger.warning(f"Invalid login attempt: {user.email}")
                raise AuthError("Invalid email or password")
            token = create_access_token(  db_user.email)
            logger.info(f"User logged in: {db_user.email}")
            return token
        except Exception as ex:
            logger.error(f"Login failed: {ex}")
            raise AuthError("Login failed")
