def determine_archetype(q):
    """
    6 Archetypes logic:
    - Rag-to-Richess
    - The Safety Netter
    - The Trend Rider
    - The Freedom Seeker
    - The Big Dreamer
    - The Legacy Builder
    """

    scores = {
        "Rag-to-Richess": 0,
        "The Safety Netter": 0,
        "The Trend Rider": 0,
        "The Freedom Seeker": 0,
        "The Big Dreamer": 0,
        "The Legacy Builder": 0
    }

    # Map kubyn-backend field names
    stress_spending = q.get("stress_spending", "")
    if stress_spending == "Yes":
        scores["Rag-to-Richess"] += 3

    track_expenses = q.get("track_expenses", "")
    if track_expenses == "Yes":
        scores["The Safety Netter"] += 3

    preferred_investment = q.get("preferred_investment", q.get("investment_preference", ""))
    if "crypto" in preferred_investment.lower():
        scores["The Trend Rider"] += 5

    employment_status = q.get("employment_status", "")
    if "self-employed" in employment_status.lower():
        scores["The Freedom Seeker"] += 5
    elif "salaried" in employment_status.lower():
        scores["The Safety Netter"] += 2

    long_term_goal = q.get("long_term_goal", q.get("ultimate_goal", ""))
    if "yes" in str(long_term_goal).lower() or "financial" in str(long_term_goal).lower():
        scores["The Big Dreamer"] += 5

    saving_motivation = q.get("saving_motivation", q.get("saving_motivation", ""))
    if "legacy" in str(saving_motivation).lower():
        scores["The Legacy Builder"] += 5

    # Income-based archetype hints
    if "annual_income_range" in q:
        income_range = q["annual_income_range"]
        if "10" in income_range or "15" in income_range or "20" in income_range:
            scores["The Big Dreamer"] += 2
            scores["The Legacy Builder"] += 1

    # return max category
    return max(scores, key=scores.get)
