import threading
import os
from train.train import TrainPipeline
from collect.self_play.collect_rl import CollectPipeline

class TrainingService:
    def __init__(self):
        self.training_thread = None
        self.collect_thread = None
        self.is_training = False
        self.is_collecting = False
        self.model_path = "models/latest.pkl"

    def start_training(self):
        if self.is_training:
            return {"status": "already_running"}

        def run_train():
            try:
                print("🔄 开始训练...")
                pipeline = TrainPipeline(init_model=self.model_path)
                pipeline.run()
                print("✅ 训练完成")
            finally:
                self.is_training = False

        self.is_training = True
        self.training_thread = threading.Thread(target=run_train, daemon=True)
        self.training_thread.start()
        return {"status": "started"}

    def start_selfplay(self):
        if self.is_collecting:
            return {"status": "already_running"}

        def run_selfplay():
            try:
                print("🔄 开始自我对弈采集...")
                collector = CollectPipeline(init_model=self.model_path)
                collector.run(is_shown=False)
            finally:
                self.is_collecting = False

        self.is_collecting = True
        self.collect_thread = threading.Thread(target=run_selfplay, daemon=True)
        self.collect_thread.start()
        return {"status": "started"}

    def get_latest_model(self):
        if not os.path.exists(self.model_path):
            return {"error": "No model found"}
        return {"model_path": self.model_path}

training_service = TrainingService()
