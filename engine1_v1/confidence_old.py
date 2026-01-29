def map_to_numeric(value, default=3):
    """
    Map string values to numeric scores (1-5 scale)
    """
    if isinstance(value, (int, float)):
        return int(max(1, min(5, value)))  # Clamp to 1-5
    
    if isinstance(value, str):
        value_lower = value.lower().strip()
        
        # Map common string values to 1-5 scale
        mapping = {
            # Scale 1-5 mappings
            "very low": 1, "low": 2, "medium": 3, "high": 4, "very high": 5,
            "none": 1, "rarely": 2, "sometimes": 3, "often": 4, "always": 5,
            "never": 1, "occasionally": 2, "regularly": 3, "frequently": 4,
            "poor": 1, "fair": 2, "good": 3, "very good": 4, "excellent": 5,
            "strongly disagree": 1, "disagree": 2, "neutral": 3, "agree": 4, "strongly agree": 5,
            
            # Specific values from your data
            "analyze": 4,  # Good reaction
            "expert": 4,   # Preference for expert advice
            "planned": 4,  # Planned spending
        }
        
        if value_lower in mapping:
            return mapping[value_lower]
        
        # Try to extract number from string
        try:
            # Remove non-numeric characters except minus and dot
            import re
            numbers = re.findall(r'-?\d+\.?\d*', value)
            if numbers:
                num = float(numbers[0])
                return int(max(1, min(5, num)))
        except:
            pass
    
    return default  # Default to middle value (3)

def calculate_confidence(user, q):
    """
    Confidence score based on core factors:
    - investment_confidence
    - budget discipline
    - reaction_to_expense
    - compare_with_peers
    - personality stability proxies
    """

    score = 50  # base neutral score

    # Investment confidence (1–5)
    ic = map_to_numeric(q.get("investment_confidence", "Medium"))
    score += (ic - 3) * 6

    # Budget discipline (1–5)
    bd = map_to_numeric(q.get("budget_discipline", "Medium"))
    score += (bd - 3) * 5

    # Reaction to expense (1–5)
    re_value = q.get("reaction_to_expense", "Analyze")
    # Map reaction to 1-5 scale
    reaction_map = {
        "panic": 1,
        "ignore": 2,
        "analyze": 4,
        "adjust": 5
    }
    re = reaction_map.get(re_value.lower(), 3)
    score += (re - 3) * 4

    # Peer comparison (emotional stability indicator)
    peer = q.get("compare_with_peers", "").lower()
    if peer == "never":
        score += 4
    elif peer == "sometimes" or peer == "occasionally":
        score += 1
    elif peer == "often" or peer == "frequently":
        score -= 4

    # Additional confidence factors
    spending_decision = q.get("spending_decision", "").lower()
    if spending_decision == "planned":
        score += 3
    elif spending_decision == "impulsive":
        score -= 5
    
    advice_preference = q.get("advice_preference", "").lower()
    if advice_preference == "expert":
        score += 2
    
    track_expenses = q.get("track_expenses", "").lower()
    if track_expenses == "yes":
        score += 3

    # Clamp 0–100
    score = max(0, min(100, score))

    return int(score)
