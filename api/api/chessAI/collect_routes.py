import os
import subprocess

from fastapi import APIRouter,HTTPException

from api.services.chessAI.collect_service import CollectDataRequest, SelfPlayParams, CrawlerParams

router = APIRouter(prefix="/chess", tags=["Chess"])
@router.post("/collect-data")
async def collect_data(request: CollectDataRequest):
    if request.collection_method == "self_play":
        # 获取自我对弈参数
        params = request.self_play_params or SelfPlayParams()

        # 构建命令行参数
        cmd = [
            "python", "src/cchessAI/collect/self_play/collect_multi_threads.py",
            "--workers", str(params.processes),
            "--save-interval", str(params.num_games)
        ]

        # 执行采集脚本（异步或后台运行）
        try:
            # 可使用 background_tasks 添加后台任务
            subprocess.Popen(cmd)
            return {"status": "started", "method": "self_play", "params": params}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Self-play采集启动失败: {str(e)}")

    elif request.collection_method == "crawler":
        # 获取爬虫参数
        params = request.crawler_params or CrawlerParams()

        # 构建命令行参数
        cmd = [
            "python", "src/cchessAI/collect/crawl/crawl_data_csv.py",
            "--owner", params.owner,
            "--mode", params.mode
        ]

        # 模拟指定 ID 范围的处理（需修改脚本支持 start/end）
        try:
            # 示例：临时写入 start_id 和 end_id 到环境变量（可扩展为脚本参数）
            os.environ['CRAWLER_START_ID'] = str(params.start_id)
            os.environ['CRAWLER_END_ID'] = str(params.end_id)

            subprocess.Popen(cmd)
            return {"status": "started", "method": "crawler", "params": params}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Crawler采集启动失败: {str(e)}")

    else:
        raise HTTPException(status_code=400, detail="无效的采集方式")
