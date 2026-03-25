import config.cloudinaryConfig
import cloudinary.uploader
from slugify import slugify
import uuid
from config.db import profile_collection, product_collection
import bson


async def addProductService(images, data, userId):
    # Logic to add a product
    upload_images = []

    for image in images:
        content = await image.read()
        result = cloudinary.uploader.upload(
            content, folder="ecommerce-website/products"
        )
        upload_images.append(
            {"image_url": result["secure_url"], "public_id": result["public_id"]}
        )

    data = data.dict()
    # slug field
    data["slug"] = slugify(data["title"] + "____" + str(uuid.uuid4()))

    user = await profile_collection.find_one(
        {"user_id": userId},
        {
            "name": 1,
            "user_id": 1,
            "_id": 0,
        },
    )

    await product_collection.insert_one(data | {"images": upload_images, "user": user})

    return {"msg": "Product added successfully"}


async def allProductsService(userId):
    all_products = []
    async for product in product_collection.find({"user.user_id": userId}):
        all_products.append(
            {
                "id": str(product["_id"]),
                "title": product["title"],
                "description": product["description"],
                "price": product["price"],
                "category": product["category"],
                "slug": product["slug"],
                "image": product["images"][0]["image_url"]
                if product["images"]
                else None,
                "created_at": product["created_at"],
                "updated_at": product["updated_at"],
            }
        )
    return all_products


async def deleteProductService(productId, userId):
    product = await product_collection.find_one_and_delete(
        {"_id": bson.ObjectId(productId), "user.user_id": userId}
    )
    if not product:
        raise Exception(
            "Product not found or you don't have permission to delete this product"
        )

    # Delete images from Cloudinary
    for image in product.get("images", []):
        try:
            cloudinary.uploader.destroy(image["public_id"])
        except Exception as e:
            print(f"Error deleting image {image['public_id']} from Cloudinary: {e}")

    # # Delete the product from the database
    # await product_collection.delete_one({"_id": bson.ObjectId(productId)})

    return {"msg": "Product deleted successfully"}
