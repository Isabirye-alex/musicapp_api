from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.crud.songs.favorite_crud import fetch_favorite_songs, toggle_favorite_song
from app.db.session import get_db
from app.schemas.song_schema import SongResponse

router = APIRouter()


@router.post("/favorites/{song_id}")
def toggle_song_favorite(
    song_id: str,
    db: Session = Depends(get_db),
    user_dict: dict = Depends(get_current_user),
):
    try:
        return toggle_favorite_song(db, user_dict["id"], song_id)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error toggling favorite status: {exc}",
        )


@router.get(
    "/favorites",
    response_model=List[SongResponse],
    status_code=status.HTTP_200_OK,
)
def list_favorite_songs(
    db: Session = Depends(get_db),
    user_dict: dict = Depends(get_current_user),
):
    try:
        songs = fetch_favorite_songs(db, user_dict["id"])
        for song in songs:
            song.is_favorite = True
        return songs
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching favorite songs: {exc}",
        )
