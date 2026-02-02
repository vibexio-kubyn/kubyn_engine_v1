from typing import Dict, Any

def determine_personality(q: Dict[str, Any]) -> str:
    """
    Six personalities:
    - The Adventurer
    - The Hedonist
    - The Minimalist
    - The Creator
    - The Achiever
    - The Caregiver
    """

    scores = {
        "The Adventurer": 0,
        "The Hedonist": 0,
        "The Minimalist": 0,
        "The Creator": 0,
        "The Achiever": 0,
        "The Caregiver": 0
    }

    # Emotional & stress spending
    stress = str(q.get("stress_spending", "")).lower()
    if stress == "yes":
        scores["The Hedonist"] += 3

    # Weekly spending intensity (numeric)
    weekly_raw = q.get("weekly_spending")
    try:
        weekly = int(str(weekly_raw))
        if weekly < 1000:
            scores["The Minimalist"] += 3
        elif weekly > 3000:
            scores["The Hedonist"] += 2
    except:
        pass

    # Spending decision style
    spending = str(q.get("spending_decision", "")).lower()
    if spending == "planned":
        scores["The Achiever"] += 2
    elif spending == "mix of both":
        scores["The Creator"] += 2
    elif spending == "impulsive":
        scores["The Hedonist"] += 2

 
    # Goal frequency (drive)
    goal_freq = str(q.get("goal_frequency", "3"))
    if goal_freq in ("4", "5"):
        scores["The Achiever"] += 3
    elif goal_freq in ("1", "2"):
        scores["The Adventurer"] += 1

    # Overspending category (values)
    overspend = str(q.get("overspend_category", "")).lower()
    if overspend in ("family", "education", "health","food"):
        scores["The Caregiver"] += 3
    elif overspend in ("shopping", "entertainment", "travel"):
        scores["The Hedonist"] += 2

    # Short-term goals (exploration)
    short_term = str(q.get("short_term_goal", "")).lower()
    if short_term == "yes":
        scores["The Adventurer"] += 3

    # Employment (achievement orientation)
    employment = str(q.get("employment_status", "")).lower()

    if employment in ("private", "government"):
        scores["The Achiever"] += 2
    elif employment == "self-employed":
        scores["The Creator"] += 2
    elif employment == "student":
        scores["The Adventurer"] += 1

    # Marital status (care orientation)
    marital = str(q.get("marital_status", "")).lower()
    if marital == "married":
        scores["The Caregiver"] += 2
    
    return max(scores, key=scores.get)
