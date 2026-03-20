from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import datetime, timezone
from enum import Enum
from typing import Union, Optional


class RolesEnum(str, Enum):
    seller = "seller"
    buyer = "buyer"


class ProfileImage(BaseModel):
    image_uri: str
    public_id: str


class User(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=6)
    role: Optional[RolesEnum] = Field(default=RolesEnum.buyer)
    avatar: Optional[ProfileImage] = Field(default=None)
    create_at: datetime = Field(default_factory=datetime.now)
    update_at: datetime = Field(default_factory=datetime.now)

    @field_validator("name")
    def validate_name(cls, value):
        if len(value) < 3:
            raise ValueError("Name must be at least 3 characters long")
        return value


class RegisterUser(User):
    pass


class LoginUser(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=6)
