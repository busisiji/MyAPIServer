# app/api/routes.py
from fastapi import APIRouter
from app.services.user_service import get_users, create_user

router = APIRouter()

@router.get("/users/")
def read_users():
    users = get_users()
    return {"users": [{"id": u.id, "name": u.name, "email": u.email} for u in users]}

@router.post("/users/")
def add_user(name: str, email: str):
    user = create_user(name=name, email=email)
    return {"user": {"id": user.id, "name": user.name, "email": user.email}}
