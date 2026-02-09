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

    user_ids = payload.get("user_id")
    answers = payload.get("answers")

    if not user_ids or not isinstance(user_ids, list):
        raise HTTPException(status_code=400, detail="user_id must be a list")

    if not answers or not isinstance(answers, dict):
        raise HTTPException(status_code=400, detail="answers must be a valid object")

    user_id = user_ids[0]

    try:
        logger.info(f"Starting Engine-1 processing for user {user_id}")

        user_context = {"id": user_id}
        result = process_engine_one(user_context, answers)

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