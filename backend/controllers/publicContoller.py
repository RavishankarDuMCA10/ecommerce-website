from services import publicService
from fastapi import HTTPException, status
from typing import Optional


async def getAllProductsContoller(
    search: Optional[str] = None, category: Optional[str] = None
):
    try:
        res_obj = await publicService.getAllProductsService(
            search=search, category=category
        )
        return res_obj
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def getProductBySlugController(slug: str):
    try:
        res_obj = await publicService.getProductBySlugService(slug)
        return res_obj
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
