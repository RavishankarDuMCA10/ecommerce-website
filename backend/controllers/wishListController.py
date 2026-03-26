from services import wishListservice
from fastapi import HTTPException, status


async def toggleProductWishListController(product_id, user_id):
    try:
        res_obj = await wishListservice.toggleProductWishListService(
            product_id, user_id
        )
        return res_obj
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def getProductWishListController(product_id, user_id):
    try:
        res_obj = await wishListservice.getProductWishListService(product_id, user_id)
        return res_obj
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
