from sqlalchemy.orm import Session
import uuid

from app.core.password_hash import hash_password
from app.models.user_model import UserModel
from app.schemas.user_schema import UserCreate



def create_user(db: Session, user: UserCreate):
    hashed = hash_password(user.password_hash)
    db_user = UserModel(
        id=str(uuid.uuid4()),
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password_hash=hashed,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
