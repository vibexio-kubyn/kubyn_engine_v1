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

    if q.get("stress_spending") == "Yes":
        scores["Rag-to-Richess"] += 3

    if q.get("track_expenses") == "Yes":
        scores["The Safety Netter"] += 3

    if q.get("preferred_investment") == "Crypto":
        scores["The Trend Rider"] += 5

    if q.get("employment_status") == "Self-employed":
        scores["The Freedom Seeker"] += 5

    if q.get("long_term_goal") == "Yes":
        scores["The Big Dreamer"] += 5

    if q.get("saving_motivation") == "legacy":
        scores["The Legacy Builder"] += 5

    # return max category
    return max(scores, key=scores.get)
