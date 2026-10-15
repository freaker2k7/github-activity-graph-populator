from __future__ import annotations

import importlib
import logging
from datetime import datetime, timedelta

from ..lib.consts import package_name
from ..templates import flatten_matrix

logger = logging.getLogger(f"{package_name}-matrix")


def calc_commits(
    matrix_name,
    from_date: datetime,
    to_date: datetime,
    custom_matrix: str | None = None,
) -> tuple[int, list[datetime]]:
    count = 0
    dates = []

    days = (to_date - from_date).days
    start_day = from_date.isoweekday() % 7

    if matrix_name == "custom" and custom_matrix:
        with open(custom_matrix, "r") as f:
            matrix = f.read()
    else:
        matrix = importlib.import_module(
            f"..templates.{matrix_name.replace('-', '_')}", package=__package__
        ).matrix

    flat_matrix = flatten_matrix(matrix)

    for i in range(days):
        cell_commits = flat_matrix[(start_day + i) % len(flat_matrix)]
        count += cell_commits

        for j in range(cell_commits):
            dates.append(from_date + timedelta(days=i, hours=12, minutes=j))

    return count, dates
