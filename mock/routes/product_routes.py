# mock/routes/product_routes.py
from fastapi import APIRouter, HTTPException, status
from typing import List
from models.product import Product, ProductCreate
from db.product_db import (
    get_all_products,
    get_product_by_id,
    create_product,
    update_product,
    delete_product,
)

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_new_product(product: ProductCreate):
    return create_product(product.dict())


@router.get("/", response_model=List[Product])
def read_products():
    return get_all_products()


@router.get("/{product_id}", response_model=Product)
def read_product(product_id: int):
    product = get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=Product)
def update_existing_product(product_id: int, product: ProductCreate):
    updated_product = update_product(product_id, product.dict())
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_product(product_id: int):
    if not delete_product(product_id):
        raise HTTPException(status_code=404, detail="Product not found")
