from sqlalchemy import Column, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.base import Base


class RecentlyPlayedSongModel(Base):
    __tablename__ = "recently_played_songs"

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    song_id = Column(
        UUID(as_uuid=True),                             
        ForeignKey("songs.song_id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )

    played_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # ── Relationships ──
    song = relationship("SongModel", lazy="joined")
    user = relationship("UserModel", lazy="select")