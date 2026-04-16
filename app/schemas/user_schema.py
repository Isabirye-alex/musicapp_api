from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password_hash: str = Field(min_length=8, max_length=64)

    @field_validator("first_name", "last_name")
    @classmethod
    def no_blank_strings(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Field cannot be blank or whitespace")
        return v.strip()

    @field_validator("password_hash")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one number")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        return v


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True) 

    id: UUID
    first_name: str
    last_name: str
    email: EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password_hash: str


class AuthResponse(BaseModel):
    user: UserResponse
    token: str

    model_config = ConfigDict(from_attributes=True)
