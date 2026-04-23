import uuid
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.favorite_songs_model import FavoriteSongsModel
from app.models.song_model import SongModel


def add_favorite_song(db: Session, user_id: str, song_id: str) -> FavoriteSongsModel:
    song = db.query(SongModel).filter(SongModel.song_id == song_id).first()
    if not song:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Song not found")

    existing_favorite = (
        db.query(FavoriteSongsModel)
        .filter(FavoriteSongsModel.user_id == user_id, FavoriteSongsModel.song_id == song_id)
        .first()
    )
    if existing_favorite:
        return existing_favorite

    favorite = FavoriteSongsModel(id=uuid.uuid4(), user_id=user_id, song_id=song_id)
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return favorite


def remove_favorite_song(db: Session, user_id: str, song_id: str) -> None:
    favorite = (
        db.query(FavoriteSongsModel)
        .filter(FavoriteSongsModel.user_id == user_id, FavoriteSongsModel.song_id == song_id)
        .first()
    )
    if not favorite:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Favorite not found")

    db.delete(favorite)
    db.commit()


def fetch_favorite_songs(db: Session, user_id: str) -> list[SongModel]:
    return (
        db.query(SongModel)
        .join(FavoriteSongsModel, SongModel.song_id == FavoriteSongsModel.song_id)
        .filter(FavoriteSongsModel.user_id == user_id)
        .all()
    )
