from datetime import datetime, timedelta, timezone
from collections import defaultdict


def expand_granularity(monthly_projection: list) -> dict:
    if not monthly_projection:
        return {"day": [], "week": [], "month": [], "year": []}

    day_series = []
    week_series = defaultdict(float)
    month_series = []
    year_series = {}

    previous_value = 0.0

    for row in monthly_projection:
        current_value = row["value"]
        increment = current_value - previous_value
        previous_value = current_value

        month_series.append({
            "period": row["period"],
            "value": round(current_value, 2)
        })

        base_date = datetime.strptime(
            row["period"], "%Y-%m"
        ).replace(tzinfo=timezone.utc)

        # ---- YEAR (cumulative end-of-year value) ----
        year_series[base_date.year] = current_value

        # ---- WEEK (approx, spread increment) ----
        weekly_increment = increment / 4
        for w in range(4):
            week_key = f"{base_date.year}-W{(base_date.month - 1) * 4 + w + 1}"
            week_series[week_key] += weekly_increment

        # ---- DAY (smooth cumulative) ----
        daily_increment = increment / 30
        for d in range(30):
            day_series.append({
                "date": (base_date + timedelta(days=d)).strftime("%Y-%m-%d"),
                "value": round(
                    (previous_value - increment) + daily_increment * (d + 1),
                    2
                )
            })

    return {
        "day": day_series,
        "week": [
            {"week": k, "value": round(v, 2)}
            for k, v in sorted(week_series.items())
        ],
        "month": month_series,
        "year": [
            {"year": k, "value": round(v, 2)}
            for k, v in sorted(year_series.items())
        ]
    }
