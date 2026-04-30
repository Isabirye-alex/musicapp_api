from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.user.user_delete import delete_user, activate_user
from app.middleware.auth_middleware import auth_middleware

router = APIRouter()


@router.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(
    user_id: str,
    permanent: bool = False,
    db: Session = Depends(get_db), 
    current_user: dict = Depends(auth_middleware)
):
    try:
        delete_user(user_id, db, permanent=permanent)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the user",
        )

@router.post("/activate/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def activate_user_endpoint(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth_middleware)
):
    try:
        activate_user(user_id, db)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error activating user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while activating the user",
        )
