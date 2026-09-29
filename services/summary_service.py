def get_summary(db):
    docs = db.collection("data").stream()

    values = []
    dates = []

    for doc in docs:
        data = doc.to_dict()

        if "value" in data:
            values.append(float(data["value"]))

        if "date" in data:
            dates.append(data["date"])

    if not values:
        return {
            "period": "데이터 없음",
            "count": 0,
            "metrics": {
                "average": 0,
                "max": 0,
                "min": 0
            },
            "trend": "데이터 없음"
        }

    average = round(sum(values) / len(values), 2)
    maximum = max(values)
    minimum = min(values)

    trend = "상승" if values[-1] >= values[0] else "하락"

    return {
        "period": f"{min(dates)} ~ {max(dates)}",
        "count": len(values),
        "metrics": {
            "average": average,
            "max": maximum,
            "min": minimum
        },
        "trend": trend
    }