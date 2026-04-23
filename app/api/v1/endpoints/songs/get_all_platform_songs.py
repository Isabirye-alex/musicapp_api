from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.crud.songs.song_fetch_crud import fetch_all_platform_songs
from app.db.session import get_db
from app.middleware.auth_middleware import auth_middleware
from app.schemas.song_schema import SongResponse
from typing import List

router = APIRouter()


@router.get("/all", response_model=List[SongResponse], status_code=status.HTTP_200_OK)
def get_all_platform_songs(
    db: Session = Depends(get_db),
    user_dict: dict = Depends(auth_middleware),  # Added back for is_favorite
):
    try:
        songs = fetch_all_platform_songs(db, user_dict)  # Pass user_dict
        if not songs:
            return []
        return songs
    except Exception as e:
        raise RuntimeError(f"Error retrieving songs: {e}")
