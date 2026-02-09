def build_loss_explanation(
    personality_type,
    archetype,
    loss_profile,
    safe_zone,
    critical_zone
) -> str:

    personality_type = personality_type or "balanced"
    archetype = archetype or "planner"
    loss_profile = loss_profile or "unknown"

    # ---- SAFE ZONE TEXT ----
    if safe_zone is not None:
        safe_text = (
            f"You tend to remain stable until losses approach around "
            f"{abs(safe_zone)}%, after which emotional pressure increases."
        )
    else:
        safe_text = (
            "You demonstrate strong emotional stability across moderate losses."
        )

    # ---- CRITICAL ZONE TEXT ----
    if critical_zone is not None:
        critical_text = (
            f"Beyond approximately {abs(critical_zone)}% loss, discipline "
            f"and consistency are likely to break down."
        )
    else:
        critical_text = (
            "Even under significant losses, you are likely to maintain discipline."
        )

    return (
        f"Based on your behavioral patterns and past responses to stress, "
        f"your loss aversion profile is classified as {loss_profile}. "
        f"{safe_text} {critical_text}\n\n"
        f"Given your {personality_type} personality and {archetype} archetype, "
        f"gradual exposure with clearly defined loss boundaries helps protect "
        f"long-term financial progress."
    )
