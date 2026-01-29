from engine4_v1.db import fetch_one, fetch_all, execute
 
from engine4_v1.behavior_model import compute_loss_sensitivity

from engine4_v1.loss_simulator import simulate_loss_curve

from engine4_v1.curve_builder import derive_loss_profile

from engine4_v1.llm_explainer import build_loss_explanation
 
from datetime import datetime

from decimal import Decimal

import json
 
 
def run_engine4(user_id):

    # ---- ENGINE 1 ----

    engine1 = fetch_one("""

        SELECT confidence_score, personality_type, archetype

        FROM engine1_scores

        WHERE user_id = %s

        ORDER BY run_timestamp DESC

        LIMIT 1

    """, (user_id,))
 
    if not engine1:

        raise ValueError("Engine1 data not found for user")
 
    # ---- EXPENSE DATA ----

    expenses = fetch_all("""

        SELECT amount

        FROM expenses

        WHERE user_id = %s

    """, (user_id,))
 
    amounts = [e["amount"] for e in expenses]
 
    # ---- EXPENSE VOLATILITY (FLOAT SAFE) ----

    expense_volatility = float(

        (max(amounts) - min(amounts)) / max(amounts)

    ) if amounts else 0.0
 
    # ---- STRESS SPENDING EVENTS (DECIMAL SAFE) ----

    if amounts:

        avg = sum(amounts) / Decimal(len(amounts))

        stress_spending_events = len([

            a for a in amounts

            if a > avg * Decimal("1.5")

        ])

    else:

        stress_spending_events = 0
 
    # ---- LOSS SENSITIVITY ----

    lsi = compute_loss_sensitivity(

        float(engine1["confidence_score"]),

        expense_volatility,

        stress_spending_events

    )
 
    # ---- SIMULATION ----

    loss_curve = simulate_loss_curve(lsi)
 
    profile_data = derive_loss_profile(loss_curve)
 
    # ---- AI EXPLANATION ----

    explanation = build_loss_explanation(

        engine1["personality_type"],

        engine1["archetype"],

        profile_data["loss_aversion_profile"],

        profile_data["safe_exposure_zone"],

        profile_data["critical_loss_zone"]

    )
 
    # ---- STORE OUTPUT ----

    execute("""

        INSERT INTO engine4_scores

        (user_id, run_timestamp, loss_curve,

         loss_aversion_profile, safe_exposure_zone,

         critical_loss_zone, ai_explanation)

        VALUES (%s,%s,%s,%s,%s,%s,%s)

    """, (

        user_id,

        datetime.utcnow(),

        json.dumps(loss_curve),

        profile_data["loss_aversion_profile"],

        profile_data["safe_exposure_zone"],

        profile_data["critical_loss_zone"],

        explanation

    ))
 
    return {

        "loss_aversion_curve": loss_curve,

        **profile_data,

        "ai_explanation": explanation

    }

 
