from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user_optional
from app.crud.songs.song_fetch_crud import fetch_all_platform_songs
from app.db.session import get_db
from app.schemas.song_schema import SongResponse

router = APIRouter()


@router.get(
    "/all",
    response_model=List[SongResponse],
    status_code=status.HTTP_200_OK,
)
def get_all_platform_songs(
    limit: int = Query(default=100, ge=1),
    offset: int = Query(default=0, ge=0),
    sort: str = Query(default="newest"),
    search: str | None = Query(default=None),
    db: Session = Depends(get_db),
    user_dict: dict | None = Depends(get_current_user_optional),
):
    try:
        return fetch_all_platform_songs(
            db,
            limit=limit,
            offset=offset,
            sort=sort,
            user_dict=user_dict,
            search=search,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving songs: {exc}",
        )
