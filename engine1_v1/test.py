import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Test with sample data
sample_answers = {
    "stress_spending": "Yes",
    "weekly_spending": "low",
    "spending_decision": "Mix of both",
    "goal_frequency": "3",
    "overspend_category": "Family",
    "short_term_goal": "Yes",
    "track_expenses": "Yes",
    "preferred_investment": "Crypto",
    "employment_status": "Self-employed",
    "long_term_goal": "Yes",
    "saving_motivation": "legacy",
    "monthly_income": "80000",
    "monthly_expense": "40000",
    "monthly_saving_percentage": "25",
    "investment_confidence": "high",
    "budget_discipline": "good",
    "reaction_to_expense": "analyze",
    "compare_with_peers": "never",
    "advice_preference": "expert"
}

from engine1 import process_engine_one

user_data = {"id": "test_user_123"}
result = process_engine_one(user_data, sample_answers)
print("Test Result:")
print(result)
