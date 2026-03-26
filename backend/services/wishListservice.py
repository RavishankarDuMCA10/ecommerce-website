from config.db import wishlist_collection
from models import wishListModel


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
