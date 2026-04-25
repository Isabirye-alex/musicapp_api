import os
from fastapi import HTTPException, Header
import jwt


def auth_middleware(x_auth_token: str | None = Header(default=None)):
    try:
        # Get token from header
        if not x_auth_token:
            return None

        # Decode token
        SECRET_KEY = os.getenv("SECRET_KEY")
        if not SECRET_KEY:
            raise ValueError("SECRET_KEY is not set in environment variables")
        auth_token = jwt.decode(x_auth_token, SECRET_KEY, ["HS256"])

        if not auth_token:
            raise HTTPException(
                401, "Invalid or empty auth token, Authorization denied"
            )

        uid = auth_token.get("id")

        return {"id": uid, "acccess_token": auth_token}
    except jwt.PyJWTError:
        raise HTTPException(401, "Token is invalid, Authorization failed")
