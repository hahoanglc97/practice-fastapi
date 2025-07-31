from sqlalchemy.orm import Session
from src.utils.db_utils import get_db
from src.repositories.book_repository import BookRepository
from src.repositories.user_repository import UserRepository
from src.repositories.rental_repository import RentalRepository
from fastapi import Depends

def get_book_repository(db: Session = Depends(get_db)) -> BookRepository:
    return BookRepository(db)

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_rental_repository(db: Session = Depends(get_db)) -> RentalRepository:
    return RentalRepository(db)
