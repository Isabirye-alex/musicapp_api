from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user_model import User
from app.crud.user.user_delete import delete_user

router = APIRouter()


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(user_id: str, db: Session = Depends(get_db)):
    try:
        delete_user(user_id, db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the user",
        )
