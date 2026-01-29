from fastapi import FastAPI
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI(title="Surplus Simulation Engine")

@app.get("/health")
def health():
    return {"status": "healthy", "engine": "surplus_simulation"}

@app.get("/")
def root():
    return {"message": "Surplus Simulation Engine API"}

@app.post("/run")
async def run_engine(data: dict):
    try:
        # Fix import - check what module exists
        try:
            from app import run_engine2
        except ImportError:
            # Maybe the file has a different name
            import engine2
            run_engine2 = engine2.run_engine2
        
        user_id = data.get("user_id")
        monthly_income = data.get("monthly_income", 5000)
        
        if not user_id:
            return {"error": "Missing user_id"}
        
        result = run_engine2(user_id, monthly_income)
        return {"success": True, "result": result}
    except Exception as e:
        import traceback
        return {"error": str(e), "traceback": traceback.format_exc()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
