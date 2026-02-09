def build_explanation(
    confidence_score,
    personality_type,
    archetype,
    consistent_years,
    inconsistent_years
) -> str:
    confidence_score = round(confidence_score or 50)

    personality_type = personality_type or "balanced"
    archetype = archetype or "planner"

    delay = inconsistent_years - consistent_years

    if delay > 0:
        delay_text = (
            f"Skipping contributions, even occasionally, can delay your progress "
            f"by around {delay} year{'s' if delay > 1 else ''}, "
            f"pushing this closer to {inconsistent_years} years."
        )
    else:
        delay_text = (
            "Even with occasional inconsistencies, your long-term timeline "
            "remains largely unchanged."
        )

    return (
        f"You are on track to reach your goal in approximately {consistent_years} years "
        f"if your savings remain consistent. {delay_text}\n\n"
        f"Given your {personality_type} personality and {archetype} archetype, "
        f"small behavioral defaults matter more than intensity. "
        f"Your confidence score of {confidence_score} suggests that automation and "
        f"consistency can protect your progress without added stress."
    )
