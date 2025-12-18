from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from models import Book, User, Rating
from schemas import BookResponse, BookDetailResponse, RatingCreate, RatingResponse
from auth import get_current_user, get_current_user_optional
from database import get_db

router = APIRouter(prefix="/api/books", tags=["books"])


@router.get("/", response_model=list[BookResponse])
def get_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: str = Query(None),
    genre: str = Query(None),
    db: Session = Depends(get_db)
):

    query = db.query(Book)
    

    if search:
        query = query.filter(
            (Book.title.ilike(f"%{search}%")) | 
            (Book.author.ilike(f"%{search}%"))
        )
    

    if genre:
        query = query.filter(Book.genre.ilike(f"%{genre}%"))
    
    books = query.offset(skip).limit(limit).all()
    return books

@router.get("/{book_id}", response_model=BookDetailResponse)
def get_book(
    book_id: int,
    current_user: User = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Получить информацию о конкретной книге"""
    book = db.query(Book).filter(Book.id == book_id).first()
    
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    

    is_bookmarked = False
    user_rating = None
    
    if current_user:
        is_bookmarked = current_user in book.bookmarked_by
        rating = db.query(Rating).filter(
            (Rating.user_id == current_user.id) & 
            (Rating.book_id == book_id)
        ).first()
        if rating:
            user_rating = rating.rating
    
    book_detail = BookDetailResponse(
        **{k: getattr(book, k) for k in book.__table__.columns.keys()},
        is_bookmarked=is_bookmarked,
        user_rating=user_rating
    )
    return book_detail

@router.get("/genre/list/all")
def get_genres(db: Session = Depends(get_db)):
    """Получить список всех жанров"""
    genres = db.query(Book.genre).distinct().filter(Book.genre != None).all()
    return [g[0] for g in genres]



@router.post("/{book_id}/rate", response_model=RatingResponse)
def rate_book(
    book_id: int,
    rating_data: RatingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if not (1 <= rating_data.rating <= 5):
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")

    existing_rating = db.query(Rating).filter(
        (Rating.user_id == current_user.id) &
        (Rating.book_id == book_id)
    ).first()

    if existing_rating:
        existing_rating.rating = rating_data.rating
        rating_obj = existing_rating
    else:
        rating_obj = Rating(
            user_id=current_user.id,
            book_id=book_id,
            rating=rating_data.rating,
        )
        db.add(rating_obj)


    db.flush()  


    avg_rating = db.query(func.avg(Rating.rating)).filter(
        Rating.book_id == book_id
    ).scalar()
    book.average_rating = float(avg_rating) if avg_rating is not None else 0.0

    db.commit()
    db.refresh(rating_obj)
    db.refresh(book)

    return rating_obj


@router.post("/admin/create", response_model=BookResponse)
def create_book(
    book_data: BookResponse,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Создать новую книгу (только для администраторов)"""
    
    new_book = Book(**book_data.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book
