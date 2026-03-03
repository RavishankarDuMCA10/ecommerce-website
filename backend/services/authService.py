from config.db import user_collection


async def registerService(data):
    doc = await user_collection.insert_one(data.dict())
    print(doc)
    return data.dict()
