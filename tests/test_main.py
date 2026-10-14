from datetime import date, datetime, time

from github_activity_graph_populator.main import main


def test_spread_actions_matrix(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        [
            "gagp",
            "--from-date",
            "2013-01-01",
            "--to-date",
            "2013-01-10",
            "--matrix",
            "smile",
        ],
    )
    main()


def test_spread_actions_busy(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        [
            "gagp",
            "--from-date",
            "2013-01-01",
            "--to-date",
            "2013-01-10",
            "--mode",
            "busy",
        ],
    )
    main()
