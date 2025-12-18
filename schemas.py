from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    bio: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    email: Optional[str] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserProfileResponse(UserResponse):
    bookmarks_count: int = 0

class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    isbn: Optional[str] = None
    publication_year: Optional[int] = None
    genre: Optional[str] = None
    pages: Optional[int] = None
    cover_url: Optional[str] = None

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int
    average_rating: float
    created_at: datetime
    
    class Config:
        from_attributes = True

class BookDetailResponse(BookResponse):
    user_rating: Optional[int] = None
    is_bookmarked: bool = False

class RatingCreate(BaseModel):
    rating: int  

class RatingResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    rating: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class BookmarkResponse(BaseModel):
    book_id: int
    added_at: datetime
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
