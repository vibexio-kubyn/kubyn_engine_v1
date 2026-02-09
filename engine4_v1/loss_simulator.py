def simulate_loss_curve(loss_sensitivity_index: float) -> list:
    """
    Simulates behavioral stability under progressive financial losses.
    Higher loss sensitivity leads to faster stability decay.
    """

    #SAFETY CLAMPS
    if loss_sensitivity_index is None:
        loss_sensitivity_index = 0.5

    loss_sensitivity_index = max(0.0, min(loss_sensitivity_index, 1.0))

    #CONFIG
    BASE_STABILITY = 100
    MAX_LOSS = 20          # percent
    LOSS_STEP = 2          # percent
    IMPACT_MULTIPLIER = 3  # softness of curve

    curve = []

    for loss in range(0, -(MAX_LOSS + LOSS_STEP), -LOSS_STEP):
        loss_impact = abs(loss) * (1 + loss_sensitivity_index)
        stability = max(
            0.0,
            BASE_STABILITY - loss_impact * IMPACT_MULTIPLIER
        )

        curve.append({
            "loss_percent": loss,
            "stability": round(stability, 2)
        })

    return curve
