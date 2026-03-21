from config.Env import ENVConfig

from motor.motor_asyncio import AsyncIOMotorClient

client: AsyncIOMotorClient = AsyncIOMotorClient(ENVConfig.MONGO_URI)
db = client[ENVConfig.MONGO_DB]

# User Collection
user_collection = db["users"]
profile_collection = db["profile"]
