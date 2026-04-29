from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.token.device_token_schema import RegisterTokenRequest
from app.models.tokens.device_token_model import DeviceTokenModel

router = APIRouter()

@router.post("/fcm/register-token")
async def register_token(request: RegisterTokenRequest, db: Session = Depends(get_db)):
    existing = db.query(DeviceTokenModel).filter_by(token=request.token).first()

    if existing:
        # Update user_id if they just logged in
        existing.user_id = request.user_id or existing.user_id
        existing.platform = request.platform
    else:
        db.add(DeviceTokenModel(
            token=request.token,
            user_id=request.user_id,   # None for guests
            platform=request.platform,
        ))

    db.commit()
    return {"success": True}