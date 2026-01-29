from engine3_v1.db import fetch_one, fetch_all, execute
 
from engine3_v1.projection_core import build_monthly_projection

from engine3_v1.behaviour_adjuster import apply_inconsistency

from engine3_v1.granularity_transformer import expand_granularity

from engine3_v1.llm_explainer import build_explanation
 
from datetime import datetime

import json
 
 
def run_engine3(user_id):

    """

    Runs Engine 3 automatically after Engine 2

    """
 
    # ---- SIMULATION HORIZON ----

    projection_years = 10

    months = projection_years * 12
 
    # ---- ENGINE 1 DATA ----

    engine1 = fetch_one("""

        SELECT confidence_score, personality_type, archetype

        FROM engine1_scores

        WHERE user_id = %s

        ORDER BY run_timestamp DESC

        LIMIT 1

    """, (user_id,))
 
    if not engine1:

        raise ValueError("Engine1 data not found for user")
 
    # ---- EXPENSES (LAST 3 MONTHS AVG) ----

    expense_row = fetch_one("""

        SELECT IFNULL(SUM(amount), 0) / 3 AS avg_monthly_expense

        FROM expenses

        WHERE user_id = %s

          AND created_at >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH)

    """, (user_id,))
 
    avg_monthly_expense = float(expense_row["avg_monthly_expense"])
 
    # ---- MONTHLY INCOME ----
    income_row = fetch_one("""
        SELECT IFNULL(SUM(amount), 0) AS monthly_income
        FROM incomes
        WHERE user_id = %s
        AND YEAR(created_at) = YEAR(CURDATE())
        AND MONTH(created_at) = MONTH(CURDATE())
    """, (user_id,))
 
    monthly_income = float(income_row["monthly_income"])
 
    # ---- DERIVED SAVING ----

    ui_monthly_saving = max(0.0, monthly_income - avg_monthly_expense)

    effective_monthly_saving = ui_monthly_saving
 
    # ---- ENGINE 2 GOALS ----

    goals = fetch_all("""

        SELECT target_amount, current_saved

        FROM goals

        WHERE user_id = %s

    """, (user_id,))
 
    # ---- PROJECTIONS ----

    consistent = build_monthly_projection(

        effective_monthly_saving,

        months

    )
 
    inconsistent = apply_inconsistency(

        consistent,

        engine1["confidence_score"],

        goals

    )
 
    consistent_years = len(consistent) // 12

    inconsistent_years = len(inconsistent) // 12
 
    consistent_series = expand_granularity(consistent)

    inconsistent_series = expand_granularity(inconsistent)
 
    # ---- AI EXPLANATION ----

    explanation = build_explanation(

        engine1["confidence_score"],

        engine1["personality_type"],

        engine1["archetype"],

        consistent_years,

        inconsistent_years

    )
 
    # ---- STORE OUTPUT ----

    execute("""

        INSERT INTO engine3_scores

        (user_id, run_timestamp, projection_granularity,

         consistent_projection, inconsistent_projection,

         consistent_goal_year, inconsistent_goal_year,

         ai_explanation)

        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)

    """, (

        user_id,

        datetime.utcnow(),

        "all",

        json.dumps(consistent_series),

        json.dumps(inconsistent_series),

        consistent_years,

        inconsistent_years,

        explanation

    ))
 
    return {

        "projection": {

            "consistent": consistent_series,

            "inconsistent": inconsistent_series

        },

        "goal_timeline": {

            "consistent_years": consistent_years,

            "inconsistent_years": inconsistent_years

        },

        "constraints": {

            "ui_monthly_saving": ui_monthly_saving,

            "avg_monthly_expense": avg_monthly_expense,

            "monthly_income": monthly_income

        },

        "ai_explanation": explanation

    }

 
