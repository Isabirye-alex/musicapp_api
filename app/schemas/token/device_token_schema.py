
from pydantic import BaseModel
from typing import Optional

class RegisterTokenRequest(BaseModel):
    token: str
    user_id: Optional[str] = None     # null for guests
    platform: Optional[str] = None