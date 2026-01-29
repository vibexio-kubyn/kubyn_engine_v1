def simulate_loss_curve(loss_sensitivity_index):
    """
    Simulates behavioral stability under progressive losses.
    """

    curve = []
    base_stability = 100

    for loss in range(0, -22, -2):  # 0 to -20
        loss_impact = abs(loss) * (1 + loss_sensitivity_index)
        stability = max(0, base_stability - loss_impact * 4)

        curve.append({
            "loss_percent": loss,
            "stability": round(stability, 2)
        })

    return curve
