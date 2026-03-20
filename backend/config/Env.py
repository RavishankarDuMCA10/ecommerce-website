from dotenv import load_dotenv
import os

load_dotenv()


class ENVConfig:
    MONGO_URI = os.getenv("MONGO_URI", "")
    MONGO_DB = os.getenv("MONGO_DB", "")
    JWT_AUTH_SECRET_KEY = os.getenv("JWT_AUTH_SECRET_KEY", "$%^&*(*&)")
    ALGORITHMS = "HS256"
    API_KEY_CLOUDINARY = os.getenv("API_KEY_CLOUDINARY", "")
    API_SECRET_CLOUDINARY = os.getenv("API_SECRET_CLOUDINARY", "")
    CLOUD_NAME_CLOUDINARY = os.getenv("CLOUD_NAME_CLOUDINARY", "")
