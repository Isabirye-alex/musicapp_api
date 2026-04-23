from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.user.user_delete import delete_user
from app.middleware.auth_middleware import auth_middleware

router = APIRouter()


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(
    db: Session = Depends(get_db), current_user: dict = Depends(auth_middleware)
):
    try:
        delete_user(current_user["id"], db)
    except Exception as e:
        print(f"Error deleting user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the user",
        )
