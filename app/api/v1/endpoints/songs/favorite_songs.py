from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.songs.favorite_crud import (
    add_favorite_song,
    fetch_favorite_songs,
    remove_favorite_song,
)
from app.db.session import get_db
from app.middleware.auth_middleware import auth_middleware
from app.schemas.song_schema import SongResponse

router = APIRouter()


@router.post("/favorites/{song_id}", status_code=status.HTTP_201_CREATED)
def add_song_to_favorites(
    song_id: str,
    db: Session = Depends(get_db),
    user_dict: dict = Depends(auth_middleware),
):
    try:
        add_favorite_song(db, user_dict["id"], song_id)
        return {"status": "success", "message": "Song added to favorites"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding song to favorites: {e}",
        )


@router.delete("/favorites/{song_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_song_from_favorites(
    song_id: str,
    db: Session = Depends(get_db),
    user_dict: dict = Depends(auth_middleware),
):
    try:
        remove_favorite_song(db, user_dict["id"], song_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error removing song from favorites: {e}",
        )


@router.get("/favorites", response_model=List[SongResponse], status_code=status.HTTP_200_OK)
def list_favorite_songs(
    db: Session = Depends(get_db),
    user_dict: dict = Depends(auth_middleware),
):
    try:
        songs = fetch_favorite_songs(db, user_dict["id"])
        for song in songs:
            setattr(song, "is_favorite", True)
        return songs
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching favorite songs: {e}",
        )
