# api_mock/routes/user_routes.py
from fastapi import APIRouter, HTTPException, status
from typing import List
from models.user import User, UserCreate
from db.user_db import (
    get_all_users,
    get_user_by_id,
    create_user,
    update_user,
    delete_user,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_new_user(user: UserCreate):
    return create_user(user.dict())


@router.get("/", response_model=List[User])
def read_users():
    return get_all_users()


@router.get("/{user_id}", response_model=User)
def read_user(user_id: int):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=User)
def update_existing_user(user_id: int, user: UserCreate):
    updated_user = update_user(user_id, user.dict())
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(user_id: int):
    if not delete_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
