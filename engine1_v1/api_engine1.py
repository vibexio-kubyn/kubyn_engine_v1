import sys
import os
from fastapi import FastAPI

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = FastAPI(title="Engine 1: Behaviour, Personality & Archetypes")

@app.get("/")
def root():
    return {
        "message": "Engine 1 API is running",
        "endpoints": {
            "GET /": "This info",
            "GET /health": "Health check",
            "POST /compute_score": "Process user data"
        }
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "engine": "engine1",
        "version": "1.0"
    }

@app.post("/compute_score")
def compute_score(payload: dict):
    """Process user data through Engine 1"""
    print(f"\n📨 Received request for users: {payload.get('user_id', [])}")
    
    try:
        # Dynamically execute engine1.py to import its functions
        import importlib.util
        
        # Get the path to engine1.py
        engine1_path = os.path.join(os.path.dirname(__file__), "engine1.py")
        
        # Load module from file
        spec = importlib.util.spec_from_file_location("engine1_module", engine1_path)
        engine1_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(engine1_module)
        
        user_ids = payload.get("user_id", [])
        answers = payload.get("answers", {})
        
        if not user_ids:
            return {"status": "error", "message": "No user_id provided"}
        
        results = {}
        for user_id in user_ids:
            print(f"🔧 Processing user {user_id}...")
            
            user_data = {"id": user_id}
            result = engine1_module.process_engine_one(user_data, answers)
            
            # Try to store in database
            try:
                engine1_module.store_engine1_output(user_id, result)
                print(f"💾 Stored results for user {user_id}")
            except Exception as e:
                print(f"⚠️  Storage failed for user {user_id}: {e}")
                # Continue without storage
            
            results[user_id] = result
        
        print(f"✅ Processed {len(user_ids)} users")
        return {
            "status": "success",
            "message": "Engine 1 processing completed",
            "results": results
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": f"Processing error: {str(e)}"}
