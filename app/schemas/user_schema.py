from datetime import datetime
from typing import Optional
from uuid import UUID

import re

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    role: Optional[str] = Field(default="user")

    @field_validator("first_name", "last_name")
    @classmethod
    def no_blank_strings(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Field cannot be blank or whitespace")
        return v.strip()

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return v


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True)

    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    role: str
    is_active: bool
    user_avatar: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class UserUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True, validate_by_name=True)

    first_name: Optional[str] = Field(default=None, min_length=1, max_length=250)
    last_name: Optional[str] = Field(default=None, min_length=1, max_length=250)
    email: Optional[EmailStr] = None
    user_avatar: Optional[str] = None

    @field_validator("first_name", "last_name", mode="before")
    @classmethod
    def strip_and_validate_name(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        stripped = v.strip()
        if not stripped:
            raise ValueError("Name fields cannot be blank or whitespace only")
        if not re.match(r"^[a-zA-Z\s\-']+$", stripped):
            raise ValueError(
                "Name fields can only contain letters, spaces, hyphens, and apostrophes"
            )
        return stripped


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user: UserResponse
    access_token: str
