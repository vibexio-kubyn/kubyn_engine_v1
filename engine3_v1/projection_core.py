from datetime import datetime

def build_monthly_projection(monthly_saving, months):
    """
    Builds a month-by-month cumulative savings projection.
    No behavior penalty applied here.
    """

    projection = []
    total = 0.0
    current = datetime.utcnow().replace(day=1)

    for i in range(1, months + 1):
        total += monthly_saving

        projection.append({
            "month_index": i,
            "period": current.strftime("%Y-%m"),
            "value": round(total, 2)
        })

        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1)
        else:
            current = current.replace(month=current.month + 1)

    return projection
