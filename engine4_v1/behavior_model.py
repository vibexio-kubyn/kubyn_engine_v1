def compute_loss_sensitivity(
    confidence_score: float,
    expense_volatility: float,
    stress_spending_events: int
) -> float:
    """
    Returns Loss Sensitivity Index (0-1).
    Higher = more loss averse.
    """

    #SAFETY DEFAULTS
    confidence_score = confidence_score if confidence_score is not None else 50
    confidence_score = max(0.0, min(confidence_score, 100.0))

    expense_volatility = max(0.0, min(expense_volatility, 1.0))
    stress_spending_events = max(0, stress_spending_events)

    #FACTORS
    confidence_factor = (100.0 - confidence_score) / 100.0
    volatility_factor = expense_volatility
    stress_factor = min(1.0, stress_spending_events * 0.1)

    #WEIGHTED SCORE
    lsi = (
        0.5 * confidence_factor +
        0.3 * volatility_factor +
        0.2 * stress_factor
    )

    return min(1.0, lsi)
