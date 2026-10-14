import logging
import math
import random
from datetime import datetime, timedelta, timezone

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("github-activity-graph-populator-busy")


def spread_actions(
    from_date: datetime,
    to_date: datetime,
    max_average_actions_in_a_day: int,
    total_actions: int,
) -> list[datetime]:
    if to_date < from_date:
        raise ValueError("to_date must be >= from_date")
    if max_average_actions_in_a_day < 1 or total_actions < 1:
        raise ValueError("Invalid action limits")

    # Build the inclusive calendar-day range.
    first_day = from_date.date()
    last_day = to_date.date()
    days = (last_day - first_day).days

    # Choose 3%-5% zero-action days, if possible.
    min_zero = (days * 3 + 99) // 100
    max_zero = (days * 5) // 100

    min_zero = min(min_zero, max_zero)

    zero_days_count = random.randint(min_zero, max_zero)
    active_days_count = days - zero_days_count

    # The average across the entire period must not exceed the limit.
    if total_actions > days * max_average_actions_in_a_day:
        raise ValueError("Total actions exceed the average daily limit")

    max_actions_per_active_day = math.ceil(total_actions / active_days_count)

    if total_actions > days * max_average_actions_in_a_day:
        raise ValueError("Total actions exceed the average daily limit")

    all_days = [first_day + timedelta(days=i) for i in range(days)]
    zero_days = set(random.sample(all_days, zero_days_count))
    active_days = [day for day in all_days if day not in zero_days]
    random.shuffle(active_days)

    # Randomly assign actions to active days.
    daily_counts = {day: 0 for day in all_days}
    remaining = total_actions

    for i, day in enumerate(active_days):
        days_left = len(active_days) - i - 1
        min_today = max(
            0,
            remaining - days_left * max_actions_per_active_day,
        )
        max_today = min(max_actions_per_active_day, remaining)

        count = random.randint(min_today, max_today)
        daily_counts[day] = count
        remaining -= count

    # Generate a random datetime for each action within the given bounds.
    result = []

    for day, count in daily_counts.items():
        day_start = datetime.combine(day, datetime.min.time(), tzinfo=timezone.utc)
        day_end = day_start + timedelta(days=1)

        start = max(from_date, day_start)
        end = min(to_date, day_end)

        if count and start >= end:
            raise ValueError(f"No valid time range for an active day: {day} [{start} - {end}]")

        for _ in range(count):
            offset = random.random() * (end - start).total_seconds()
            result.append(start + timedelta(seconds=offset))

    return sorted(result)
