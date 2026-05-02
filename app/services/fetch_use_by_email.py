from sqlalchemy.orm import Session
from app.models.user_model import UserModel


def get_user_by_email(db: Session, email: str):
    """
    Fetches a user by email, ensuring they are active.

    :param db: Database session
    :param email: Email to search for
    :return: UserModel instance if found and active, else None
    """
    return (
        db.query(UserModel)
        .filter(
            UserModel.email == email,
            UserModel.is_active == True,  # Ensure the user is active
        )
        .first()
    )
