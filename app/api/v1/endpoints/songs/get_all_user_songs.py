from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.crud.songs.song_fetch_crud import fetch_all_user_songs
from app.db.session import get_db
from app.middleware.auth_middleware import auth_middleware
from app.schemas.song_schema import SongResponse
from typing import List
router = APIRouter()


@router.get("/list", response_model=List[SongResponse], status_code=status.HTTP_200_OK)
@router.get("/list/{limit}/{offset}", response_model=List[SongResponse], status_code=status.HTTP_200_OK)
def get_all_user_songs(
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db), 
    user_dict=Depends(auth_middleware)
):
    try:
        songs = fetch_all_user_songs(db, user_dict)
        if songs is None:
            return None or 'No songs found for this user'

        return songs
    except Exception as e:
        raise RuntimeError(f'Error retrieving users songs with error code: {e}')
