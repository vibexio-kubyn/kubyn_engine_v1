def apply_inconsistency(
    base_projection,
    confidence_score,
    contribution_rows
):
    """
    Applies behavioral inconsistency to monthly projections
    based on psychological risk + past saving discipline.
    """

    # SAFELY count zero or missed contributions
    zero_contrib_months = sum(
        1 for r in contribution_rows
        if r.get("current_saved", 0) <= 0
    )

    # Risk factors
    psychological_risk = (100 - confidence_score) / 100
    behavior_risk = min(0.3, zero_contrib_months * 0.05)

    total_risk = min(0.4, psychological_risk + behavior_risk)

    skip_every = max(3, int(1 / max(total_risk, 0.05)))

    adjusted = []
    for i, amount in enumerate(base_projection):
        if (i + 1) % skip_every == 0:
            continue
        adjusted.append(amount)

    return adjusted

