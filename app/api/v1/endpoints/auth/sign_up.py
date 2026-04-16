from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud.user.user_signup_crud import create_user
from app.db.session import get_db
from app.schemas.user_schema import UserCreate, AuthResponse
from app.services.fetch_use_by_email import get_user_by_email
import jwt
import os


router = APIRouter()


@router.post(
    "/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED
)
def sign_up(user: UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY is not set in environment variables")
    
    new_user = create_user(db, user)

    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY is not set in environment variables")
    
    token = jwt.encode({"id": str(new_user.id)}, SECRET_KEY, algorithm="HS256")
    
    return {"user": new_user, "access_token": token}
