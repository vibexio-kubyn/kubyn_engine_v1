# engine1/income_expense.py

def calculate_income_expense(question_data):
    monthly_income = _to_int(question_data.get("monthly_income", 0))
    monthly_expense = _to_int(question_data.get("monthly_expense", 0))
    saving_percent = _to_int(question_data.get("monthly_saving_percentage", 0))

    # Income score
    if monthly_income >= 100000:
        income_score = 90
    elif monthly_income >= 70000:
        income_score = 75
    elif monthly_income >= 40000:
        income_score = 60
    else:
        income_score = 40

    # Expense score
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


def _to_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0
