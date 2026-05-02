from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.crud.auth.google_auth_crud import google_sign_in
from app.db.session import get_db
from app.schemas.user_schema import AuthResponse

router = APIRouter()

class GoogleAuthRequest(BaseModel):
    token: str

@router.post("/google", response_model=AuthResponse, status_code=status.HTTP_200_OK)
def google_auth(body: GoogleAuthRequest, db: Session = Depends(get_db), background_tasks: BackgroundTasks = None):
    return google_sign_in(token=body.token, db=db, background_tasks=background_tasks)