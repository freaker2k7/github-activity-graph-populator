from datetime import timedelta

import pytest

from github_activity_graph_populator.modes.busy import spread_actions


def test_spread_actions(from_date, to_date):
    commits: int = ((to_date - from_date).days) * 10
    dates = spread_actions(from_date, to_date, 10, commits)

    assert commits > 0
    assert len(dates) == commits
    assert dates[0].date() >= from_date.date()
    assert dates[-1].date() <= to_date.date()


def test_spread_actions_with_invalid_range(from_date, bad_to_date):
    commits: int = 10
    with pytest.raises(ValueError) as e:
        spread_actions(from_date, bad_to_date, 10, commits)
    assert str(e.value) == "to_date must be >= from_date"


def test_spread_actions_with_total_actions_exceeding_limit(from_date, to_date):
    commits: int = 2000
    with pytest.raises(ValueError) as e:
        spread_actions(from_date, to_date, 10, commits)
    assert str(e.value) == "Total actions exceed the average daily limit"


def test_spread_actions_with_zero_count(from_date, to_date):
    commits: int = 0
    with pytest.raises(ValueError) as e:
        spread_actions(from_date, to_date, 10, commits)
    assert str(e.value) == "Invalid action limits"


def test_spread_actions_with_zero_max_average_actions_in_a_day(from_date, to_date):
    commits: int = 10
    with pytest.raises(ValueError) as e:
        spread_actions(from_date, to_date, 0, commits)
    assert str(e.value) == "Invalid action limits"


def test_spread_actions_range(from_date):
    for i in range(1, 366):
        to_date = from_date + timedelta(days=i)
        commits: int = ((to_date - from_date).days) * 10
        dates = spread_actions(from_date, to_date, 10, commits)

        assert commits > 0
        assert len(dates) == commits
        assert dates[0].date() >= from_date.date()
        assert dates[-1].date() <= to_date.date()
