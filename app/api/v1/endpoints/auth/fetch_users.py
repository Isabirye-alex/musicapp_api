from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.crud.user.fetch_all_users import fetch_users
from app.db.session import get_db
from app.schemas.user_schema import UserResponse

from app.middleware.auth_middleware import auth_middleware

router = APIRouter()


@router.get("/users", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def get_users(
    db: Session = Depends(get_db), user_dict: dict = Depends(auth_middleware)
):
    users = fetch_users(db)

    return users
