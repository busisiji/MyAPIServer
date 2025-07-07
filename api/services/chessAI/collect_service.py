from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
import subprocess

router = APIRouter()

# 定义请求体模型
class SelfPlayParams(BaseModel):
    processes: int = 4
    model_path: str = "/models/default_model"
    model_depth: int = 5
    num_games: int = 100

class CrawlerParams(BaseModel):
    owner: str = "_m_"
    mode: str = "append"  # append / overwrite
    start_id: int = 100000
    end_id: int = 120000

class CollectDataRequest(BaseModel):
    user_id: str
    collection_method: str  # self_play / crawler
    self_play_params: Optional[SelfPlayParams] = None
    crawler_params: Optional[CrawlerParams] = None
