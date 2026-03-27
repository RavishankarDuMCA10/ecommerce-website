from services import wishListService
from fastapi import HTTPException, status


async def toggleProductWishListController(product_id, user_id):
    try:
        res_obj = await wishListService.toggleProductWishListService(
            product_id, user_id
        )
        return res_obj
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def getProductWishListController(product_id, user_id):
    try:
        res_obj = await wishListService.getProductWishListService(product_id, user_id)
        return res_obj
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def getProductsWishListController(user_id):
    try:
        print("getProductsWishListController", user_id)
        res_obj = await wishListService.getProductsWishListService(user_id)
        return res_obj
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def deleteProductWishListController(product_id, user_id):
    try:
        res_obj = await wishListService.deleteProductWishListService(
            product_id, user_id
        )
        return res_obj
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
