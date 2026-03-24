import config.cloudinaryConfig
import cloudinary.uploader
from slugify import slugify
import uuid
from config.db import profile_collection, product_collection


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
            "email": 1,
            "_id": 1,
        },
    )

    await product_collection.insert_one(data | {"images": upload_images, "user": user})

    return {"msg": "Product added successfully"}


async def allProductsService(userId):
    products = []
    async for product in product_collection.find({"user.user_id": userId}):
        products.append(product)
    return products
