def compute_loss_sensitivity(
    confidence_score,
    expense_volatility,
    stress_spending_events
):
    """
    Returns Loss Sensitivity Index (0–1).
    Higher = more loss averse.
    """

    confidence_factor = (100 - confidence_score) / 100
    volatility_factor = min(1.0, expense_volatility)
    stress_factor = min(1.0, stress_spending_events * 0.1)

    lsi = (
        0.5 * confidence_factor +
        0.3 * volatility_factor +
        0.2 * stress_factor
    )

    return min(1.0, round(lsi, 2))
