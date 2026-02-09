def derive_loss_profile(loss_curve: list) -> dict:
    """
    Determines loss aversion profile and exposure zones
    based on stability thresholds.
    """

    if not loss_curve:
        return {
            "loss_aversion_profile": "Unknown",
            "safe_exposure_zone": None,
            "critical_loss_zone": None
        }

    safe_breach = None
    critical_breach = None

    for point in loss_curve:
        stability = point["stability"]
        loss = point["loss_percent"]

        if stability < 70 and safe_breach is None:
            safe_breach = loss

        if stability < 40 and critical_breach is None:
            critical_breach = loss

    # ---- PROFILE CLASSIFICATION ----
    if critical_breach is None:
        profile = "Resilient"
    elif critical_breach <= -12:
        profile = "Adaptive"
    elif -12 < critical_breach <= -8:
        profile = "Reactive"
    else:
        profile = "Avoidant"

    return {
        "loss_aversion_profile": profile,
        "safe_exposure_zone": safe_breach,
        "critical_loss_zone": critical_breach
    }
