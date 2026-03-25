from services import productService
from fastapi import HTTPException, status


async def addProductController(images, data, userId):
    try:
        return await productService.addProductService(images, data, userId)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def allProductsController(userId):
    try:
        return await productService.allProductsService(userId)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def deleteProductController(productId, userId):
    try:
        return await productService.deleteProductService(productId, userId)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
