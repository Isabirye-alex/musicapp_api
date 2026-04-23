from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user_model import UserModel


def delete_user(user_id: str, db: Session):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    db.delete(user)
    db.commit()
    return None