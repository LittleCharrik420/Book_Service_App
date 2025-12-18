from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import Book, User
from schemas import BookResponse
from auth import get_current_user
from database import get_db

router = APIRouter(prefix="/api/bookmarks", tags=["bookmarks"])

@router.get("/", response_model=list[BookResponse])
def get_bookmarks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return current_user.bookmarks

@router.post("/{book_id}")
def add_bookmark(
    book_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    book = db.query(Book).filter(Book.id == book_id).first()
    
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    if book not in current_user.bookmarks:
        current_user.bookmarks.append(book)
        db.commit()
    
    return {"message": "Book added to bookmarks"}

@router.delete("/{book_id}")
def remove_bookmark(
    book_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    book = db.query(Book).filter(Book.id == book_id).first()
    
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    if book in current_user.bookmarks:
        current_user.bookmarks.remove(book)
        db.commit()
    
    return {"message": "Book removed from bookmarks"}

@router.get("/{book_id}/status")
def check_bookmark(
    book_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    book = db.query(Book).filter(Book.id == book_id).first()
    
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    is_bookmarked = book in current_user.bookmarks
    return {"is_bookmarked": is_bookmarked}
