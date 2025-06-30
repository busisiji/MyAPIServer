# 这是项目的启动文件，主要职责包括：
# 初始化日志系统；
# 初始化数据库连接并创建表；
# 注册中间件（如请求日志）；
# 注册路由；
# 添加全局异常处理器；
# 启动 Uvicorn 服务器。

from fastapi import FastAPI
import uvicorn

from app.api.user_routes import router as user_router
from app.utils.logger import setup_logger
from app.exceptions.handler import add_exception_handlers
from app.middleware.request_logger import log_requests
from app.models.user import db, User

# 初始化日志
setup_logger(debug=False)

# 初始化数据库
db.connect()
db.create_tables([User], safe=True)

app = FastAPI(debug=False)

# 注册中间件
app.middleware("http")(log_requests)

# 注册路由
app.include_router(user_router)

# 添加全局异常处理器
add_exception_handlers(app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=1)
