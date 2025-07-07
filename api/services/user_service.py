# 这一层封装了与用户相关的业务逻辑，实现接口与数据访问的解耦。
from api.models.user import User
from api.utils.exceptions import ResourceNotFoundException, InvalidInputException

def get_all_users():
    return list(User.select())

def get_user_by_id(user_id: int):
    user = User.get_or_none(User.id == user_id)
    if not user:
        raise ResourceNotFoundException("User")
    return user

def create_user(name: str, email: str):
    if not name or not email:
        raise InvalidInputException("Name and email are required")
    return User.create(name=name, email=email)

def update_user(user_id: int, name: str, email: str):
    user = get_user_by_id(user_id)
    if not name or not email:
        raise InvalidInputException("Name and email are required")
    user.name = name
    user.email = email
    user.save()
    return user

def delete_user(user_id: int):
    user = get_user_by_id(user_id)
    user.delete_instance()
    return {"detail": "User deleted successfully"}
