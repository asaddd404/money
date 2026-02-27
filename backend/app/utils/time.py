from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def period_bounds(period: str, tz_name: str):
    tz = ZoneInfo(tz_name)
    local_now = datetime.now(tz)
    if period == 'day':
        start = local_now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == 'week':
        start = (local_now - timedelta(days=local_now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        start = local_now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return start.astimezone(timezone.utc), local_now.astimezone(timezone.utc)
