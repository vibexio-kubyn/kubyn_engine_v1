def build_explanation(
    confidence_score,
    personality_type,
    archetype,
    consistent_years,
    inconsistent_years
):
    delay = inconsistent_years - consistent_years

    return (
        f"You are on track to reach your goal in approximately {consistent_years} years "
        f"if your savings remain consistent. Skipping contributions, even occasionally, "
        f"pushes this timeline closer to {inconsistent_years} years.\n\n"
        f"Given your {personality_type} personality and {archetype} archetype, "
        f"small behavioral defaults matter more than intensity. "
        f"Your confidence score of {confidence_score} suggests that automation and "
        f"consistency can protect your progress without added stress."
    )
