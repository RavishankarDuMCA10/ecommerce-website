from fastapi import APIRouter, Depends, HTTPException, status
from controllers import wishListController
from middlewares.VerifyUser import ValidateUser
from models import wishListModel, authModel

router = APIRouter(prefix="/api/v1/wishlist", tags=["WishList"])


@router.post("/toggle")
async def toggleProductWishListView(
    data: wishListModel.ToggleProduct,
    user_id: str = Depends(ValidateUser(authModel.RolesEnum.buyer)),
):
    try:
        return await wishListController.toggleProductWishListController(
            data.product_id, user_id
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/get")
async def getProductsWishListView(
    user_id: str = Depends(ValidateUser(authModel.RolesEnum.buyer)),
):
    print("getProductsWishListView", user_id)
    try:
        return await wishListController.getProductsWishListController(user_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/get/{product_id}")
async def getProductWishListView(
    product_id: str,
    user_id: str = Depends(ValidateUser(authModel.RolesEnum.buyer)),
):
    try:
        return await wishListController.getProductWishListController(
            product_id, user_id
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/delete/{product_id}")
async def deleteProductWishListView(
    product_id: str,
    user_id: str = Depends(ValidateUser(authModel.RolesEnum.buyer)),
):
    print("deleteProductWishListView", product_id, user_id)
    try:
        return await wishListController.deleteProductWishListController(
            product_id, user_id
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
