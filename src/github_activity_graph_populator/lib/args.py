import argparse
from pathlib import Path

this_file = Path(__file__).resolve()
choices = [
    p.stem
    for p in (this_file.parent.parent / "templates").glob("*.py")
    if p.is_file() and not p.stem.startswith("_")
]
choices.append("custom")


def get_args():
    parser = argparse.ArgumentParser(
        description="Populate GitHub activity graph",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--repo",
        default=None,
        type=str,
        help="Name of the repository to populate in the format of <github_username>/<repository_name>",
    )
    parser.add_argument(
        "--force-push",
        action="store_true",
        help="Force push to the remote repository",
    )
    parser.add_argument(
        "--filename",
        type=str,
        default="README.md",
        help="Name of the file to create and commit",
    )
    parser.add_argument(
        "--folder", type=str, default=None, help="Folder to create temporary files in"
    )
    parser.add_argument(
        "--from-date",
        type=str,
        default=None,
        help="Start date for populating GitHub activity graph",
    )
    parser.add_argument(
        "--to-date",
        type=str,
        default=None,
        help="End date for populating GitHub activity graph",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="matrix",
        choices=["matrix", "busy"],
        help="Mode for populating GitHub activity graph",
    )
    parser.add_argument(
        "--matrix",
        type=str,
        default="tree",
        choices=choices,
        help="Matrix style for populating GitHub activity graph",
    )
    parser.add_argument(
        "--custom-matrix",
        type=str,
        default=None,
        help="Path to custom tile style for populating GitHub activity graph. There must be 7 rows and at least 1 column in the matrix and it should be a plain text file. The values in the matrix represent the color 0-4 from white to dark green",
    )
    parser.add_argument(
        "--max-intensity",
        type=int,
        default=10,
        help="Average number of commits per day [only used for 'busy' mode]",
    )
    parser.add_argument(
        "--agent",
        nargs="?",
        const=".",
        default=None,
        metavar="PATH",
        help="Install SKILL.md into PATH when this argument is specified (default: current directory)",
    )
    parser.add_argument(
        "--cleanup",
        action="store_true",
        help="Run cleanup after populating GitHub activity graph",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run in test mode",
    )

    return parser.parse_args()
