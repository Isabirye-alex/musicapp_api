from fastapi import Depends, HTTPException, status

from app.middleware.auth_middleware import auth_middleware


def get_current_user(user: dict | None = Depends(auth_middleware)) -> dict:
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )
    return user


def get_current_user_optional(user: dict | None = Depends(auth_middleware)) -> dict | None:
    return user
