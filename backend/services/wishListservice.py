from config.db import wishlist_collection, product_collection
from models import wishListModel
import bson


async def toggleProductWishListService(product_id, user_id):
    check_exist = await wishlist_collection.find_one(
        {"user_id": user_id, "product_id": product_id}
    )
    if check_exist:
        await wishlist_collection.find_one_and_delete(
            {"user_id": user_id, "product_id": product_id}
        )
        return {"msg": "Product  has been removed from the Wishlist"}
    product = wishListModel.AddProductWishList(product_id=product_id, user_id=user_id)
    await wishlist_collection.insert_one(product.dict())
    return {"msg": "Product has been added in the Wishlist"}


async def getProductWishListService(product_id, user_id):
    check_exist = await wishlist_collection.find_one(
        {"user_id": user_id, "product_id": product_id}
    )
    if check_exist:
        return {"exist": True}
    return {"exist": False}


async def getProductsWishListService(user_id):
    products = []
    async for product in wishlist_collection.find({"user_id": user_id}):
        product_data = await product_collection.find_one(
            {"_id": bson.ObjectId(product["product_id"])}
        )
        if product_data:
            products.append(
                {
                    "id": str(product_data["_id"]),
                    "title": product_data["title"],
                    "description": product_data["description"],
                    "price": product_data["price"],
                    "category": product_data["category"],
                    "slug": product_data["slug"],
                    "image": product_data["images"][0]["image_url"]
                    if product_data["images"]
                    else None,
                    "created_at": product_data["created_at"],
                }
            )
    print("Products in wishlist:", products)
    return products


async def deleteProductWishListService(product_id, user_id):
    await wishlist_collection.find_one_and_delete(
        {"user_id": user_id, "product_id": product_id}
    )
    return {"msg": "Product  has been removed from the Wishlist"}
