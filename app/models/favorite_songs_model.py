
import uuid

from sqlalchemy import Column, ForeignKey, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from app.core.base import Base


class FavoriteSongsModel(Base):
    __tablename__ = "favorite_songs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    song_id = Column(Text, ForeignKey("songs.song_id", ondelete="CASCADE"), nullable=False, index=True)

    __table_args__ = (
        UniqueConstraint("user_id", "song_id", name="uq_user_song_favorite"),
    )

    def __repr__(self):
        return f"<FavoriteSongsModel user_id={self.user_id} song_id={self.song_id}>"
    