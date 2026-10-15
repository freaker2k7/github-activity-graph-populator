import subprocess
import sys
from pathlib import Path

from github_activity_graph_populator.main import main, run


def test_spread_actions_matrix(monkeypatch, from_date, to_date):
    monkeypatch.setattr(
        "sys.argv",
        [
            "gagp",
            "--from-date",
            str(from_date.date()),
            "--to-date",
            str(to_date.date()),
            "--matrix",
            "smile",
            "--test",
        ],
    )
    main()


def test_spread_actions_busy(monkeypatch, from_date, to_date):
    monkeypatch.setattr(
        "sys.argv",
        [
            "gagp",
            "--from-date",
            str(from_date.date()),
            "--to-date",
            str(to_date.date()),
            "--mode",
            "busy",
            "--test",
        ],
    )

    main()


def test_spread_actions_busy_with_mocked_run(monkeypatch, from_date, to_date):
    monkeypatch.setattr(
        "sys.argv",
        [
            "gagp",
            "--from-date",
            str(from_date.date()),
            "--to-date",
            str(to_date.date()),
            "--mode",
            "busy",
            "--repo",
            "test/test",
            "--test",
        ],
    )

    def conditional_wrapper(*args, **kwargs):
        if args and args[1].startswith(("git remote", "git push")):
            return "Mocked Value!"

        return run(*args, **kwargs)

    monkeypatch.setattr("github_activity_graph_populator.main.run", conditional_wrapper)

    main()


def test_spread_actions_busy_with_mocked_run_force_push(
    monkeypatch, from_date, to_date
):
    monkeypatch.setattr(
        "sys.argv",
        [
            "gagp",
            "--from-date",
            str(from_date.date()),
            "--to-date",
            str(to_date.date()),
            "--mode",
            "busy",
            "--repo",
            "test/test",
            "--force-push",
            "--test",
        ],
    )

    def conditional_wrapper(*args, **kwargs):
        if args and args[1].startswith(("git remote", "git push")):
            return "Mocked Value!"

        return run(*args, **kwargs)

    monkeypatch.setattr("github_activity_graph_populator.main.run", conditional_wrapper)

    main()


def test_main_runs_as_script():
    script_path = (
        Path(__file__).parents[1]
        / "src"
        / "github_activity_graph_populator"
        / "main.py"
    )

    result = subprocess.run(
        [sys.executable, str(script_path), "--test"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "Repository imported" in result.stdout or "Repository imported" in result.stderr
