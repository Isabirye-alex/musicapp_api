from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud.user.user_login_crud import login_user
from app.db.session import get_db
from app.schemas.user_schema import AuthResponse, LoginRequest, UserResponse
import jwt
import secrets
import os

router = APIRouter()


@router.post("/signin", response_model=UserResponse, status_code=status.HTTP_200_OK)
@router.post("/signin", response_model=AuthResponse)
def signin(credentials: LoginRequest, db: Session = Depends(get_db)):
    user_db, error = login_user(db, credentials.email, str(credentials.password_hash))

    if error or user_db is None:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = error or "Invalid credentials",
    )
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY is not set in environment variables")
    
    token = jwt.encode({"id": str(user_db.id)}, SECRET_KEY, algorithm="HS256")
    print(secrets.token_hex(32))

    return {"user": user_db, "token": token}
