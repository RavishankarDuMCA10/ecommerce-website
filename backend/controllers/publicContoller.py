from services import publicService
from fastapi import HTTPException, status


async def getAllProductsContoller():
    try:
        res_obj = await publicService.getAllProductsService()
        return res_obj
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
