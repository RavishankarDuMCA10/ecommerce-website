from fastapi import File, UploadFile
from config.db import user_collection, profile_collection
from models import authModel
from fastapi.exceptions import HTTPException
import bcrypt
import jwt
from config.Env import ENVConfig
from datetime import datetime, timedelta
import bson
from typing import Annotated
import cloudinary.uploader


async def registerService(data: authModel.RegisterUser):
    check_exist = await user_collection.find_one({"email": data.email.lower()})
    if check_exist:
        raise HTTPException(status_code=400, detail="Email already exists")

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(data.password.encode("utf-8"), salt)
    hash_string = hashed_password.decode("utf-8")
    user_data = data.dict()
    user_data["password"] = hash_string
    del user_data["name"]
    doc = await user_collection.insert_one(user_data)
    # profile
    user_profile = authModel.UserProfile(
        user_id=str(doc.inserted_id),
        name=data.name,
    )
    await profile_collection.insert_one(user_profile.dict())
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
    check_exist = await user_collection.find_one(
        {"_id": bson.ObjectId(userId)},
        {
            "password": 0,
        },
    )
    if not check_exist:
        raise HTTPException(status_code=404, detail="User Detail Not Found")
    # del check_exist["password"]
    check_exist["_id"] = str(check_exist["_id"])
    profile = await profile_collection.find_one({"user_id": check_exist["_id"]})
    del profile["_id"]
    del profile["user_id"]
    return check_exist | profile


async def updateAvatarService(avatar: Annotated[UploadFile, File()], userId: str):
    try:
        exist = await profile_collection.find_one({"user_id": userId})
        if exist["avatar"] and exist["avatar"]["image_uri"]:
            cloudinary.uploader.destroy(exist["avatar"]["public_id"])

        contents = await avatar.read()
        print(f"Received file: {avatar.filename}")
        upload_result = cloudinary.uploader.upload(
            contents, folder="ecommerce-website/user_profile"
        )
        print(f"Upload result: {upload_result}")
        await profile_collection.find_one_and_update(
            {"user_id": userId},
            {
                "$set": {
                    "avatar": {
                        "image_uri": upload_result["secure_url"],
                        "public_id": upload_result["public_id"],
                    },
                    "update_at": datetime.now(),
                }
            },
        )
        return {"msg": "Profile image updated successfully"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=f"{e}")
