from typing import Dict, Any
# Main calculation

def calculate_income_expense(q: Dict[str, Any]) -> Dict[str, int]:
    monthly_income = _extract_income(q)
    monthly_expense = _extract_expense(q)
    saving_percent = _extract_savings(q)

    # Income score
    if monthly_income >= 100000:
        income_score = 90
    elif monthly_income >= 70000:
        income_score = 75
    elif monthly_income >= 40000:
        income_score = 60
    else:
        income_score = 40

    # Expense score (expense ratio)
    if monthly_income > 0:
        expense_ratio = monthly_expense / monthly_income
    else:
        expense_ratio = 1

    if expense_ratio <= 0.4:
        expense_score = 90
    elif expense_ratio <= 0.6:
        expense_score = 70
    elif expense_ratio <= 0.8:
        expense_score = 50
    else:
        expense_score = 30

    # Savings score
    if saving_percent >= 30:
        savings_score = 90
    elif saving_percent >= 20:
        savings_score = 75
    elif saving_percent >= 10:
        savings_score = 60
    else:
        savings_score = 40

    return {
        "income_score": income_score,
        "expense_score": expense_score,
        "savings_score": savings_score
    }

# Extractoion of each component
def _extract_income(q: Dict[str, Any]) -> int:
    """
    Extract monthly income ONLY from `annual_income_range`.
    Example values:
    - "Under 5L"
    - "5L - 10L"
    """

    value = q.get("annual_income_range", "").lower().replace(" ", "").strip()

    # Mapping annual ranges → estimated monthly income
    income_map = {
    "under5l": 25000,
    "5l-15l": 62500,
    "15l-30l": 125000,
    "30labove": 150000,
}

    if value in income_map:
        return income_map[value]

    # Fallback (safe default)
    return 30000


def _extract_expense(q: Dict[str, Any]) -> int:
    """
    Extract monthly expense from `weekly_spending'.
    """

    weekly = q.get("weekly_spending")

    try:
        weekly_int = int(str(weekly).strip())
        return weekly_int * 4  # Approx monthly
    except:
        # Default: assume 50% of income
        return int(_extract_income(q) * 0.5)


def _extract_savings(q: Dict[str, Any]) -> int:
    """
    Extract savings percentage ONLY from `monthly_saving_percentage.
    """
    value = q.get("monthly_saving_percentage")

    try:
        return int(str(value).strip())
    except:
        return 10  # Safe default
