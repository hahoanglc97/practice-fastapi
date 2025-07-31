from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query

from src.schemas.book import BookCreate, BookResponse
from src.repositories.book_repository import BookRepository
from src.dependencies import get_book_repository

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=List[BookResponse])
def get_books(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    book_repo: BookRepository = Depends(get_book_repository)
):
    """Get all books with pagination"""
    books = book_repo.get_all(skip=skip, limit=limit)
    return books

@router.get("/available", response_model=List[BookResponse])
def get_available_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    book_repo: BookRepository = Depends(get_book_repository)
):
    """Get books that have available copies for borrowing"""
    books = book_repo.get_available_books(skip=skip, limit=limit)
    return books

@router.get("/search", response_model=List[BookResponse])
def search_books(
    title: str = Query(None, description="Search by book title"),
    author: str = Query(None, description="Search by author name"),
    isbn: str = Query(None, description="Search by ISBN"),
    book_repo: BookRepository = Depends(get_book_repository)
):
    """Search books by title, author, or ISBN"""
    if not any([title, author, isbn]):
        raise HTTPException(status_code=400, detail="At least one search parameter is required")
    
    books = book_repo.search_books(title=title, author=author, isbn=isbn)
    return books

@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, book_repo: BookRepository = Depends(get_book_repository)):
    """Get a specific book by ID"""
    book = book_repo.get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.get("/isbn/{isbn}", response_model=BookResponse)
def get_book_by_isbn(isbn: str, book_repo: BookRepository = Depends(get_book_repository)):
    """Get a book by ISBN"""
    book = book_repo.get_by_isbn(isbn)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=BookResponse, status_code=201)
def create_book(book: BookCreate, book_repo: BookRepository = Depends(get_book_repository)):
    """Create a new book"""
    # Check if ISBN already exists
    existing_book = book_repo.get_by_isbn(book.ISBN)
    if existing_book:
        raise HTTPException(status_code=400, detail="Book with this ISBN already exists")
    
    return book_repo.create(book)

@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int, 
    book: BookCreate, 
    book_repo: BookRepository = Depends(get_book_repository)
):
    """Update a book"""
    db_book = book_repo.get(book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Check if ISBN is being changed and if it conflicts with another book
    if book.ISBN != db_book.ISBN:
        existing_book = book_repo.get_by_isbn(book.ISBN)
        if existing_book:
            raise HTTPException(status_code=400, detail="Book with this ISBN already exists")
    
    return book_repo.update(db_book, book)

@router.delete("/{book_id}")
def delete_book(book_id: int, book_repo: BookRepository = Depends(get_book_repository)):
    """Delete a book"""
    book = book_repo.delete(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return {"message": "Book deleted successfully"}
