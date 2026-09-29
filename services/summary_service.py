def get_summary(db):
    docs = db.collection("data").stream()

    data_list = [doc.to_dict() for doc in docs]

    if not data_list:
        return {
            "period": None,
            "count": 0,
            "metrics": {
                "average": None,
                "max": None,
                "min": None
            },
            "trend": "데이터 없음"
        }

    values = [float(item["value"]) for item in data_list]
    dates = sorted(item["date"] for item in data_list)

    average = sum(values) / len(values)
    maximum = max(values)
    minimum = min(values)

    sorted_data = sorted(
        data_list,
        key=lambda x: x["date"]
    )

    if len(sorted_data) >= 14:
        recent_values = [
            float(item["value"])
            for item in sorted_data[-7:]
        ]

        previous_values = [
            float(item["value"])
            for item in sorted_data[-14:-7]
        ]

        recent_average = (
            sum(recent_values) / len(recent_values)
        )

        previous_average = (
            sum(previous_values) / len(previous_values)
        )

        difference = recent_average - previous_average

        if difference > 0.5:
            trend = "상승"
        elif difference < -0.5:
            trend = "하락"
        else:
            trend = "유지"
    else:
        trend = "데이터 부족"

    return {
        "period": f"{dates[0]} ~ {dates[-1]}",
        "count": len(data_list),
        "metrics": {
            "average": round(average, 2),
            "max": maximum,
            "min": minimum
        },
        "trend": trend
    }