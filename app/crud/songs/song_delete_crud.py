import cloudinary.api
from sqlalchemy.orm import Session
from app.models.song_model import SongModel
import re
def delete_song_by_id(db: Session, song_id: str) -> bool:
    song = db.query(SongModel).filter(SongModel.song_id == song_id).first()
    if not song:
        return False
    
    # Delete from DB
    db.delete(song)
    db.commit()

    # Try deleting from Cloudinary
    try:

        cloudinary_id = song_id
        if song.song_url:
            match = re.search(r"songs/([^/]+)/", song.song_url)
            if match:
                cloudinary_id = match.group(1)
                
        cloudinary.api.delete_resources_by_prefix(f"songs/{cloudinary_id}", resource_type="video")
        cloudinary.api.delete_resources_by_prefix(f"songs/{cloudinary_id}", resource_type="image")
        cloudinary.api.delete_folder(f"songs/{cloudinary_id}")
    except Exception as e:
        print(f"Failed to delete cloudinary resources for {song_id}: {e}")

    return True
