# 使用 Peewee ORM 定义用户数据模型。
from peewee import Model, IntegerField, CharField
from app.db.database import db

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    name = CharField(max_length=50)
    email = CharField(unique=True, max_length=100)

    class Meta:
        table_name = 'users'
