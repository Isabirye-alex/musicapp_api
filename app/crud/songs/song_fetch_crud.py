

from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.middleware.auth_middleware import auth_middleware
from app.models.song_model import SongModel


def fetch_all_user_songs(db: Session, user_dict: dict):
    songs = db.query(SongModel).filter(SongModel.user_id == user_dict['id']).all()

    return songs

