import sys
import os
from fastapi import FastAPI, HTTPException
from typing import Dict, Any
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)
# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine1 import process_engine_one, store_engine1_output

app = FastAPI(title="Engine 1: Behaviour, Personality & Archetypes")

@app.get("/")
def root():
    return {
        "message": "Engine 1 API is running",
        "endpoints": {
            "GET /": "This info",
            "GET /health": "Health check",
            "POST /compute_score": "Process single user data"
        }
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "engine": "engine1",
        "version": "1.2"
    }

@app.post("/compute_score")
def compute_score(payload: Dict[str, Any]):
    """
    Expected payload:
    {
        "user_id": "1",
        "answer": { ... }
    }
    """

    user_id = payload.get("user_id")
    answer = payload.get("answer")

    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")

    if not answer or not isinstance(answer, dict):
        raise HTTPException(status_code=400, detail="answer must be a valid object")

    try:
        logger.info(f"Starting Engine-1 processing for user {user_id}")

        user_context = {"id": user_id}
        result = process_engine_one(user_context, answer)

        store_engine1_output(user_id, result)

        return {
            "status": "success",
            "user_id": user_id,
            "engine": "engine1",
            "result": result
        }
    except ValueError as e:
        logger.warning(f"Validation error for user {user_id}: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Engine-1 crashed for user {user_id}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Engine-1 processing failed: {str(e)}"
        )
