from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.crud.songs.recently_played_songs_crud import insert_recently_played
from app.db.session import get_db
from app.middleware.auth_middleware import auth_middleware
from app.crud.songs.song_fetch_crud import fetch_all_user_songs
from app.crud.songs.recently_played_songs_crud import insert_recently_played

router = APIRouter("/")


@router.post("/", status_code=status.HTTP_200_OK, response_model=dict)
def add_recently_played_song(
    db: Session = Depends(get_db),
    user_dict: dict = Depends(auth_middleware),
    song_id=Query(default=None),
):
    try:
        if not song_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="song_id query parameter is required",
            )
        song = insert_recently_played(db, user_dict["id"], song_id)
        return {"status": "success", "song": song}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
