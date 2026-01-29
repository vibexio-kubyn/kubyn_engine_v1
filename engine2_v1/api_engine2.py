import sys
import os
from fastapi import FastAPI

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = FastAPI(title="Engine 2 API")

@app.get("/")
def root():
    return {"message": "Engine 2 API - Financial Advice Engine"}

@app.get("/health")
def health():
    return {"status": "healthy", "engine": "engine2"}

@app.post("/engine2/process")
def trigger_engine2(payload: dict):
    """
    Triggers Engine 2 when finance / goal events happen
    """

    print("ENGINE 2 API HIT")
    print("PAYLOAD:", payload)

    user_id = payload.get("user_id")

    if not user_id:
        return {"status": "error", "message": "user_id missing"}

    try:
        # Import engine2 module
        import engine2
        # CALL ENGINE 2 CORE
        result = engine2.run_engine2(user_id=user_id)

        return {
            "status": "success",
            "engine": "engine2",
            "result": result
        }
    except ImportError as e:
        return {"status": "error", "message": f"Cannot import engine2: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Engine 2 processing error: {str(e)}"}
