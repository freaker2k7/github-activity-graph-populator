from datetime import date, datetime, time, timezone

import pytest


# fixture for from_date and to_date range
@pytest.fixture
def from_date():
    return datetime.combine(
        date.fromisoformat("2013-01-01"), time.min, tzinfo=timezone.utc
    )


@pytest.fixture
def to_date():
    return datetime.combine(
        date.fromisoformat("2013-01-10"), time.min, tzinfo=timezone.utc
    )


@pytest.fixture
def bad_to_date():
    return datetime.combine(
        date.fromisoformat("2012-01-01"), time.min, tzinfo=timezone.utc
    )
