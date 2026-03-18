from config.db import user_collection
from models import authModel
from fastapi.exceptions import HTTPException
import bcrypt
import jwt
from config.Env import ENVConfig
from datetime import datetime, timedelta
import bson


async def registerService(data: authModel.RegisterUser):
    check_exist = await user_collection.find_one({"email": data.email.lower()})
    if check_exist:
        raise HTTPException(status_code=400, detail="Email already exists")

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(data.password.encode("utf-8"), salt)
    hash_string = hashed_password.decode("utf-8")
    user_data = data.dict()
    user_data["password"] = hash_string
    doc = await user_collection.insert_one(user_data)
    token = jwt.encode(
        {
            "user_id": str(doc.inserted_id),
            "exp": datetime.utcnow() + timedelta(days=2),
            "iat": datetime.utcnow(),
        },
        ENVConfig.JWT_AUTH_SECRET_KEY,
        algorithm=ENVConfig.ALGORITHMS,
    )
    return {"message": "User registered successfully", "token": token}


async def loginService(data: authModel.LoginUser):
    # Check if user exist
    check_exist = await user_collection.find_one({"email": data.email.lower()})
    if not check_exist:
        raise HTTPException(status_code=400, detail="User Not Exist")

    # Verify password
    is_match = bcrypt.checkpw(
        data.password.encode("utf-8"), check_exist["password"].encode("utf-8")
    )
    if not is_match:
        raise HTTPException(status_code=400, detail="Invalid Credentials")

    token = jwt.encode(
        {
            "user_id": str(check_exist["_id"]),
            "exp": datetime.utcnow() + timedelta(days=2),
            "iat": datetime.utcnow(),
        },
        ENVConfig.JWT_AUTH_SECRET_KEY,
        algorithm=ENVConfig.ALGORITHMS,
    )

    return {"message": "Login Successfull", "token": token}


async def profileService(userId: str):
    check_exist = await user_collection.find_one({"_id": bson.ObjectId(userId)})
    if not check_exist:
        raise HTTPException(status_code=404, detail="User Detail Not Found")
    del check_exist["password"]
    check_exist["_id"] = str(check_exist["_id"])
    return check_exist
