from sqlalchemy.orm import Session


from app.core.password_hash import verify_password
from app.services.fetch_use_by_email import get_user_by_email

def login_user(db: Session, email: str, password: str):
    # 1. Check user exists
    user = get_user_by_email(db, email)
    if not user:
        return None, "Invalid email or password"

    # 2. Check password matches
    if not verify_password(password, user.password_hash): # type: ignore
        return None, "Invalid email or password"

    return user, None
