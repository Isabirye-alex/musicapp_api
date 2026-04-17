from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.crud.user.user_signup_crud import create_user
from app.db.session import get_db
from app.schemas.user_schema import UserCreate
from app.services.fetch_use_by_email import get_user_by_email
import jwt
import os


router = APIRouter()

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def sign_up(user: UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    create_user(db, user)
    return Response(status_code=status.HTTP_201_CREATED)
