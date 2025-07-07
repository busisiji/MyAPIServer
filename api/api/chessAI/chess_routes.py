# api/api/chess_routes.py
from fastapi import APIRouter, BackgroundTasks
from api.services.chessAI.chess_service import chess_tasks, run_chess_ai_game, run_chess_ocr

router = APIRouter(prefix="/chess", tags=["Chess"])

@router.post("/ai-game")
def start_ai_game(background_tasks: BackgroundTasks):
    """启动象棋对弈模型任务"""
    task_id = "ai_game_" + str(len(chess_tasks) + 1)
    background_tasks.add_task(run_chess_ai_game, task_id)
    return {"task_id": task_id, "message": "象棋对弈任务已启动"}

@router.post("/ocr")
def start_ocr(image_path: str, background_tasks: BackgroundTasks):
    """启动象棋识别模型任务"""
    task_id = "ocr_" + str(len(chess_tasks) + 1)
    background_tasks.add_task(run_chess_ocr, task_id, image_path)
    return {"task_id": task_id, "message": "象棋识别任务已启动"}

@router.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    """查询任务状态和结果"""
    task = chess_tasks.get(task_id)
    if not task:
        return {"error": "任务不存在"}
    return task
