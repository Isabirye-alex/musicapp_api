# models/device_token.py
from sqlalchemy import Column, DateTime, ForeignKey, String, UUID, func
import uuid
from app.core.base import Base
from sqlalchemy.sql import func

class DeviceTokenModel(Base):
    __tablename__ = "device_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token = Column(String(250), nullable=False, unique=True)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True
    )
    platform = Column(String(20), nullable=True)  # "android", "ios"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
