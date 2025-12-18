from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime, Table, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

bookmarks_table = Table(
    "bookmarks",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("book_id", Integer, ForeignKey("books.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    bookmarks = relationship(
        "Book",
        secondary=bookmarks_table,
        back_populates="bookmarked_by"
    )
    ratings = relationship("Rating", back_populates="user")

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), index=True, nullable=False)
    author = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    isbn = Column(String(20), unique=True, index=True, nullable=True)
    publication_year = Column(Integer, nullable=True)
    genre = Column(String(50), nullable=True)
    pages = Column(Integer, nullable=True)
    cover_url = Column(String(500), nullable=True)
    average_rating = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    bookmarked_by = relationship(
        "User",
        secondary=bookmarks_table,
        back_populates="bookmarks"
    )
    ratings = relationship("Rating", back_populates="book")

class Rating(Base):
    __tablename__ = "ratings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="ratings")
    book = relationship("Book", back_populates="ratings")
