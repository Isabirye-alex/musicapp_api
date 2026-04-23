from sqlalchemy import Boolean, Column, DateTime, Enum, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum

from app.core.base import Base


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"


class UserModel(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, unique=True, index=True)
    
    # Text avoids truncation for longer hash algorithms (Argon2, scrypt)
    password_hash = Column(Text, nullable=False)
    
    # Enum enforces valid roles at the DB level
    role = Column(
        Enum(UserRole, name="user_role_enum"),
        nullable=False,
        default=UserRole.USER
    )
    
    # Fixed: was DateTime — should be Boolean
    is_active = Column(Boolean, nullable=False, default=True)
    
    # Fixed: use func.now() instead of the string "now()"
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
    # Fixed: onupdate keeps this accurate on every UPDATE
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    def __repr__(self):
        return f"<UserModel id={self.id} email={self.email} role={self.role}>"