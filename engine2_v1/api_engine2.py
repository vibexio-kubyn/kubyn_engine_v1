import sys
import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import engine2
from engine2 import run_engine2

# Logging config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("engine2-api")

app = FastAPI(title="Engine 2 API")

class Engine2Payload(BaseModel):
    user_id: int
    model_config =ConfigDict(extra="allow")

@app.get("/")
def root():
    return {"message": "Engine 2 API - Financial Advice Engine"}

@app.get("/health")
def health():
    return {"status": "healthy", "engine": "engine2"}

@app.post("/engine2/process")
def trigger_engine2(payload: Engine2Payload):
    """
    Triggers Engine 2 when finance / goal events happen
    """
    logger.info("ENGINE 2 API HIT")
    logger.info(f"FULL PAYLOAD={payload.model_dump()}")

    try:
        result =run_engine2(user_id=payload.user_id)

        return {
            "status": "success",
            "engine": "engine2",
            "result": result
        }

    except Exception as e:
        logger.exception("Engine 2 processing failed")
        raise HTTPException(
            status_code=500,
            detail=f"Engine 2 processing error: {str(e)}"
        )