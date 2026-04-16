from sqlalchemy.orm import Session

from app.models.user_model import UserModel

def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()
