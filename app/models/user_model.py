from sqlalchemy import VARCHAR, Column, LargeBinary, String
from sqlalchemy.dialects.postgresql import UUID  # or use sqlalchemy UUID for generic

import uuid

from app.core.declarative_base_ import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(VARCHAR(250), nullable=False)
    last_name = Column(VARCHAR(250), nullable=False)
    email = Column(VARCHAR(250), nullable=False, unique=True, index=True)
    password_hash = Column(VARCHAR(250), nullable=False) 
