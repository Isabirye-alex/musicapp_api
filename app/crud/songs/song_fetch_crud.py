from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.middleware.auth_middleware import auth_middleware
from app.models.song_model import SongModel
from app.models.favorite_songs_model import FavoriteSongsModel
from sqlalchemy import or_

def fetch_all_user_songs(db: Session, user_dict: dict, limit: int, offset: int):
    songs = db.query(SongModel).filter(SongModel.user_id == user_dict["id"]).offset(offset).limit(limit).all()

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


def fetch_all_platform_songs(
    db: Session,
    limit: int,
    offset: int,
    sort: str,
    user_dict: dict | None = None,
    search: str | None = None
):

    query = db.query(SongModel)

    if search:
        term = f"%{search.strip()}%"
        query = query.filter(
            or_(
                SongModel.song_name.ilike(term),
                SongModel.artist_name.ilike(term), 
            )
        )

    if sort == "newest":
        query = query.order_by(SongModel.created_at.desc())
    elif sort == "oldest":
        query = query.order_by(SongModel.created_at.asc())
    elif sort == "name":
        query = query.order_by(SongModel.song_name.asc())
    songs = query.offset(offset).limit(limit).all()

    if not user_dict:
        for song in songs:
            song.is_favorite = False
        return songs

    user_id = user_dict.get("id")

    favorite_ids = {
        res[0]
        for res in db.query(FavoriteSongsModel.song_id)
        .filter(FavoriteSongsModel.user_id == user_id)
        .all()
    }

    for song in songs:
        song.is_favorite = song.song_id in favorite_ids

    return songs
