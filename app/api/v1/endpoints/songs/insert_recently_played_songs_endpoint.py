from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.crud.songs.recently_played_songs_crud import insert_recently_played
from app.db.session import get_db
from app.middleware.auth_middleware import auth_middleware
from app.crud.songs.recently_played_songs_crud import insert_recently_played
from app.schemas.song_schema import SongResponse
from typing import List

router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK, response_model=SongResponse)
def add_recently_played_song(
    db: Session = Depends(get_db),
    user_dict: dict = Depends(auth_middleware),
    song_id: str = Query(default=None),
):
    if not song_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="song_id query parameter is required",
        )

    try:
        song = insert_recently_played(db, user_dict["id"], song_id)

        return song

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
