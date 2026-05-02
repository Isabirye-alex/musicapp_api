import os
from fastapi import HTTPException, Header
import jwt

def auth_middleware(
    x_auth_token: str | None = Header(default=None),
    authorization: str | None = Header(default=None)
) -> dict | None:  
    try:
        token = x_auth_token
        if not token and authorization and authorization.startswith("Bearer "):
            token = authorization.split(" ")[1]

        if not token:
            return None  # ← was raising 401, now returns None for guest users

        SECRET_KEY = os.getenv("SECRET_KEY")
        if not SECRET_KEY:
            raise ValueError("SECRET_KEY is not set in environment variables")
        
        auth_token = jwt.decode(token, SECRET_KEY, ["HS256"])

        uid = auth_token.get("id")

        if not uid:
            raise HTTPException(401, "Token payload missing user id")

        return {"id": uid, "access_token": auth_token} # ← return decoded token for downstream use

    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token has expired") 
    except jwt.PyJWTError:
        raise HTTPException(401, "Token is invalid, Authorization failed")