from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID
from datetime import datetime

class SongCreate(BaseModel):
    song_name: str
    artist_name: str
    song_url: str
    thumbnail_url: str
    user_id: UUID
    hex_code: str

    @field_validator("song_name", "artist_name", "song_url", "thumbnail_url")
    @classmethod
    def no_blank_strings(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Field cannot be blank or whitespace")
        return v.strip()


class SongResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    song_id: str
    song_name: str
    artist_name: str
    song_url: str
    thumbnail_url: str
    user_id: UUID
    hex_code: str
    is_favorite: bool = Field(default=False)
    created_at: datetime
    updated_at: datetime    
