from __future__ import annotations

import logging
import subprocess
from pathlib import Path

from .consts import package_name

logger = logging.getLogger(f"{package_name}-runner")


def run(
    cwd: str,
    command: str,
    stdin_file: str | None = None,
    allowed_status_codes: list[int] | None = None,
) -> str:
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


def cleanup(paths: list[str | Path]) -> None:
    _paths = [Path(path) for path in paths]
    for path in _paths:
        if path.exists():
            if path.is_dir():
                for sub_path in path.iterdir():
                    if sub_path.is_file():
                        sub_path.unlink()
                    else:
                        cleanup([sub_path])
                path.rmdir()
            else:
                path.unlink()
