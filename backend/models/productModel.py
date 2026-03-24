from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional
from datetime import datetime


class ProductCategory(str, Enum):
    JEWELLERY = "JEWELLERY"
    TSHIRT = "TSHIRT"
    PICTURES = "PICTURES"
    BEAUTY = "BEAUTY"
    PAJAMA = "PAJAMA"
    SAREE = "SAREE"


class Product(BaseModel):
    title: str = Field(...)
    description: str = Field(...)
    price: int = Field(...)
    category: Optional[ProductCategory] = Field(...)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
