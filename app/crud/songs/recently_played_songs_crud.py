import uuid
from fastapi import HTTPException, status
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from app.models.recently_played_song_model import RecentlyPlayedSongModel
from sqlalchemy import func
from sqlalchemy.orm import joinedload

from app.models.song_model import SongModel

def insert_recently_played(db: Session, user_id: str, song_id: str):
    # First, verify the song exists
    song = db.query(SongModel).filter(SongModel.song_id == song_id).first()
    if not song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Song with id {song_id} not found"
        )
    
    # Convert user_id string to UUID (user_id IS UUID in model)
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user_id format"
        )
    
    # Insert or update recently played
    stmt = insert(RecentlyPlayedSongModel).values(
        user_id=user_uuid,      
        song_id=song_id,        
    ).on_conflict_do_update(
        index_elements=["user_id", "song_id"],
        set_={"played_at": func.now()}
    )
    
    db.execute(stmt)
    db.commit()
    
    return song

def get_recently_played_songs(db: Session, user_id: str, limit: int, offset: int):
    recently_played = (
        db.query(RecentlyPlayedSongModel)
        .filter(RecentlyPlayedSongModel.user_id == uuid.UUID(user_id))
        .order_by(RecentlyPlayedSongModel.played_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return [entry.song for entry in recently_played if entry.song is not None]