# mock/models/product.py
from pydantic import BaseModel
from typing import Optional


class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category_id: int
    is_active: bool = True


class Product(ProductCreate):
    id: int
