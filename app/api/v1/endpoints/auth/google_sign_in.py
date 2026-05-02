from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.crud.auth.google_auth_crud import google_sign_in
from app.db.session import get_db
from app.schemas.user_schema import AuthResponse

router = APIRouter()

class GoogleAuthRequest(BaseModel):
    token: str

@router.post("/google", response_model=AuthResponse, status_code=status.HTTP_200_OK)
def google_auth(body: GoogleAuthRequest, db: Session = Depends(get_db)):
    return google_sign_in(token=body.token, db=db)