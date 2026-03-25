from fastapi import APIRouter, FastAPI
from controllers import publicContoller

router = APIRouter(prefix="/api/v1", tags=["Public"])


@router.get("/products")
async def getAllProductsView():
    return await publicContoller.getAllProductsContoller()
