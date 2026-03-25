from middlewares.VerifyToken import verifyToken
from fastapi import HTTPException, status, Depends
from models.authModel import RolesEnum
from config import db
import bson


def ValidateUser(role: RolesEnum):
    async def wrapper(user_id: str = Depends(verifyToken)):
        user = await db.user_collection.find_one({"_id": bson.ObjectId(user_id)})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )

        if user["role"] != role.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User is not {role.value}",
            )
        return user_id

    return wrapper
