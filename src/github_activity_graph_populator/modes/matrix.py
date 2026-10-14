import importlib
import logging
from datetime import datetime, timedelta

from ..matrix import flatten_matrix

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("github-activity-graph-populator-matrix")


def calc_commits(
    matrix_name, from_date: datetime, to_date: datetime
) -> tuple[int, list[datetime]]:
    count = 0
    dates = []

    days = (to_date - from_date).days
    start_day = from_date.isoweekday() % 7
    matrix = importlib.import_module(
        f"..matrix.{matrix_name.replace('-', '_')}", package=__package__
    ).matrix
    flat_matrix = flatten_matrix(matrix)

    for i in range(days):
        cell_commits = flat_matrix[(start_day + i) % len(flat_matrix)]
        count += cell_commits

        for j in range(cell_commits):
            dates.append(from_date + timedelta(days=i, hours=12, minutes=j))

    return count, dates
