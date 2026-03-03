from fastapi import APIRouter
from controllers.authController import registerController
from typing import Any
from models.authModel import User as UserModel

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


# register
@router.post("/register")
def registerView(data: UserModel):
    return registerController(data.dict())
