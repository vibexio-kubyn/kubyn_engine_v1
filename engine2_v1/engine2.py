import sys

import os

import json

import traceback
 
# ✅ ADD PROJECT ROOT ONCE (VERY IMPORTANT)

PROJECT_ROOT = "/home/ubuntu/engine_v1"

if PROJECT_ROOT not in sys.path:

    sys.path.insert(0, PROJECT_ROOT)
 
from expense import analyse_expenses

from surplus import simulate_surplus

from llm_advice import generate_llm_suggestion

from db import execute
 
 
def run_engine2(user_id, days=7):

    """

    Runs Engine-2 end to end and stores outputs.

    """
 
    # 1. Expense analysis

    expense_summary = analyse_expenses(user_id, days)

    expense_total = expense_summary["total_spent"]
 
    # 2. Surplus simulation

    surplus_result = simulate_surplus(

        user_id=user_id,

        expense_total=expense_total

    )
 
    # 3. LLM suggestion

    recommendation = generate_llm_suggestion(

        user_id=user_id,

        expense_summary=expense_summary,

        goal_summary=surplus_result

    )
 
    # 4. Store Engine 2 output

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
 
    # Engine status tracking

    engine3_status = "not_run"

    engine3_error = None

    engine4_status = "not_run"

    engine4_error = None
 
    user_id_str = str(user_id)
 
    # ---------------- ENGINE 3 ----------------

    try:

        from engine3_v1.engine3 import run_engine3
 
        result = run_engine3(user_id_str)
 
        if result and "error" not in result:

            engine3_status = "completed"

        else:

            engine3_status = "failed"

            engine3_error = result.get("error") if result else "Unknown error"
 
    except ImportError as e:

        engine3_status = "import_error"

        engine3_error = str(e)

        traceback.print_exc()
 
    except Exception as e:

        engine3_status = "runtime_error"

        engine3_error = str(e)

        traceback.print_exc()
 
    # ---------------- ENGINE 4 ----------------

    try:

        from engine4_v1.engine4 import run_engine4
 
        result = run_engine4(user_id_str)
 
        if result and "error" not in result:

            engine4_status = "completed"

        else:

            engine4_status = "failed"

            engine4_error = result.get("error") if result else "Unknown error"
 
    except ImportError as e:

        engine4_status = "import_error"

        engine4_error = str(e)

        traceback.print_exc()
 
    except Exception as e:

        engine4_status = "runtime_error"

        engine4_error = str(e)

        traceback.print_exc()
 
    # Final response

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
 
    return response

 
