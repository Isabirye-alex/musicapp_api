from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.user_schema import UserUpdate
from app.models.user_model import UserModel
import logging

logger = logging.getLogger(__name__)

PROTECTED_FIELDS = {"id", "role", "is_active", "created_at", "hashed_password"}


def update_user(
    user_id: dict, user_update: UserUpdate, db: Session, current_user: UserModel
):
    # Authorization: only allow self-update or admin
    if current_user.id != user_id and not current_user.role == "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user",
        )

    user = db.query(UserModel).filter(UserModel.id == user_id['id']).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # strip protected fields
    update_data = {
        key: value
        for key, value in user_update.model_dump(exclude_unset=True).items()
        if key not in PROTECTED_FIELDS
    }

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid fields provided for update",
        )

    for key, value in update_data.items():
        setattr(user, key, value)

    try:
        db.commit()
        db.refresh(user)
    except SQLAlchemyError as e:
        db.rollback()
        logger.error("Failed to update user %s: %s", user_id, e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the user",
        )

    return user
