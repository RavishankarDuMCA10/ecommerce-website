from services.authService import registerService, loginService
from models.authModel import RegisterUser, LoginUser
from fastapi.exceptions import HTTPException


async def registerController(data: RegisterUser):
    try:
        res_obj = await registerService(data)
        return res_obj
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=f"{str(e)}")


async def loginController(data: LoginUser):
    try:
        res_obj = await loginService(data)
        return res_obj
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=f"{e}")
