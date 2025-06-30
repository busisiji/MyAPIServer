# app/db/database.py
import peewee
from config import settings

# 根据 DATABASE_URL 自动识别数据库类型
if settings.DATABASE_URL.startswith("sqlite"):
    db = peewee.SqliteDatabase(settings.DATABASE_URL)
elif settings.DATABASE_URL.startswith("mysql"):
    from urllib.parse import urlparse
    url = urlparse(settings.DATABASE_URL)
    db = peewee.MySQLDatabase(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port or 3306
    )
elif settings.DATABASE_URL.startswith("postgres"):
    from urllib.parse import urlparse
    url = urlparse(settings.DATABASE_URL)
    db = peewee.PostgresqlDatabase(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port or 5432
    )
else:
    raise ValueError("Unsupported database type")
