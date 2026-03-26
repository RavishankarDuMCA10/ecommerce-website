from pydantic import BaseModel, Field
from datetime import datetime


class ToggleProduct(BaseModel):
    product_id: str = Field(..., description="ID of the product to add to the wishlist")
    user_id: str = Field(
        ..., description="ID of the user adding the product to the wishlist"
    )


class AddProductWishList(BaseModel):
    product_id: str = Field(..., description="ID of the product to add to the wishlist")
    user_id: str = Field(
        ..., description="ID of the user adding the product to the wishlist"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the product was added to the wishlist",
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the wishlist entry was last updated",
    )
