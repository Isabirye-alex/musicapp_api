from sqlalchemy import TEXT, UUID, VARCHAR, Column, DateTime, ForeignKey, func

from app.core.base import Base


from sqlalchemy import Column, ForeignKey, VARCHAR
from sqlalchemy.orm import relationship


class SongModel(Base):
    __tablename__ = "songs"

    song_id = Column(TEXT, primary_key=True)
    song_name = Column(VARCHAR(250), nullable=False)
    artist_name = Column(VARCHAR(250), nullable=False)
    song_url = Column(VARCHAR(250), nullable=False)
    thumbnail_url = Column(VARCHAR(250), nullable=True)

    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    hex_code = Column(VARCHAR(100), nullable=True)
