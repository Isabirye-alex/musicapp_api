
import uuid

from sqlalchemy import TEXT, UUID, VARCHAR, Column

from app.core.base import Base


class SongModel(Base):

    __tablename__ = 'songs'

    song_id = Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4 )
    song_name = Column(VARCHAR(250), nullable=False)
    artist_name = Column(VARCHAR(250), nullable=False)
    song_url = Column(VARCHAR(250), nullable=False)
    thumbnail_url = Column(VARCHAR(250), nullable=True)
    user_id = Column(VARCHAR(250), nullable=False)