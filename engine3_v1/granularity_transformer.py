from datetime import datetime, timedelta
from collections import defaultdict

def expand_granularity(monthly_projection):
    day_series = []
    week_series = defaultdict(float)
    month_series = []
    year_series = defaultdict(float)

    for row in monthly_projection:
        value = row["value"]
        month_series.append(row)

        base_date = datetime.strptime(row["period"], "%Y-%m")

        # Year
        year_series[base_date.year] = value

        # Week (approximate – visualization only)
        for w in range(4):
            key = f"{base_date.year}-W{(base_date.month-1)*4 + w + 1}"
            week_series[key] = value

        # Day (smooth interpolation)
        daily_increment = value / 30
        for d in range(30):
            day_series.append({
                "date": (base_date + timedelta(days=d)).strftime("%Y-%m-%d"),
                "value": round(daily_increment * (d + 1), 2)
            })

    return {
        "day": day_series,
        "week": [{"week": k, "value": round(v, 2)} for k, v in week_series.items()],
        "month": month_series,
        "year": [{"year": k, "value": round(v, 2)} for k, v in year_series.items()]
    }
