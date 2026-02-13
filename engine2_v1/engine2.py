import json
import logging
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("engine2-core")

from expense import analyse_expenses
from surplus import simulate_surplus
from llm_advice import generate_llm_suggestion
from db import execute

def run_engine2(user_id, days=7):
    """
    Runs Engine-2 end to end and stores outputs.
    """
    logger.info(f"Engine-2 started | user_id={user_id}")

    # 1. Expense analysis for the past 7 days.
    try:
        expense_summary = analyse_expenses(user_id, days) #calculating expense for last 7 days.
        expense_total = expense_summary.get("total_spent", 0) # for the past 7 days.
    except Exception as e:
        logger.exception("Expense analysis failed")
        raise RuntimeError("Expense analysis failed") from e

    # 2. Surplus simulation 
    try:
        surplus_result = simulate_surplus(user_id=user_id)
    except Exception as e:
        logger.exception("Surplus simulation failed")
        raise 

    # 3. LLM suggestion
    try:
        recommendation = generate_llm_suggestion(
            user_id=user_id,
            expense_summary=expense_summary,
            goal_summary=surplus_result
        )
    except Exception as e:
        logger.exception("LLM advice generation failed")
        recommendation = "AI advice could not be generated at this time."

    #4. Store Engine-2 output
    try:
        execute("""
            INSERT INTO engine2_scores
            (user_id, runTimestamp, llm_explainer,
             surplus_snapshot, expense_snapshot, engine_version)
            VALUES (%s, NOW(), %s, %s, %s, %s)
        """, (
            user_id,
            recommendation,
            json.dumps(surplus_result, default=str),
            json.dumps(expense_summary, default=str),
            "v1"
        ))
    except Exception:
        logger.exception("Failed to store Engine-2 results (continuing)")

    # ENGINE 3 & 4 STATUS
    engine3_status, engine3_error = "not_run", None
    engine4_status, engine4_error = "not_run", None

    user_id_str = str(user_id)

    #ENGINE 3
    try:
        from engine3_v1.engine3 import run_engine3
        result = run_engine3(user_id_str)

        if result and "error" not in result:
            engine3_status = "completed"
        else:
            engine3_status = "failed"
            engine3_error = result.get("error") if result else "Unknown error"

    except Exception as e:
        engine3_status = "error"
        engine3_error = str(e)
        logger.exception("Engine-3 execution failed")

    #ENGINE 4
    try:
        from engine4_v1.engine4 import run_engine4
        result = run_engine4(user_id_str)

        if result and "error" not in result:
            engine4_status = "completed"
        else:
            engine4_status = "failed"
            engine4_error = result.get("error") if result else "Unknown error"

    except Exception as e:
        engine4_status = "error"
        engine4_error = str(e)
        logger.exception("Engine-4 execution failed")

    #FINAL RESPONSE
    response = {
        "expense_analysis": expense_summary,
        "surplus_simulation": surplus_result,
        "ai_suggestion": recommendation,
        "engine3_status": engine3_status,
        "engine4_status": engine4_status
    }

    if engine3_error:
        response["engine3_error"] = engine3_error

    if engine4_error:
        response["engine4_error"] = engine4_error

    logger.info(f"Engine-2 completed | user_id={user_id}")

    return response
