from typing import Dict, Any

def determine_archetype(q: Dict[str, Any]) -> str:
    """
    Financial Archetype determination using real user inputs.

    Archetypes:
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

    # 1. Stress & reaction behavior

    stress = str(q.get("stress_spending", "")).lower()
    reaction = str(q.get("reaction_to_expense", "")).strip()

    if stress == "yes":
        scores["Rag-to-Richess"] += 3

    if reaction == "3":          #stressful
        scores["Rag-to-Richess"] += 2
    elif reaction == "2":        # neutral
        scores["The Safety Netter"] += 1
    elif reaction == "1":        # manageable
        scores["The Safety Netter"] += 2

    # 2. Discipline & control

    track = str(q.get("track_expenses", "")).lower()
    budget = str(q.get("budget_discipline", "3"))
    adjust_freq = str(q.get("adjust_frequency", "3"))

    if track == "yes":
        scores["The Safety Netter"] += 3

    if budget in ("4", "5"):
        scores["The Safety Netter"] += 2

    if adjust_freq in ("4", "5"):
        scores["The Safety Netter"] += 1

    # 3. Spending style
    spending = str(q.get("spending_decision", "")).lower()
    if spending == "planned":
        scores["The Safety Netter"] += 2
    elif spending == "impulsive":
        scores["Rag-to-Richess"] += 2
    elif spending == "mix of both":
        scores["The Freedom Seeker"] += 1


    # 4. Ambition & dreams
    long_term = str(q.get("long_term_goal", "")).lower()
    goal_freq = str(q.get("goal_frequency", "3"))
    invest_conf = str(q.get("investment_confidence", "3"))

    if long_term == "yes":
        scores["The Big Dreamer"] += 2

    if goal_freq in ("4", "5"):
        scores["The Big Dreamer"] += 1

    if invest_conf in ("4", "5"):
        scores["The Big Dreamer"] += 2


    # 5. Savings & legacy orientation
    saving_pct = str(q.get("monthly_saving_percentage", "0"))
    saving_motive = str(q.get("saving_motivation", "")).lower()
    marital = str(q.get("marital_status", "")).lower()

    try:
        if int(saving_pct) >= 20:
            scores["The Legacy Builder"] += 3
        elif int(saving_pct) >= 10:
            scores["The Safety Netter"] += 1
    except:
        pass

    if any(word in saving_motive for word in ("family", "future", "care", "secure")):
        scores["The Legacy Builder"] += 2

    if marital == "married":
        scores["The Legacy Builder"] += 1


    # 6. Investment preference
    investment = str(q.get("preferred_investment", "")).lower()

    if investment in ("crypto", "stocks"):
        scores["The Trend Rider"] += 3
    elif investment in ("real estate", "gold"):
        scores["The Legacy Builder"] += 3


    # 7. Employment & independence
    employment = str(q.get("employment_status", "")).lower()
    extra_income = str(q.get("extra_income_action", "")).lower()

    if employment == "self-employed":
        scores["The Freedom Seeker"] += 3
    elif employment in ("private", "government"):
        scores["The Safety Netter"] += 1

    if extra_income in ("Mostly Save", "mix of both"):
        scores["The Freedom Seeker"] += 1


    # 8. Income reality (normalized)
    income_range = (
        str(q.get("annual_income_range", ""))
        .lower()
        .replace(" ", "")
    )

    if income_range == "under5l":
        scores["Rag-to-Richess"] += 2
    elif income_range in ("5l-15l", "15l-30l"):
        scores["The Big Dreamer"] += 2
    elif income_range == "30labove":
        scores["The Legacy Builder"] += 2

    #result determination
    return max(scores, key=scores.get)
