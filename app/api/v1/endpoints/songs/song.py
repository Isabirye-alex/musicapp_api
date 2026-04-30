import uuid

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
import cloudinary.uploader
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.middleware.auth_middleware import auth_middleware
from app.schemas.song_schema import SongCreate, SongResponse
from app.crud.songs.song_upload_crud import create_song
from app.crud.songs.song_delete_crud import delete_song_by_id

router = APIRouter()


@router.post(
    "/upload", response_model=SongResponse, status_code=status.HTTP_201_CREATED
)
async def upload_song(
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

     

        # Upload SONG (Cloudinary)

        song_upload_result = cloudinary.uploader.upload(
            song.file,
            resource_type="video",  # rfor audio/video
            folder=f"songs/{song_id}",
            chunk_size=6000000,  # to handle large files safely
        )

        # Upload THUMBNAIL

        thumbnail_upload_result = cloudinary.uploader.upload(
            thumbnail.file,
            resource_type="image",
            folder=f"songs/{song_id}",
        )

        # Extract URLs safely
        song_url = song_upload_result.get("secure_url")
        thumbnail_url = thumbnail_upload_result.get("secure_url")

        if not song_url or not thumbnail_url:
            raise HTTPException(
                status_code=500, detail="Failed to retrieve uploaded file URLs"
            )

        # Create DB object

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
        #  return proper JSON error (prevents Flutter crash)
        raise HTTPException(status_code=500, detail=f"Error uploading song: {str(e)}")

@router.delete("/{song_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_song(
    song_id: str,
    db: Session = Depends(get_db),
    user_dict=Depends(auth_middleware),
):
    try:
        success = delete_song_by_id(db, song_id)
        if not success:
            raise HTTPException(status_code=404, detail="Song not found")
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting song: {str(e)}")

