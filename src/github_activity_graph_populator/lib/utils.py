from __future__ import annotations

import logging
import subprocess

from .consts import package_name

logger = logging.getLogger(f"{package_name}-runner")


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
