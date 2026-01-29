# expense_analysis.py
#expense table relation
from db import fetch_all

def analyse_expenses(user_id, days=7):
    query = """
        SELECT category, SUM(amount) AS total
        FROM expenses
        WHERE user_id = %s
          AND expense_date >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
        GROUP BY category
    """
    data = fetch_all(query, (user_id, days))

    total_spent = sum(row["total"] for row in data)

    insights = []
    for row in data:
        share = (row["total"] / total_spent) if total_spent else 0
        status = "overspend" if share > 0.35 else "healthy"
        insights.append({
            "category": row["category"],
            "amount": float(row["total"]),
            "share": round(share, 2),
            "status": status
        })

    return {
        "period_days": days,
        "total_spent": float(total_spent),
        "breakdown": insights
    }
