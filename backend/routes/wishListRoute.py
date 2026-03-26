from fastapi import APIRouter, Depends
from controllers import wishListController
from middlewares.VerifyUser import ValidateUser
from models import wishListModel, authModel

router = APIRouter(prefix="/api/v1/wishlist", tags=["WishList"])


@router.post("/toggle")
async def toggleProductWishListView(
    data: wishListModel.ToggleProduct,
    user_id: str = Depends(ValidateUser(authModel.RolesEnum.buyer)),
):
    return await wishListController.toggleProductWishListController(
        data.product_id, user_id
    )


@router.get("/get/{product_id}")
async def getProductWishListView(
    product_id: str,
    user_id: str = Depends(ValidateUser(authModel.RolesEnum.buyer)),
):
    return await wishListController.getProductWishListController(product_id, user_id)
