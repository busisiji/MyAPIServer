# api/services/dobot_service.py
import threading
from fastapi import HTTPException, BackgroundTasks
from api.dobot.dobot_utils import DobotArm

class DobotService:
    _arm = None
    _connected = False
    _feed_started = False

    @classmethod
    def connect(cls, background_tasks: BackgroundTasks):
        if cls._connected:
            return {"status": "already_connected"}
        try:
            cls._arm = DobotArm()
            cls._arm.connect()
            background_tasks.add_task(cls._start_feed)
            cls._connected = True
            return {"status": "connected"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"连接失败: {str(e)}")

    @classmethod
    def _start_feed(cls):
        if not cls._feed_started:
            cls._arm.start_feed_thread()
            cls._feed_started = True

    @classmethod
    def move(cls, point):
        if not cls._connected:
            raise HTTPException(status_code=400, detail="未连接机械臂")
        try:
            cls._arm.run_point(point)
            cls._arm.wait_arrive(point)
            return {"status": "moved", "point": point}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"移动失败: {str(e)}")

    @classmethod
    def suck_on(cls):
        if not cls._connected:
            raise HTTPException(status_code=400, detail="未连接机械臂")
        try:
            cls._arm.hll(f_13=1)
            return {"status": "suck_on"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"吸盘打开失败: {str(e)}")

    @classmethod
    def suck_off(cls):
        if not cls._connected:
            raise HTTPException(status_code=400, detail="未连接机械臂")
        try:
            cls._arm.hll(f_13=0)
            return {"status": "suck_off"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"吸盘关闭失败: {str(e)}")

    @classmethod
    def get_current_position(cls):
        if not cls._connected:
            raise HTTPException(status_code=400, detail="未连接机械臂")
        pos = cls._arm.current_actual
        if pos is None:
            raise HTTPException(status_code=500, detail="无法获取当前位置")
        return {"position": list(pos)}
