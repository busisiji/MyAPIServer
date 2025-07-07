# api/api/dobot_routes.py
from fastapi import APIRouter, BackgroundTasks
from api.services.dobot_service import DobotService

router = APIRouter(prefix="/dobot", tags=["Dobot Arm"])

@router.post("/connect")
def connect_dobot(background_tasks: BackgroundTasks):
    """连接 Dobot 机械臂"""
    return DobotService.connect(background_tasks)

@router.post("/move")
def move_to_point(x: float, y: float, z: float, rx: float = 180.0, ry: float = 0.0, rz: float = 90.0):
    """移动到指定坐标点"""
    point = [x, y, z, rx, ry, rz]
    return DobotService.move(point)

@router.post("/suck-on")
def suck_on():
    """启动吸盘"""
    return DobotService.suck_on()

@router.post("/suck-off")
def suck_off():
    """关闭吸盘"""
    return DobotService.suck_off()

@router.get("/position")
def get_position():
    """获取当前机械臂位置"""
    return DobotService.get_current_position()
