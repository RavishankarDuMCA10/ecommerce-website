from fastapi import APIRouter, FastAPI
from controllers import publicContoller

router = APIRouter(prefix="/api/v1", tags=["Public"])


@router.get("/products")
async def getAllProductsView():
    return await publicContoller.getAllProductsContoller()


@router.get("/product/{slug}")
async def getProductBySlugView(slug: str):
    return await publicContoller.getProductBySlugController(slug)
