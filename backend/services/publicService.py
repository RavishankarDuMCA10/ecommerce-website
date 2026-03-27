from config.db import product_collection
from random import choice
from fastapi import HTTPException, status
from typing import Optional


async def getAllProductsService(
    search: Optional[str] = None, category: Optional[str] = None
):
    query = {}
    if search:
        query["title"] = {"$regex": search, "$options": "i"}
    if category:
        query["category"] = {"$regex": f"^{category}$", "$options": "i"}

    all_products = []
    async for product in product_collection.find(
        query,
        {
            "_id": 0,
            "description": 0,
            "user": 0,
            "created_at": 0,
            "updated_at": 0,
        },
    ):
        product["image"] = (
            choice(product["images"])["image_url"] if product["images"] else None
        )
        del product["images"]
        all_products.append(product)
    return all_products


async def getProductBySlugService(slug: str):
    product = await product_collection.find_one(
        {"slug": {"$regex": slug, "$options": "i"}},
        {
            "updated_at": 0,
        },
    )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    if "_id" in product:
        product["_id"] = str(product["_id"])
    if "_id" in product["user"]:
        del product["user"]["_id"]
    if "user_id" in product["user"]:
        del product["user"]["user_id"]

    product["image"] = (
        choice(product["images"])["image_url"] if product["images"] else None
    )
    del product["images"]
    return product
