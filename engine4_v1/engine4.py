from datetime import datetime, timezone
import json

from engine4_v1.db import fetch_one, fetch_all, execute
from engine4_v1.behavior_model import compute_loss_sensitivity
from engine4_v1.loss_simulator import simulate_loss_curve
from engine4_v1.curve_builder import derive_loss_profile
from engine4_v1.llm_explainer import build_loss_explanation


def run_engine4(user_id: int) -> dict:
    #ENGINE 1 DATA
    engine1 = fetch_one("""
        SELECT confidence_score, personality_type, archetype
        FROM engine1_scores
        WHERE user_id = %s
        ORDER BY run_timestamp DESC
        LIMIT 1
    """, (user_id,))

    if not engine1:
        raise ValueError("Engine1 data not found for user")

    confidence_score = float(engine1.get("confidence_score") or 50)
    personality_type = engine1.get("personality_type") or "The Safety Netter"
    archetype = engine1.get("archetype") or "The Minimalist"

    #EXPENSE DATA
    expenses = fetch_all("""
        SELECT amount
        FROM expenses
        WHERE user_id = %s
    """, (user_id,)) or []

    amounts = [float(e["amount"]) for e in expenses if e.get("amount") is not None] #list

    #EXPENSE VOLATILITY
    if amounts and max(amounts) > 0:
        expense_volatility = (max(amounts) - min(amounts)) / max(amounts)
    else:
        expense_volatility = 0.0

    #STRESS SPENDING EVENTS
    if amounts:
        avg = sum(amounts) / len(amounts)
        stress_spending_events = len([
            a for a in amounts if a > avg * 1.5
        ])
    else:
        stress_spending_events = 0

    #LOSS SENSITIVITY
    loss_sensitivity_index = compute_loss_sensitivity(
        confidence_score,
        expense_volatility,
        stress_spending_events
    )

    #LOSS SIMULATION
    loss_curve = simulate_loss_curve(loss_sensitivity_index)

    profile_data = derive_loss_profile(loss_curve)

    #EXPLANATION
    explanation = build_loss_explanation(
        personality_type,
        archetype,
        profile_data.get("loss_aversion_profile"),
        profile_data.get("safe_exposure_zone"),
        profile_data.get("critical_loss_zone")
    )

    #STORE OUTPUT
    execute("""
        INSERT INTO engine4_scores (
            user_id,
            run_timestamp,
            loss_curve,
            loss_aversion_profile,
            safe_exposure_zone,
            critical_loss_zone,
            ai_explanation
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (
        user_id,
        datetime.now(timezone.utc),
        json.dumps(loss_curve),
        profile_data.get("loss_aversion_profile"),
        profile_data.get("safe_exposure_zone"),
        profile_data.get("critical_loss_zone"),
        explanation
    ))

    return {
        "loss_aversion_curve": loss_curve,
        **profile_data,
        "ai_explanation": explanation
    }
