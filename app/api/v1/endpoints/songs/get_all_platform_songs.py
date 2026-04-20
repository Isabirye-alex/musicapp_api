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
    # ✅ removed auth_middleware
):
    try:
        songs = fetch_all_platform_songs(db)  # no user_id filter needed
        if not songs:
            return []
        return songs
    except Exception as e:
        raise RuntimeError(f"Error retrieving songs: {e}")
