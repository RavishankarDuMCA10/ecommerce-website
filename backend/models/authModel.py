from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional
import bson


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
    create_at: datetime = Field(default_factory=datetime.now)
    update_at: datetime = Field(default_factory=datetime.now)


class AddressModel(BaseModel):
    pin_code: str
    district: str
    state: str
    country: str
    landmark: str


class UserProfile(BaseModel):
    user_id: str = Field(...)
    name: str = Field(...)
    avatar: Optional[ProfileImage] = Field(default=None)
    address: List[AddressModel] = []
    create_at: datetime = Field(default_factory=datetime.now)
    update_at: datetime = Field(default_factory=datetime.now)


class RegisterUser(User):
    pass


class LoginUser(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=6)
