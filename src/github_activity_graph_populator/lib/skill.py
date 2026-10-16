from pathlib import Path

skill = """# GitHub Activity Graph Populator — Agent Skill

## Purpose

Use `gagp` to populate a GitHub activity graph with synthetic commit history.

## Requirements

- Python and Git installed.
- A target GitHub repository.
- Appropriate Git authentication and push access.
- Terminal or command-line interface for running the tool.

Install the package:

```bash
pip install github-activity-graph-populator
```

Run `gagp --help` to verify the available options.

## Workflow

1. Identify the target repository (`USERNAME/REPOSITORY`) and the desired date range.
2. Prefer `busy` mode for straightforward activity generation. If the user requests a visual pattern, use `matrix` mode and remember the selected pattern throughout the task.
3. Use `--from-date` and `--to-date` to specify the activity period.
4. Select a supported pattern when using matrix mode: `tree`, `checkmark`, `wave`, `smile`, `flower`, or `custom`.
5. For `custom`, provide `--custom-matrix PATH` pointing to a valid matrix file.
6. Always include `--force-push`.
7. Execute the command and report the outcome accurately.

## CLI Options

- `--repo USERNAME/REPOSITORY`: Target repository.
- `--from-date YYYY-MM-DD`: Start date.
- `--to-date YYYY-MM-DD`: End date.
- `--mode matrix|busy`: Generation mode.
- `--matrix tree|checkmark|wave|smile|flower|custom`: Pattern for matrix mode.
- `--custom-matrix PATH`: Custom matrix file; must contain exactly 7 rows, at least 1 column, and values from `0` to `4`.
- `--max-intensity N`: Average commits per day in busy mode; defaults to `10`.
- `--force-push`: Force-push changes to the remote repository when required.

## Examples

### Busy mode

```bash
gagp \\
  --repo USERNAME/REPOSITORY \\
  --from-date 2025-01-01 \\
  --to-date 2025-03-31 \\
  --mode busy \\
  --max-intensity 10 \\
  --force-push
```

### Matrix mode

```bash
gagp \\
  --repo USERNAME/REPOSITORY \\
  --from-date 2025-01-01 \\
  --to-date 2025-03-31 \\
  --mode matrix \\
  --matrix wave \\
  --force-push
```

## Safety and Constraints

- Always include `--force-push`.
- Confirm the target repository and date range before execution.
- Explain that the tool generates synthetic commit history.
- Never invent unsupported CLI options.
- Report errors and unsuccessful executions accurately.
"""


def set_skill(str_path: str) -> None:
    path = Path(str_path)
    path.mkdir(parents=True, exist_ok=True)

    with open(path / "SKILL.md", "w") as f:
        f.write(skill)
