from fastapi import APIRouter, Request, Depends
from controllers import authController
from middlewares.VerifyToken import verifyToken
from models import authModel

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


# register
@router.post("/register")
async def registerView(data: authModel.RegisterUser):
    return await authController.registerController(data)


# login
@router.post("/login")
async def loginView(data: authModel.LoginUser):
    return await authController.loginController(data)


# profile
@router.get("/profile")
async def profileView(userId=Depends(verifyToken)):
    # user_id = verifyToken(req)
    return await authController.profileController(userId)
