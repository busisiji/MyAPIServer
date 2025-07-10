from fastapi import APIRouter
from src.cchessAI.services.training_service import training_service

router = APIRouter(prefix="/train", tags=["训练"])

@router.post("/start")
def start_train():
    return training_service.start_training()

@router.post("/selfplay/start")
def start_selfplay():
    return training_service.start_selfplay()

@router.get("/model")
def get_model_info():
    return training_service.get_latest_model()
