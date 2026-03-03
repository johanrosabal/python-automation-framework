# mock/routes/category_routes.py
from fastapi import APIRouter, HTTPException, status
from typing import List
from models.category import Category, CategoryCreate
from db.category_db import (
    get_all_categories,
    get_category_by_id,
    create_category,
    update_category,
    delete_category,
)

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_new_category(category: CategoryCreate):
    return create_category(category.dict())


@router.get("/", response_model=List[Category])
def read_categories():
    return get_all_categories()


@router.get("/{category_id}", response_model=Category)
def read_category(category_id: int):
    category = get_category_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/{category_id}", response_model=Category)
def update_existing_category(category_id: int, category: CategoryCreate):
    updated_category = update_category(category_id, category.dict())
    if not updated_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated_category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_category(category_id: int):
    if not delete_category(category_id):
        raise HTTPException(status_code=404, detail="Category not found")
