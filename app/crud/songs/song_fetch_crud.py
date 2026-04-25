from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.middleware.auth_middleware import auth_middleware
from app.models.song_model import SongModel
from app.models.favorite_songs_model import FavoriteSongsModel
from sqlalchemy import bool


def fetch_all_user_songs(db: Session, user_dict: dict):
    songs = db.query(SongModel).filter(SongModel.user_id == user_dict["id"]).all()

    for song in songs:
        favorite = (
            db.query(FavoriteSongsModel)
            .filter(
                FavoriteSongsModel.user_id == user_dict["id"],
                FavoriteSongsModel.song_id == song.song_id,
            )
            .first()
        )
        setattr(song, "is_favorite", favorite is not None)

    return songs


def fetch_all_platform_songs(db: Session, user_dict: dict | None):
    user_id = user_dict.get("id") if user_dict else None

    query = db.query(
        SongModel, (FavoriteSongsModel.user_id == user_id).label("is_favorite")
    ).outerjoin(
        FavoriteSongsModel,
        (FavoriteSongsModel.song_id == SongModel.song_id)
        & (FavoriteSongsModel.user_id == user_id),
    )

    results = query.all()

    for song, is_fav in results:
        song.is_favorite = bool(is_fav)

    return [r[0] for r in results]
