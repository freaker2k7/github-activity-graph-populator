# GitHub Activity Graph Populator

A tool to populate your GitHub activity graph the way you like — or make it look super busy!

## Installation

```bash
pip install github-activity-graph-populator
```

## Usage

```bash
gagp --help
```

## Examples

```bash
gagp --matrix tree --from 2013-01-01 --to 2013-04-01 --repo your-github-username/your-repo-name
# or make it look super busy
gagp --mode busy --from 2013-01-01 --to 2013-04-01 --repo your-github-username/your-repo-name
```

(Optionally) You can force push the changes if the repository is not clean:

```bash
gagp --mode busy --from 2013-01-01 --to 2013-04-01 --repo your-github-username/your-repo-name --force-push
```

### Dry Run

This is helpful sometime for debugging to leave the temporary folder:

```bash
gagp --mode busy --from 2013-01-01 --to 2013-04-01
```