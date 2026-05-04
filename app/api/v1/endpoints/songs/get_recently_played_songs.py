from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.crud.songs.recently_played_songs_crud import insert_recently_played
from app.db.session import get_db
from app.middleware.auth_middleware import auth_middleware
from app.crud.songs.recently_played_songs_crud import get_recently_played_songs
from app.schemas.song_schema import SongResponse
from typing import List

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[SongResponse])
def get_recently_played(
    db: Session = Depends(get_db),
    user_dict: dict = Depends(auth_middleware),
    limit: int = Query(default=10),
    offset: int = Query(default=0),
):
    try:
        recently_played_songs = get_recently_played_songs(
            db, user_dict["id"], limit, offset
        )
        return recently_played_songs

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
