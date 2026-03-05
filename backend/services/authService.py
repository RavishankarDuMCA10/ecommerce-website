from config.db import user_collection


async def registerService(data):
    await user_collection.insert_one(data.dict())
    return {"message": "User registered successfully"}
