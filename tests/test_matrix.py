from datetime import timedelta
from pathlib import Path

import pytest

from github_activity_graph_populator.modes.matrix import calc_commits

this_file = Path(__file__).resolve()
templates = list(
    (this_file.parent.parent / "src/github_activity_graph_populator/templates").glob(
        "*.py"
    )
)
good_choices = [p.stem for p in templates if p.is_file() and not p.stem.startswith("_")]
bad_choices = [p.stem for p in templates if p.is_file() and p.stem.startswith("_b")]

templates = list((this_file.parent / "assets").glob("*.txt"))
custom_good_choices = [
    str(p.resolve())
    for p in templates
    if p.is_file() and not p.stem.startswith("broken")
]
custom_bad_choices = [
    str(p.resolve()) for p in templates if p.is_file() and p.stem.startswith("broken")
]


def test_choices():
    assert good_choices, "No good choices found"
    assert bad_choices, "No bad choices found"


@pytest.mark.parametrize("matrix", good_choices)
def test_calc_commits_valid_matrices(matrix, from_date, to_date):
    commits, dates = calc_commits(matrix, from_date, to_date)

    assert commits > 0
    assert len(dates) == commits
    assert dates[0].date() >= from_date.date()
    assert dates[-1].date() <= to_date.date()


@pytest.mark.parametrize("matrix", bad_choices)
def test_calc_commits_invalid_matrices(matrix, from_date, to_date):
    with pytest.raises(ValueError):
        calc_commits(matrix, from_date, to_date)


@pytest.mark.parametrize("matrix_path", custom_good_choices)
def test_calc_commits_valid_matrices_custom(matrix_path, from_date, to_date):
    commits, dates = calc_commits("custom", from_date, to_date, matrix_path)

    assert commits > 0
    assert len(dates) == commits
    assert dates[0].date() >= from_date.date()
    assert dates[-1].date() <= to_date.date()


@pytest.mark.parametrize("matrix_path", custom_bad_choices)
def test_calc_commits_invalid_custom_matrices(matrix_path, from_date, to_date):
    with pytest.raises(ValueError):
        calc_commits("custom", from_date, to_date, matrix_path)


def test_calc_commits_range(from_date):
    for i in range(1, 366):
        to_date = from_date + timedelta(days=i)
        commits, dates = calc_commits(good_choices[0], from_date, to_date)

        assert commits > 0
        assert len(dates) == commits
        assert dates[0].date() >= from_date.date()
        assert dates[-1].date() <= to_date.date()
