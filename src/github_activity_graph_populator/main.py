import logging
import tempfile
from datetime import date, datetime, time, timezone
from os import linesep

from github_activity_graph_populator.lib.args import get_args
from github_activity_graph_populator.lib.consts import package_name
from github_activity_graph_populator.lib.utils import cleanup, run
from github_activity_graph_populator.modes.busy import spread_actions
from github_activity_graph_populator.modes.matrix import calc_commits

logging.basicConfig(
    level=logging.INFO, format="[%(levelname)s] %(asctime)s: %(name)s >> %(message)s"
)
logger = logging.getLogger(package_name)


def main():
    args = get_args()

    blank_file = True
    input_folder_path = tempfile.mkdtemp(prefix="gagp-", dir=args.folder or "/tmp")
    output_folder_path = tempfile.mkdtemp(prefix="gagp-", dir=args.folder or "/tmp")
    tmp_export_file_path = tempfile.mkstemp(prefix="gagp-export-", dir="/tmp")[1]
    tmp_import_file_path = tempfile.mkstemp(prefix="gagp-import-", dir="/tmp")[1]

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
        commits, dates = calc_commits(
            args.matrix, from_date, to_date, args.custom_matrix
        )
    else:  # busy mode
        commits: int = ((to_date - from_date).days) * args.max_intensity

        dates = spread_actions(
            from_date=from_date,
            to_date=to_date,
            max_average_actions_in_a_day=args.max_intensity,
            total_actions=commits,
        )

    logger.info(f"Temporary input folder created at: {input_folder_path}")
    logger.info(f"Temporary output folder created at: {output_folder_path}")
    logger.info(f"Temporary export file created at: {tmp_export_file_path}")
    logger.info(f"Temporary import file created at: {tmp_import_file_path}")

    open(input_folder_path + "/" + args.filename, "w").close()

    run(input_folder_path, "git init")

    if args.test:
        logger.info("Running in test mode")
        run(input_folder_path, "git config --local user.email 'you@example.com'")
        run(input_folder_path, "git config --local user.name 'Your Name'")

    run(input_folder_path, f"git add {args.filename}")

    logger.info(f"Repository initialized in {input_folder_path}")

    for i in range(commits):
        with open(input_folder_path + "/" + args.filename, "w") as f:
            if blank_file:
                f.write(".")
            else:
                f.write("")
        blank_file = not blank_file

        run(input_folder_path, f"git commit -am 'Fix #{i+1}'")

        print(
            f"[INFO] {datetime.now(tz=timezone.utc).isoformat()}: {package_name} >> Committed Fix #{i+1}\r",
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
                line = " ".join(parts) + linesep
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

    if args.cleanup:
        cleanup(
            [
                input_folder_path,
                output_folder_path,
                tmp_export_file_path,
                tmp_import_file_path,
            ]
        )


if __name__ == "__main__":
    main()
