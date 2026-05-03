from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from app.crud.songs.song_fetch_crud import fetch_all_user_songs
from app.db.session import get_db
from app.middleware.auth_middleware import auth_middleware
from app.schemas.song_schema import SongResponse
from typing import List

router = APIRouter()


@router.get("/list", response_model=List[SongResponse], status_code=status.HTTP_200_OK)
def get_all_user_songs(
    limit: int = Query(default=20),  # ← correct syntax
    offset: int = Query(default=0),
    db: Session = Depends(get_db),
    user_dict=Depends(auth_middleware),
):
    try:
        songs = fetch_all_user_songs(db, user_dict, limit, offset)
        return songs or []  # ← return empty list instead of string
    except Exception as e:
        raise HTTPException(  # ← not RuntimeError
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving user songs: {e}",
        )
