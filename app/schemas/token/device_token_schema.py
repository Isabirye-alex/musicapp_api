
from pydantic import BaseModel
from typing import Optional

class RegisterTokenRequest(BaseModel):
    token: str   # null for guests
    platform: Optional[str] = None