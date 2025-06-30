# app/services/api_service.py
import logging
from functools import lru_cache
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class ApiService:
    @staticmethod
    @lru_cache(maxsize=128)
    def process_api1():
        logger.info("Processing API 1 request")
        try:
            # 模拟业务逻辑
            return {"message": "This is API 1"}
        except Exception as e:
            logger.error(f"Error in API 1: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
