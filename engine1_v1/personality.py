def determine_personality(q):
    """
    Six personality matches:
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

    stress_spending = q.get("stress_spending", "")
    if stress_spending == "Yes":
        scores["The Hedonist"] += 4

    weekly_spending = q.get("weekly_spending", q.get("spending_level", "medium"))
    if weekly_spending == "low":
        scores["The Minimalist"] += 5
    elif weekly_spending == "high":
        scores["The Hedonist"] += 3

    spending_decision = q.get("spending_decision", "")
    if spending_decision == "Mix of both":
        scores["The Creator"] += 3
    elif spending_decision == "Planned":
        scores["The Achiever"] += 2

    goal_frequency = q.get("goal_frequency", "")
    if goal_frequency == "3" or "monthly" in str(goal_frequency).lower():
        scores["The Achiever"] += 5

    overspend_category = q.get("overspend_category", q.get("spending_category", ""))
    if overspend_category == "Family":
        scores["The Caregiver"] += 5
    elif overspend_category == "Entertainment":
        scores["The Hedonist"] += 3

    short_term_goal = q.get("short_term_goal", "")
    if short_term_goal == "Yes":
        scores["The Adventurer"] += 4

    # Demographic factors
    employment_status = q.get("employment_status", "")
    if "salaried" in employment_status.lower():
        scores["The Achiever"] += 2
    
    marital_status = q.get("marital_status", "")
    if "married" in marital_status.lower():
        scores["The Caregiver"] += 3

    return max(scores, key=scores.get)
