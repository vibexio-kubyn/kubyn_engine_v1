from db import fetch_one, fetch_all, execute
from projection_core import build_monthly_projection
from behavior_adjuster import apply_inconsistency
from granularity_transformer import expand_granularity
from llm_explainer import build_explanation
from datetime import datetime
from decimal import Decimal
import json
 
def run_engine3(user_id):
    """
    Runs Engine 3 automatically after Engine 2
    """
    # ---- FETCH USER PREFERENCES ----
    prefs = fetch_one("""
        SELECT projection_years, ui_monthly_saving
        FROM user_preferences
        WHERE user_id = %s
        ORDER BY updated_at DESC
        LIMIT 1
    """, (user_id,))
    if not prefs:
        return {"error": "User preferences not found"}
    projection_years = int(prefs["projection_years"])
    ui_monthly_saving = float(prefs["ui_monthly_saving"])
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
        return {"error": "Engine 1 data not found"}
    confidence_score = float(engine1["confidence_score"])
    # ---- EXPENSES (LAST 3 MONTHS) ----
    expense_row = fetch_one("""
        SELECT IFNULL(SUM(amount),0)/3 AS avg_monthly_expense
        FROM expenses
        WHERE user_id = %s
          AND created_at >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH)
          AND type = 'expense'
    """, (user_id,))
    avg_monthly_expense = float(expense_row["avg_monthly_expense"] or 0)
    # ---- MONTHLY INCOME ----
    income_row = fetch_one("""
        SELECT IFNULL(SUM(amount),0) AS monthly_income
        FROM expenses
        WHERE user_id = %s AND type = 'income'
    """, (user_id,))
    monthly_income = float(income_row["monthly_income"] or 0)
    max_sustainable_saving = max(0, monthly_income - avg_monthly_expense)
    effective_monthly_saving = min(ui_monthly_saving, max_sustainable_saving)
    # ---- ENGINE 2 CONTRIBUTIONS ----
    contributions = fetch_all("""
        SELECT amount
        FROM goal_contributions
        WHERE user_id = %s
    """, (user_id,))
    # Convert Decimal to float
    contributions = [{"amount": float(c["amount"])} for c in contributions]
    # ---- PROJECTIONS ----
    consistent = build_monthly_projection(effective_monthly_saving, months)
    inconsistent = apply_inconsistency(
        consistent,
        confidence_score,
        contributions
    )
    consistent_years = len(consistent) // 12
    inconsistent_years = len(inconsistent) // 12
    consistent_series = expand_granularity(consistent)
    inconsistent_series = expand_granularity(inconsistent)
    # ---- AI EXPLANATION ----
    explanation = build_explanation(
        confidence_score,
        engine1["personality_type"],
        engine1["archetype"],
        consistent_years,
        inconsistent_years
    )
    # ---- STORE OUTPUT ----
    execute("""
        INSERT INTO engine3_projections
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
            "effective_monthly_saving": effective_monthly_saving,
            "avg_monthly_expense": avg_monthly_expense
        },
        "ai_explanation": explanation
    }
