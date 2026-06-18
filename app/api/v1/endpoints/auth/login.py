from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.core.config import settings
from app.core.security import create_access_token
from app.crud.user.user_login_crud import login_user
from app.db.session import get_db
from app.models.user_model import UserModel
from app.schemas.user_schema import AuthResponse, LoginRequest, UserResponse

router = APIRouter()


@router.post("/signin", response_model=AuthResponse, status_code=status.HTTP_200_OK)
def signin(credentials: LoginRequest, db: Session = Depends(get_db)):
    user_db, error = login_user(db, str(credentials.email), credentials.password)

    if error or user_db is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error or "Invalid credentials",
        )

    token = create_access_token(str(user_db.id))
    return {"user": user_db, "access_token": token}


@router.get("/me", response_model=UserResponse)
def get_current_user_endpoint(
    db: Session = Depends(get_db),
    user_dict: dict = Depends(get_current_user),
):
    user = db.query(UserModel).filter(UserModel.id == user_dict["id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="No user found")
    return user