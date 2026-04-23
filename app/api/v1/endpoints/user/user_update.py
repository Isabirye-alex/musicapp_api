from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.middleware.auth_middleware import auth_middleware
from app.schemas.user_schema import UserUpdate
from app.crud.user.user_update import update_user


router = APIRouter()
@router.patch("/update/{user_id}", response_model=UserUpdate)
def update_user_endpoint(user_id: str, user_update: UserUpdate, db: Session = Depends(get_db), current_user: dict = Depends(auth_middleware)): 
    try:
        updated_user = update_user(current_user['id'], user_update, db)
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while updating the user")