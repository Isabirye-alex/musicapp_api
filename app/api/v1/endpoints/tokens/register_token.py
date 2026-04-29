from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.token.device_token_schema import RegisterTokenRequest
from app.models.tokens.device_token_model import DeviceTokenModel
from app.middleware.auth_middleware import auth_middlware

router = APIRouter()


@router.post("/fcm/register-token")
async def register_token(
    request: RegisterTokenRequest,
    db: Session = Depends(get_db),
    user_dict: dict | None = Depends(auth_middlware),
):
    existing = db.query(DeviceTokenModel).filter_by(token=request.token).first()

    user_id = user_dict.get("id") if user_dict else None

    if existing:
        if user_id:
            existing.user_id = user_id
        existing.platform = request.platform
        action = "updated"
    else:
        db.add(
            DeviceTokenModel(
                token=request.token,
                user_id=user_id,  # None for guests
                platform=request.platform,
            )
        )
        action = "created"

    db.commit()

    return {
        "success": True,
        "action": action,
    }