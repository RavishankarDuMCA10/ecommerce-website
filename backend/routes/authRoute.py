from fastapi import APIRouter, File, Request, Depends, UploadFile
from controllers import authController
from middlewares.VerifyToken import verifyToken
from models import authModel
from typing import Any, Annotated

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
    return await authController.profileController(userId)


@router.put("/update-avatar")
async def updateAvatar(
    avatar: Annotated[UploadFile, File()], userId=Depends(verifyToken)
):
    return await authController.updateAvatarController(avatar, userId)


@router.put("/update-basic-details")
async def updateBasicDetails(
    data: authModel.UpdateBasicDetails, userId=Depends(verifyToken)
):
    return await authController.updateBasicDetailsController(data, userId)


@router.post("/add-address")
async def addAddress(data: authModel.AddressModel, userID=Depends(verifyToken)):
    return await authController.addNewAddressController(data, userID)


@router.delete("/delete-address/{id}")
async def deleteAddress(id: str, userID=Depends(verifyToken)):
    return await authController.deleteAddressController(id, userID)
