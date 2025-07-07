# api/services/chess_service.py
import time
import threading
from typing import Dict, Any
from concurrent.futures import ThreadPoolExecutor

# 存储任务状态
chess_tasks = {}

def run_chess_ai_game(task_id: str):
    """模拟象棋对弈模型运行"""
    try:
        chess_tasks[task_id] = {"status": "running", "result": None}
        print(f"[任务 {task_id}] 象棋对弈模型开始运行")
        time.sleep(10)  # 模拟耗时操作
        result = "红方胜利"
        chess_tasks[task_id] = {"status": "completed", "result": result}
        print(f"[任务 {task_id}] 象棋对弈完成：{result}")
    except Exception as e:
        chess_tasks[task_id] = {"status": "failed", "error": str(e)}

def run_chess_ocr(task_id: str, image_path: str):
    """模拟象棋识别模型运行"""
    try:
        chess_tasks[task_id] = {"status": "running", "result": None}
        print(f"[任务 {task_id}] 象棋识别模型开始运行，识别图片: {image_path}")
        time.sleep(5)  # 模拟耗时操作
        result = {"board_state": "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR"}
        chess_tasks[task_id] = {"status": "completed", "result": result}
        print(f"[任务 {task_id}] 象棋识别完成：{result}")
    except Exception as e:
        chess_tasks[task_id] = {"status": "failed", "error": str(e)}

# 全局线程池执行器
executor = ThreadPoolExecutor(max_workers=2)
