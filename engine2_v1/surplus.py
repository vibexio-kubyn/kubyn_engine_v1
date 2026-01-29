# surplus_simulation.py

from db import fetch_all, execute

def simulate_surplus(user_id, expense_total):
    surplus = 0 - expense_total
    if surplus <= 0:
        return {"surplus": 0, "allocations": []}

    goals = fetch_all("""
        SELECT id, target_amount, saved_amount
        FROM goals
        WHERE user_id = %s
    """, (user_id,))

    allocations = []
    remaining = surplus

    for goal in goals:
        needed = goal["target_amount"] - goal["saved_amount"]
        if needed <= 0 or remaining <= 0:
            continue

        allocation = min(needed, remaining)
        remaining -= allocation

        execute("""
            INSERT INTO goal_contributions (goal_id, user_id, amount)
            VALUES (%s, %s, %s)
        """, (goal["id"], user_id, allocation))

        allocations.append({
            "goal_id": goal["id"],
            "allocated": float(allocation)
        })

    return {
        "surplus": float(surplus),
        "allocations": allocations,
        "remaining_unallocated": float(remaining)
    }
