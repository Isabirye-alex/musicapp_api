from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user_model import UserModel

def fetch_users(db: Session, user_id: str):
    users = db.query(UserModel).filter(UserModel.id != user_id).all()

    return users