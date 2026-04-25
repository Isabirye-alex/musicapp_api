from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.middleware.auth_middleware import auth_middleware
from app.models.song_model import SongModel
from app.models.favorite_songs_model import FavoriteSongsModel


def fetch_all_user_songs(db: Session, user_dict: dict):
    songs = db.query(SongModel).filter(SongModel.user_id == user_dict["id"]).all()

    # Add is_favorite field
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


def fetch_all_platform_songs(db: Session, user_dict: dict):
    songs = db.query(SongModel).all()

    # Add is_favorite field for each song
    if user_dict:
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
    else:
        for song in songs:
            setattr(song, "is_favorite", False)

    return songs
