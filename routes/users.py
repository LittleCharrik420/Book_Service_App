from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session

from models import User
from schemas import (
    UserResponse,
    UserCreate,
    UserUpdate,
    UserProfileResponse,
    TokenResponse,
)
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)
from database import get_db

router = APIRouter(prefix="/api/users", tags=["users"])


# ========== Registration & Login ==========

@router.post("/register", response_model=TokenResponse)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):

    existing_user = db.query(User).filter(
        (User.email == user_data.email) |
        (User.username == user_data.username)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username already exists",
        )


    new_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hash_password(user_data.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    access_token = create_access_token(data={"sub": str(new_user.id)})

    return TokenResponse(
        access_token=access_token,
        user=UserResponse.from_orm(new_user),
    )


@router.post("/login", response_model=TokenResponse)
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):

    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    access_token = create_access_token(data={"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        user=UserResponse.from_orm(user),
    )




@router.get("/me", response_model=UserProfileResponse)
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    db.refresh(current_user)
    return UserProfileResponse(
        **UserResponse.from_orm(current_user).dict(),
        bookmarks_count=len(current_user.bookmarks),
    )


@router.put("/me", response_model=UserResponse)
def update_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    # Проверка на уникальность email
    if user_data.email and user_data.email != current_user.email:
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use",
            )
        current_user.email = user_data.email

    if user_data.full_name is not None:
        current_user.full_name = user_data.full_name

    if user_data.bio is not None:
        current_user.bio = user_data.bio

    db.commit()
    db.refresh(current_user)
    return UserResponse.from_orm(current_user)


@router.get("/{user_id}", response_model=UserProfileResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return UserProfileResponse(
        **UserResponse.from_orm(user).dict(),
        bookmarks_count=len(user.bookmarks),
    )
