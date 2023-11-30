from datetime import timedelta, datetime, date


def get_nearest_day() -> date:
    return (datetime.now() + timedelta(hours=5)).date()
