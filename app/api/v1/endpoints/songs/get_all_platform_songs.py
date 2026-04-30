from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from app.crud.songs.song_fetch_crud import fetch_all_platform_songs
from app.db.session import get_db
from app.middleware.auth_middleware import auth_middleware
from app.schemas.song_schema import SongResponse
from typing import List

router = APIRouter()


@router.get(
    "/all",
    response_model=List[SongResponse],
    status_code=status.HTTP_200_OK,
)
@router.get(
    "/all/{limit}/{offset}",
    response_model=List[SongResponse],
    status_code=status.HTTP_200_OK,
)
def get_all_platform_songs(
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
    sort: str = Query(default='newest'),
    user_dict: dict | None = Depends(auth_middleware),
):
    try:
        songs = fetch_all_platform_songs(db,limit, offset,sort ,user_dict)
        return songs
    except Exception as e:
        raise RuntimeError(f"Error retrieving songs: {e}")
