import jwt
import os
from sqlalchemy.orm import Session
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from fastapi import HTTPException
from app.models.user_model import UserModel

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")

def google_sign_in(token: str, db: Session) -> dict:
    # 1. Verify token with Google
    try:
        user_info = id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            GOOGLE_CLIENT_ID,
        )
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Google token")

    # 2. Extract user info
    email      = user_info["email"]
    first_name = user_info.get("given_name", "")
    last_name  = user_info.get("family_name", "")
    avatar_url = user_info.get("picture")

    # 3. Find or create user
    user = db.query(UserModel).filter(UserModel.email == email).first()

    if not user:
        user = UserModel(
            email=email,
            first_name=first_name,
            last_name=last_name,
            user_avatar=avatar_url,
            password_hash="!google_auth_sign_in",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # 4. Block deactivated accounts
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is deactivated")

    # 5. Issue JWT — same way as signin route
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY is not set in environment variables")

    access_token = jwt.encode({"id": str(user.id)}, SECRET_KEY, "HS256")

    return {"user": user, "access_token": access_token}