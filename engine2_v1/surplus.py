#(PURE SIMULATION)
from db import fetch_all
import logging

logger = logging.getLogger("engine2-surplus")


def simulate_surplus(user_id):
    """
    PURE surplus simulation.
    Reads data, calculates surplus, suggests allocations.
    Does NOT update database.
    """

    # ---------- Fetch TOTAL income ----------
    income_rows = fetch_all("""
        SELECT COALESCE(SUM(amount), 0) AS total_income
        FROM incomes
        WHERE user_id = %s
    """, (user_id,))

    total_income = float(income_rows[0]["total_income"]) if income_rows else 0.0

    # ---------- Fetch TOTAL expense ----------
    expense_rows = fetch_all("""
        SELECT COALESCE(SUM(amount), 0) AS total_expense
        FROM expenses
        WHERE user_id = %s
    """, (user_id,))

    total_expense = float(expense_rows[0]["total_expense"]) if expense_rows else 0.0

    surplus = total_income - total_expense

    if surplus <= 0:
        return {
            "surplus": 0.0,
            "suggested_allocations": [],
            "remaining_unallocated": 0.0
        }

    # ---------- Fetch goals ----------
    goals = fetch_all("""
        SELECT goal_id as id, target_amount, current_saved
        FROM goals
        WHERE user_id = %s
        ORDER BY id
    """, (user_id,))

    remaining = surplus
    suggestions = []

    for goal in goals:
        if remaining <= 0:
            break

        needed = float(goal["target_amount"]) - float(goal["current_saved"])
        if needed <= 0:
            continue

        allocate = min(needed, remaining)
        remaining -= allocate

        suggestions.append({
            "goal_id": goal["id"],
            "suggested_amount": round(allocate, 2)
        })

    logger.info(
        f"Surplus simulated | user_id={user_id} | surplus={surplus}"
    )

    return {
        "surplus": round(surplus, 2),
        "suggested_allocations": suggestions,
        "remaining_unallocated": round(remaining, 2)
    }
