def calculate_income_expense(question_data):
    # Try to extract income from different possible field names
    monthly_income = _extract_income(question_data)
    monthly_expense = _extract_expense(question_data)
    saving_percent = _extract_savings(question_data)
    
    print(f"DEBUG Income: {monthly_income}, Expense: {monthly_expense}, Savings: {saving_percent}")

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

def _extract_income(q):
    """Extract income from various possible field names"""
    # Try different field names
    field_names = [
        'monthly_income',
        'income',
        'annual_income',
        'annual_income_range',
        'salary',
        'monthly_salary'
    ]
    
    for field in field_names:
        if field in q:
            value = q[field]
            # Convert "5-10L" to monthly (approx 41,667 - 83,333)
            if isinstance(value, str) and 'L' in value:
                try:
                    # Handle "5-10L" format
                    if '-' in value:
                        range_parts = value.split('-')
                        lower = float(range_parts[0].replace('L', '').strip())
                        upper = float(range_parts[1].replace('L', '').strip())
                        avg = (lower + upper) / 2
                        monthly = (avg * 100000) / 12  # Convert Lakhs to monthly
                        return int(monthly)
                    else:
                        # Handle "10L" format
                        num = float(value.replace('L', '').strip())
                        monthly = (num * 100000) / 12
                        return int(monthly)
                except:
                    pass
            return _to_int(value)
    
    # Default income if not found
    return 30000

def _extract_expense(q):
    """Extract expense from various possible field names"""
    field_names = [
        'monthly_expense',
        'expense',
        'monthly_spending',
        'spending'
    ]
    
    for field in field_names:
        if field in q:
            return _to_int(q[field])
    
    # Default to 50% of income if expense not found
    income = _extract_income(q)
    return int(income * 0.5)

def _extract_savings(q):
    """Extract savings percentage"""
    field_names = [
        'monthly_saving_percentage',
        'saving_percentage',
        'savings_rate'
    ]
    
    for field in field_names:
        if field in q:
            return _to_int(q[field])
    
    # Default savings rate
    return 10

def _to_int(value):
    try:
        if isinstance(value, str):
            # Remove commas, currency symbols, etc.
            import re
            numbers = re.findall(r'\d+', value)
            if numbers:
                return int(numbers[0])
        return int(value)
    except (TypeError, ValueError):
        return 0
