from __future__ import annotations

import argparse
import logging
import subprocess
import tempfile
from datetime import date, datetime, time, timezone
from random import choice
from string import ascii_uppercase

from .modes.busy import spread_actions
from .modes.matrix import calc_commits

logging.basicConfig(
    level=logging.INFO, format="[%(levelname)s] %(asctime)s: %(name)s >> %(message)s"
)
logger = logging.getLogger("github-activity-graph-populator")


def run(
    cwd: str,
    command: str,
    stdin_file: str | None = None,
    allowed_status_codes: list[int] | None = None,
):
    logger.debug(f"Running command: `{command}` in {cwd}")

    with open(stdin_file, "r") if stdin_file else open("/dev/null") as input_file:
        result = subprocess.run(
            command,
            capture_output=True,
            cwd=cwd,
            shell=True,
            text=True,
            stdin=input_file,
            check=False,
        )

        if allowed_status_codes is None:
            allowed_status_codes = [0]

        if result.returncode not in allowed_status_codes:
            raise RuntimeError(
                f"Command failed with return code {result.returncode}: {result.stderr}"
            )

        return result.stdout


def main():
    parser = argparse.ArgumentParser(description="Populate GitHub activity graph")
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
        choices=["checkmark", "smile", "tree"],
        help="Matrix style for populating GitHub activity graph",
    )
    parser.add_argument(
        "--max-intensity",
        type=int,
        default=10,
        help="Average number of commits per day [only used for 'busy' mode]",
    )
    args = parser.parse_args()

    blank_file = True
    random_string = "".join(choice(ascii_uppercase) for i in range(4096))
    input_folder_path = tempfile.mkdtemp(prefix="gpop-", dir=args.folder or "/tmp")
    output_folder_path = tempfile.mkdtemp(prefix="gpop-", dir=args.folder or "/tmp")
    tmp_export_file_path = tempfile.mkstemp(prefix="gpop-export-", dir="/tmp")[1]
    tmp_import_file_path = tempfile.mkstemp(prefix="gpop-import-", dir="/tmp")[1]

    from_date = (
        datetime.combine(
            date.fromisoformat(args.from_date), time.min, tzinfo=timezone.utc
        )
        if args.from_date
        else datetime.now(tz=timezone.utc).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
    )
    to_date = (
        datetime.combine(
            date.fromisoformat(args.to_date), time.min, tzinfo=timezone.utc
        )
        if args.to_date
        else datetime.now(tz=timezone.utc).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
    )

    # 2008 is the day GitHub was launched
    from_date = max(from_date, datetime(2008, 1, 1, tzinfo=timezone.utc))

    to_date = max(to_date, from_date)

    if args.mode == "matrix":
        commits, dates = calc_commits(args.matrix, from_date, to_date)
    else:  # busy mode
        commits: int = ((to_date - from_date).days) * args.max_intensity

        dates = spread_actions(
            from_date=from_date,
            to_date=to_date,
            max_average_actions_in_a_day=args.max_intensity,
            total_actions=commits,
        )

    if commits != len(dates):
        raise ValueError(
            "Mismatch between number of commits and verification count",
            commits,
            len(dates),
        )

    logger.info(f"Temporary input folder created at: {input_folder_path}")
    logger.info(f"Temporary output folder created at: {output_folder_path}")
    logger.info(f"Temporary export file created at: {tmp_export_file_path}")
    logger.info(f"Temporary import file created at: {tmp_import_file_path}")

    open(input_folder_path + "/" + args.filename, "w").close()

    run(input_folder_path, "git init")
    run(input_folder_path, f"git add {args.filename}")

    logger.info(f"Repository initialized in {input_folder_path}")

    for i in range(commits):
        with open(input_folder_path + "/" + args.filename, "w") as f:
            if blank_file:
                f.write(random_string)
            else:
                f.write("")
        blank_file = not blank_file

        run(input_folder_path, f"git commit -am 'Fix #{i+1}'")

        print(
            f"INFO:github-activity-graph-populator:Committed Fix #{i+1}\r",
            flush=True,
            end="",
        )

    run(input_folder_path, f"git fast-export --all > {tmp_export_file_path}")

    logger.info(f"Exported git data to: {tmp_export_file_path}")

    with (
        open(tmp_export_file_path, "r") as input,
        open(tmp_import_file_path, "w") as output,
    ):
        timestamp = datetime.now(tz=timezone.utc)
        year = 0
        for line in input:
            if line.startswith(("author ", "committer ")):
                if line.startswith("author "):
                    timestamp = dates.pop(0)
                parts = line.strip().split()
                parts[-2] = str(int(timestamp.timestamp()))
                line = " ".join(parts) + "\n"
            logger.debug(">> %s", line)
            output.write(line)

            if year != timestamp.year:
                year = timestamp.year
                logger.debug("Processing %d", year)

    logger.info("Finished reading exported git data.")

    run(output_folder_path, "git init")
    run(
        output_folder_path,
        "git fast-import --date-format=raw-permissive",
        stdin_file=tmp_import_file_path,
        # allowed_status_codes=[0, 1],
    )

    if args.repo:
        run(
            output_folder_path,
            f"git remote add origin git@github.com:{args.repo}.git",
        )

        if args.force_push:
            run(output_folder_path, "git push -f -u origin master")
        else:
            run(output_folder_path, "git push -u origin master")

    logger.info(f"Repository imported in {output_folder_path} with {commits} commits")


if __name__ == "__main__":
    main()
