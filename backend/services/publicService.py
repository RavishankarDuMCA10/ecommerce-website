from config.db import product_collection
from random import choice


async def getAllProductsService():
    all_products = []
    async for product in product_collection.find(
        {},
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
