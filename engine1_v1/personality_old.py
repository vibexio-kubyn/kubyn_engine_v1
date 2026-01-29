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

    if q.get("stress_spending") == "Yes":
        scores["The Hedonist"] += 4

    if q.get("weekly_spending") == "low":
        scores["The Minimalist"] += 5

    if q.get("spending_decision") == "Mix of both":
        scores["The Creator"] += 3

    if q.get("goal_frequency") == "3":
        scores["The Achiever"] += 5

    if q.get("overspend_category") == "Family":
        scores["The Caregiver"] += 5

    if q.get("short_term_goal") == "Yes":
        scores["The Adventurer"] += 4

    return max(scores, key=scores.get)
