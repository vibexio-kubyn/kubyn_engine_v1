from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta


def build_monthly_projection(monthly_saving: float, months: int) -> list:
    """
    Builds a month-by-month cumulative savings projection.
    No behavior penalty applied here.
    """

    if monthly_saving is None or months <= 0:
        return []

    projection = []
    total = 0.0
    current = datetime.now(timezone.utc).replace(day=1)

    for i in range(1, months + 1):
        total += monthly_saving

        projection.append({
            "month_index": i,
            "period": current.strftime("%Y-%m"),
            "value": round(total, 2)
        })

        current += relativedelta(months=1)

    return projection
