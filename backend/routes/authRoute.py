from fastapi import APIRouter
from controllers.authController import registerController
from typing import Any
from models.authModel import RegisterUser
from config.db import user_collection

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


# register
@router.post("/register")
async def registerView(data: RegisterUser):
    doc = await user_collection.insert_one(data.dict())
    print(doc)
    return registerController(data)
