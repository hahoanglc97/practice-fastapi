from fastapi import APIRouter
from src.api import books, users, rentals

api_router = APIRouter(prefix="/api")

api_router.include_router(books.router)
api_router.include_router(users.router)
api_router.include_router(rentals.router)
