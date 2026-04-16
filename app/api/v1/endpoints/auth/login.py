from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session
from app.crud.user.user_login_crud import login_user
from app.db.session import get_db
from app.middleware.auth_middleware import auth_middleware
from app.models.user_model import UserModel
from app.schemas.user_schema import AuthResponse, LoginRequest, UserResponse
import jwt
import secrets
import os
from dotenv import load_dotenv
load_dotenv()

router = APIRouter()


@router.post("/signin", response_model=AuthResponse, status_code=status.HTTP_200_OK)
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
    
    token = jwt.encode({"id": str(user_db.id)}, SECRET_KEY, "HS256")
    
    return {"user": user_db, "access_token": token}

@router.get('/', response_model=UserResponse)
def get_current_user(db: Session = Depends(get_db), user_dict = Depends(auth_middleware)):
    
    try:
        user = db.query(UserModel).filter(UserModel.id == user_dict['uid']).first()

        if not user:
            raise HTTPException(404, 'No user Found')

        return user
    except Exception as e:
        raise HTTPException(500, 'Internal Server error')