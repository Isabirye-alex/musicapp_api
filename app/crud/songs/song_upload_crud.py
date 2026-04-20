from sqlalchemy.orm import Session

import uuid

from app.core.password_hash import hash_password
from app.models.song_model import SongModel
from app.schemas.song_schema import SongCreate


def create_song(db: Session, song: SongCreate):

    db_song = SongModel(
        user_id= song.user_id,
        song_id=str(uuid.uuid4()),
        song_name=song.song_name,
        artist_name=song.artist_name,
        song_url=song.song_url,
        thumbnail_url=song.thumbnail_url,
        hex_code = song.hex_code
    )
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song
