import uuid
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from app.models.recently_played_song_model import RecentlyPlayedSongModel
from sqlalchemy import func
from sqlalchemy.orm import joinedload


def insert_recently_played(db: Session, user_id: str, song_id: str):
    stmt = insert(RecentlyPlayedSongModel).values(
        user_id=uuid.UUID(user_id),      
        song_id=uuid.UUID(song_id),     
    ).on_conflict_do_update(
        index_elements=["user_id", "song_id"],
        set_={"played_at": func.now()}
    )
    db.execute(stmt)
    db.commit()


def get_recently_played_songs(db: Session, user_id: str, limit: int, offset: int):
    recently_played = (
        db.query(RecentlyPlayedSongModel)
        .options(joinedload(RecentlyPlayedSongModel.song))  # ← eager load song
        .filter(RecentlyPlayedSongModel.user_id == uuid.UUID(user_id))
        .order_by(RecentlyPlayedSongModel.played_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return [entry.song for entry in recently_played if entry.song is not None]