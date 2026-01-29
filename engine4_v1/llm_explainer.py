def build_loss_explanation(
    personality_type,
    archetype,
    loss_profile,
    safe_zone,
    critical_zone
):
    return (
        f"Based on your behavioral patterns and past responses to stress, "
        f"your loss aversion profile is classified as {loss_profile}. "
        f"You tend to remain stable until losses approach around "
        f"{abs(safe_zone)}%, after which emotional pressure increases. "
        f"Beyond approximately {abs(critical_zone)}% loss, discipline "
        f"and consistency are likely to break down.\n\n"
        f"Given your {personality_type} personality and {archetype} archetype, "
        f"gradual exposure with clearly defined loss boundaries helps protect "
        f"long-term financial progress."
    )
