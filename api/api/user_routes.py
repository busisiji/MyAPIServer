# 该模块定义了 /users/ 路由下的所有 RESTful 接口，使用标准 HTTP 方法设计。
from fastapi import APIRouter, HTTPException
from api.services.user_service import (
    get_all_users,
    get_user_by_id,
    create_user,
    update_user,
    delete_user
)

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
def read_users():
    return {"items": get_all_users(), "total": len(get_all_users())}

@router.post("/")
def add_user(name: str, email: str):
    return create_user(name=name, email=email)

@router.get("/{user_id}")
def read_user(user_id: int):
    return get_user_by_id(user_id)

@router.put("/{user_id}")
def update_user_info(user_id: int, name: str, email: str):
    return update_user(user_id=user_id, name=name, email=email)

@router.delete("/{user_id}")
def delete_user_info(user_id: int):
    return delete_user(user_id)
