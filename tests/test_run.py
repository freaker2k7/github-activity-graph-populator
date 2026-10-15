import pytest

from github_activity_graph_populator.lib.utils import run


def test_bad_run():
    with pytest.raises(RuntimeError):
        run("/tmp", "exit 1")
