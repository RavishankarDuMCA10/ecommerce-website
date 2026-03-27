from fastapi import APIRouter, FastAPI, Query
from typing import Optional
from controllers import publicContoller

router = APIRouter(prefix="/api/v1", tags=["Public"])


@router.get("/products")
async def getAllProductsView(
    search: Optional[str] = Query(default=None, description="Search by product title"),
    category: Optional[str] = Query(default=None, description="Filter by category"),
):
    return await publicContoller.getAllProductsContoller(
        search=search, category=category
    )


@router.get("/product/{slug}")
async def getProductBySlugView(slug: str):
    return await publicContoller.getProductBySlugController(slug)
