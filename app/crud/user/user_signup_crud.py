import uuid

from sqlalchemy.orm import Session

from app.core.password_hash import hash_password
from app.models.user_model import UserModel
from app.schemas.user_schema import UserCreate


def create_user(db: Session, user: UserCreate):
    db_user = UserModel(
        id=uuid.uuid4(),
        first_name=user.first_name,
        last_name=user.last_name,
        email=str(user.email),
        password_hash=hash_password(user.password),
        role=user.role or "user",
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
