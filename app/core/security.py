import os
from datetime import datetime, timedelta
from typing import Any

import jwt

from app.core.config import settings


def create_access_token(subject: str, expires_minutes: int = 60 * 24) -> str:
    now = datetime.utcnow()
    payload = {
        "sub": subject,
        "exp": now + timedelta(minutes=expires_minutes),
        "iat": now,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def decode_access_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
