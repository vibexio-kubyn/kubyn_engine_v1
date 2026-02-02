from datetime import datetime
from typing import Dict, Any


def calculate_confidence(user_context: Dict[str, Any], q: Dict[str, Any]) -> int:
    """
    Confidence score based on core factors:
    - investment_confidence
    - budget discipline
    - reaction_to_expense
    - compare_with_peers
    - personality stability proxies
    """

    score = 50  # base neutral score

    # Investment confidence (1–5)
    ic = int(q.get("investment_confidence", 3))
    score += (ic - 3) * 6

    # Budget discipline (1–5)
    bd = int(q.get("budget_discipline", 3))
    score += (bd - 3) * 5

    # Reaction to expense (1–3)
    reaction_map = {
        1: -4,  # stressful
        2: 0,   # neutral
        3:4,   # manageable
    }
    reaction = int(q.get("reaction_to_expense", 2))
    score += reaction_map.get(reaction, 0)

    # Peer comparison (emotional stability indicator)
    peer = q.get("compare_with_peers", "").lower()
    if peer == "no":
        score += 4
    elif peer == "sometimes":
        score += 1
    elif peer == "yes":
        score -= 4

    # Additional confidence factors
    spending_decision = q.get("spending_decision", "").lower()
    if spending_decision == "planned":
        score += 4
    elif spending_decision == "mixofboth":
        score += 0
    elif spending_decision == "impulsive":
        score -= 5
    
    # Advice preference
    advice = q.get("advice_preference", "").lower()
    if advice == "expert":
        score += 3
    elif advice == "self-research":
        score += 2
    elif advice == "friends":
        score += 0

    #track_expenses
    track = q.get("track_expenses", "").lower()
    if track == "yes":
        score += 3
    elif track == "sometimes":
        score += 1
    elif track == "no":
        score -= 3
    
    # Add demographic factors (if available)
    employment = q.get("employment_status", "").lower()
    if employment == "government":
        score += 4
    elif employment == "private":
        score += 3
    elif employment == "self-employed":
        score += 2
    elif employment == "student":
        score += 0

    # Age factor (if dob available)
    dob = q.get("dob")
    if dob:
        try:
            dob_date = datetime.strptime(dob, "%d-%m-%Y")
            age = (datetime.now() - dob_date).days // 365
            if age > 30:
                score += 3
            elif age > 25:
                score += 2
        except:
            pass

    # Clamp 0–100
    return max(0, min(100, score))
