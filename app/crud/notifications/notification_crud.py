# Send to ALL users (including guests)
from app.models.tokens.device_token_model import DeviceTokenModel
from sqlalchemy.orm import Session

def get_all_tokens(db: Session):
    return db.query(DeviceTokenModel.token).all()

# Send to guests only
def get_guest_tokens(db: Session):
    return db.query(DeviceTokenModel.token).filter(
        DeviceTokenModel.user_id == None
    ).all()

# Send to specific user (all their devices)
def get_user_tokens(db: Session, user_id: str):
    return db.query(DeviceTokenModel.token).filter_by(user_id=user_id).all()