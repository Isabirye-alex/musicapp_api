from sqlalchemy.orm import Session

from app.core.password_hash import verify_password
from app.models.user_model import UserModel


def login_user(db: Session, email: str, password: str):
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        return None, "Invalid email or password"

    if user.password_hash == "!google_auth_sign_in":
        return None, "This account uses Google Sign-In. Please use the Google button to log in."

    if not verify_password(password, user.password_hash):
        return None, "Invalid email or password"

    return user, None
