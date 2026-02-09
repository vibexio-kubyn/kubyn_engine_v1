def apply_inconsistency(
    base_projection: list,
    confidence_score: float,
    contribution_rows: list
) -> list:
    """
    Applies behavioral inconsistency to monthly projections
    by reducing savings in certain months instead of removing them.
    """

    if not base_projection:
        return []

    confidence_score = confidence_score or 50  # safe default

    # Count missed or zero contributions
    zero_contrib_months = sum(
        1 for r in contribution_rows
        if r.get("current_saved", 0) <= 0
    )

    # Risk factors
    psychological_risk = (100 - confidence_score) / 100
    behavior_risk = min(0.3, zero_contrib_months * 0.05)

    total_risk = min(0.4, psychological_risk + behavior_risk)

    # Determine how often inconsistency happens
    skip_every = max(3, min(12, int(1 / max(total_risk, 0.05))))

    adjusted = []
    running_total = 0.0

    for i, month in enumerate(base_projection):
        value = month["value"]

        # Bad saving month → partial saving
        if (i + 1) % skip_every == 0:
            value *= 0.5  # lose 50% savings this month

        running_total = value

        adjusted.append({
            **month,
            "value": round(running_total, 2)
        })

    return adjusted