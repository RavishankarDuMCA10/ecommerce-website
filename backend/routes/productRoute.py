from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, Form
from typing import List, Annotated
from controllers import productController
from models import productModel, authModel
from middlewares.VerifyUser import ValidateUser

router = APIRouter(prefix="/api/v1/product", tags=["Seller Product"])


@router.get("/all-products")
async def allProductsView(
    userId: str = Depends(ValidateUser(authModel.RolesEnum.seller)),
):
    return await productController.allProductsController(userId)


@router.delete("/delete/{productId}")
async def deleteProductView(
    productId: str,
    userId: str = Depends(ValidateUser(authModel.RolesEnum.seller)),
):
    # Logic to delete a product
    try:
        return await productController.deleteProductController(productId, userId)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/add-product")
async def addProductView(
    images: Annotated[List[UploadFile], File()],
    title: str = Form(...),
    description: str = Form(...),
    price: int = Form(...),
    category: str = Form(...),
    # userId=Depends(verifyToken),
    userId: str = Depends(ValidateUser(authModel.RolesEnum.seller)),
):
    # Logic to add a product
    if not images:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one image is required",
        )
    try:
        data = productModel.Product(
            title=title, description=description, price=price, category=category
        )
        productModel.Product.model_validate(data)
        print("Validated Data:", data)
        return await productController.addProductController(images, data, userId)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
