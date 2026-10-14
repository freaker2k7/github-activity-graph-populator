from datetime import date, datetime, time

import pytest
from github_activity_graph_populator.modes.matrix import calc_commits


@pytest.mark.parametrize("matrix", ["checkmark", "smile", "tree"])
def test_calc_commits(matrix):
    from_date = datetime.combine(date.fromisoformat("2013-01-01"), time.min)
    to_date = datetime.combine(date.fromisoformat("2013-04-01"), time.min)

    commits, dates = calc_commits(matrix, from_date, to_date)

    assert commits > 0
    assert len(dates) == commits
    assert dates[0].date() == from_date.date()
    assert dates[-1].date() <= to_date.date()
