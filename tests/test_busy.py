from datetime import date, datetime, time

from github_activity_graph_populator.modes.busy import spread_actions


def test_spread_actions():
    from_date = datetime.combine(date.fromisoformat("2013-01-01"), time.min)
    to_date = datetime.combine(date.fromisoformat("2013-04-01"), time.min)

    commits: int = ((to_date - from_date).days) * 10
    dates = spread_actions(from_date, to_date, 10, commits)

    assert commits > 0
    assert len(dates) == commits
    assert dates[0].date() == from_date.date()
    assert dates[-1].date() <= to_date.date()

def test_spread_actions_with_invalid_range():
    from_date = datetime.combine(date.fromisoformat("2013-01-01"), time.min)
    to_date = datetime.combine(date.fromisoformat("2012-01-01"), time.min)

    commits: int = 10
    try:
        spread_actions(from_date, to_date, 10, commits)
    except ValueError as e:
        assert str(e) == "to_date must be >= from_date"
    else:
        assert False, "Expected ValueError was not raised"

def test_spread_actions_with_total_actions_exceeding_limit():
    from_date = datetime.combine(date.fromisoformat("2013-01-01"), time.min)
    to_date = datetime.combine(date.fromisoformat("2013-01-10"), time.min)

    commits: int = 200
    try:
        spread_actions(from_date, to_date, 10, commits)
    except ValueError as e:
        assert str(e) == "Total actions exceed the average daily limit"
    else:
        assert False, "Expected ValueError was not raised"

def test_spread_actions_with_zero_count():
    from_date = datetime.combine(date.fromisoformat("2013-01-01"), time.min)
    to_date = datetime.combine(date.fromisoformat("2013-01-10"), time.min)

    commits: int = 0
    try:
        spread_actions(from_date, to_date, 10, commits)
    except ValueError as e:
        assert str(e) == "Invalid action limits"
    else:
        assert False, "Expected ValueError was not raised"

def test_spread_actions_with_zero_max_average_actions_in_a_day():
    from_date = datetime.combine(date.fromisoformat("2013-01-01"), time.min)
    to_date = datetime.combine(date.fromisoformat("2013-01-10"), time.min)

    commits: int = 10
    try:
        spread_actions(from_date, to_date, 0, commits)
    except ValueError as e:
        assert str(e) == "Invalid action limits"
    else:
        assert False, "Expected ValueError was not raised"
