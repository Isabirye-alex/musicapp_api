import uuid

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
import cloudinary.uploader
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.middleware.auth_middleware import auth_middleware
from app.schemas.song_schema import SongCreate, SongResponse
from app.crud.songs.song_upload_crud import create_song

router = APIRouter()


@router.post(
    "/upload", response_model=SongResponse, status_code=status.HTTP_201_CREATED
)
def upload_song(
    song: UploadFile = File(...),
    thumbnail: UploadFile = File(...),
    artist_name: str = Form(...),
    song_name: str = Form(...),
    hex_code: str = Form(...),
    db: Session = Depends(get_db),
    user_dict=Depends(auth_middleware),
):
    try:
        song_id = str(uuid.uuid4())

        # Upload song
        song_upload_result = cloudinary.uploader.upload(
            song.file, resource_type="video",format='mp3' ,folder=f"songs/{song_id}"
        )

        # Upload thumbnail
        thumbnail_upload_result = cloudinary.uploader.upload(
            thumbnail.file, resource_type="image", folder=f"songs/{song_id}"
        )

        # Extract URLs
        song_url = song_upload_result.get("secure_url")
        thumbnail_url = thumbnail_upload_result.get("secure_url")

        # Create schema object
        song_data = SongCreate(
            user_id=user_dict["id"],
            song_name=song_name,
            artist_name=artist_name,
            song_url=song_url,
            thumbnail_url=thumbnail_url,
            hex_code=hex_code,
        )

        # Save to DB
        new_song = create_song(db, song_data)

        return new_song

    except Exception as e:
        raise RuntimeError(f"Error uploading song: {str(e)}")
