from middlewares import VerifyToken
from fastapi import HTTPException, status, Depends
from models.authModel import RolesEnum
from typing import Optional
from config import db
import bson


async def ValidateUser(user: RolesEnum, user_id: str = Depends(VerifyToken)):
    user = await db.user_collection.find_one({"_id": bson.ObjectId(user_id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    if user["role"] != user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"User is not {user}"
        )
    return user_id
