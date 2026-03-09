from fastapi import APIRouter
from controllers.authController import registerController, loginController
from models.authModel import RegisterUser, LoginUser

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


# register
@router.post("/register")
async def registerView(data: RegisterUser):
    return await registerController(data)


# login
@router.post("/login")
async def loginView(data: LoginUser):
    return await loginController(data)
