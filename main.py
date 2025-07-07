# 这是项目的启动文件，主要职责包括：
# 初始化日志系统；
# 初始化数据库连接并创建表；
# 注册中间件（如请求日志）；
# 注册路由；
# 添加全局异常处理器；
# 启动 Uvicorn 服务器。

from fastapi import FastAPI
import uvicorn

from api.api.chessAI.collect_routes import collect_data
from api.utils.logger import setup_logger
from api.exceptions.handler import add_exception_handlers
from api.middleware.request_logger import log_requests
from api.models.user import db, User

from api.api.user_routes import router as user_router
from api.api.chessAI.chess_routes import router as chess_router
from api.api.dobot_routes import router as dobot_router

import sys
import os

# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 构建项目 src 根目录路径
project_root = os.path.abspath(os.path.join(current_dir, "..", "..", "..", "src"))

# 添加到 PYTHONPATH
if project_root not in sys.path:
    sys.path.insert(0, project_root)


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
app.include_router(chess_router)
app.include_router(dobot_router)
app.include_router(collect_data)

# 添加全局异常处理器
add_exception_handlers(app)

if __name__ == "__main__":
    print("🚀 正在启动 API 服务...")
    print(f"🌐 监听地址: http://0.0.0.0:6017")
    print(f"⚙️  Debug 模式: {'开启' if app.debug else '关闭'}")
    uvicorn.run("main:app", host="0.0.0.0", port=6017, workers=1, log_level="info")

