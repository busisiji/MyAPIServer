# app/services/user_service.py
from app.models.user import User

def get_users():
    return list(User.select())

def create_user(name: str, email: str):
    return User.create(name=name, email=email)
