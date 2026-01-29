def derive_loss_profile(loss_curve):
    """
    Determines safe and critical zones + profile.
    """

    safe_zone = None
    critical_zone = None

    for point in loss_curve:
        if point["stability"] < 70 and safe_zone is None:
            safe_zone = point["loss_percent"]
        if point["stability"] < 40 and critical_zone is None:
            critical_zone = point["loss_percent"]

    if critical_zone is None:
        profile = "Resilient"
    elif critical_zone <= -12:
        profile = "Adaptive"
    elif critical_zone <= -8:
        profile = "Reactive"
    else:
        profile = "Avoidant"

    return {
        "loss_aversion_profile": profile,
        "safe_exposure_zone": safe_zone,
        "critical_loss_zone": critical_zone
    }
