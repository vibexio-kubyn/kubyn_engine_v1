from db import fetch_all
import logging

logger = logging.getLogger("engine2-expense")

OVERSPEND_THRESHOLD = 0.35

def analyse_expenses(user_id, days=7):
    """
    Analyse user expenses over the last N days.
    """
    query = """
        SELECT category, SUM(amount) AS total
        FROM expenses
        WHERE user_id = %s
          AND expense_date >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
        GROUP BY category
    """

    try:
        data = fetch_all(query, (user_id, days)) or []
    except Exception:
        logger.exception("Expense DB query failed")
        raise

    total_spent = sum(float(row.get("total", 0)) for row in data) #overall expenses for the past 7 days.

    insights = []
    for row in data:
        amount = float(row.get("total", 0))
        share = (amount / total_spent) if total_spent else 0 #calculating share for each category for llm generation

        insights.append({
            "category": row.get("category", "unknown"),
            "amount": amount,
            "share": round(share, 2),
            "status": "overspend" if share > OVERSPEND_THRESHOLD else "healthy"
        })

    result = {
        "period_days": days,
        "total_spent": round(total_spent, 2),
        "breakdown": insights
    }

    logger.info(
        f"Expense analysis completed | user_id={user_id} | total={total_spent}"
    )

    return result
