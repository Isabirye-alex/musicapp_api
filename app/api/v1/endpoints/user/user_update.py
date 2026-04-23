from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.middleware.auth_middleware import auth_middleware
from app.schemas.user_schema import UserUpdate, UserResponse
from app.crud.user.user_update import update_user

router = APIRouter()

@router.patch("/update", response_model=UserResponse)  # ← UserUpdate → UserResponse
def update_user_endpoint(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth_middleware)
):
    return update_user( user_update, db, current_user)