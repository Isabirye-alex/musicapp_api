from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.models.user_model import UserModel

def delete_user(user_id: str, db: Session, permanent: bool = False):
    try:
        # Converting string to UUID object
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid user ID format"
        )

    # Fetching the user record
    user = db.query(UserModel).filter(UserModel.id == user_uuid).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found."
        )
    
    if permanent:
        # Permanently delete the user
        db.delete(user)
    else:
        # Soft delete (deactivate)
        user.is_active = False
    
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to {'delete' if permanent else 'deactivate'} user"
        )
        
    return None

def activate_user(user_id: str, db: Session):
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID format")

    user = db.query(UserModel).filter(UserModel.id == user_uuid).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    user.is_active = True
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to activate user")
    
    return None