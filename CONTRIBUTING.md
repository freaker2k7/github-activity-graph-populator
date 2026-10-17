# GitHub Activity Graph Populator - Contributing Guide

First of all, thank you for considering contributing to the GitHub Activity Graph Populator project!

Your contributions help improve the tool and make it more useful for everyone 🙏

## Prerequisites

Before contributing, make sure you have the following installed:

- Python 3.9 or higher
- Git (for version control)

## Clone

To contribute to the project, you need to clone the repository on GitHub and get it on your local machine:

```bash
git clone https://github.com/your-username/github-activity-graph-populator.git
cd github-activity-graph-populator
```

## Virtual Environment

It's recommended to create a virtual environment to manage dependencies for the project.

You can create a virtual environment using the following command:

```bash
python -m venv .venv
```

Activate the virtual environment:

- On Linux/MacOS:
  ```bash
  source .venv/bin/activate
  ```
- On Windows:
  ```bash
  .venv\Scripts\activate
  ```

## Dependencies

You can install the required dependencies using pip:

```bash
python -m pip install --upgrade pip
python -m pip install build twine
python -m pip install -e ".[dev]"
```

## Adding new modes

Currently there're only 2 modes available: `busy` and `matrix`.

The `matrix` mode uses tiles which are located in the `src/github_activity_graph_populator/templates` directory.
Values in a matrix can be 0-4, corresponding to the only 5 available colors in the GitHub activity graph from light to dark.

On the other hand, the `busy` mode does not use tiles and instead focuses on generating a busy pattern in the GitHub activity graph.
It uses the `args.intensity` parameter to determine how busy the pattern should be, this value represents the max average number of commits per day.

Feel free to add new interesting modes to enhance the functionality of the GitHub Activity Graph Populator, just don't forget to update the documentation and add corresponding tests.
Modes are added to the `src/github_activity_graph_populator/modes` directory as separate Python files with each file exposing it's functionality through a namespace function (for simplicity, for now). Then, you need to add the functionality to the `main.py` file to make it available for use in the "switch" (see line 54 in `main.py`).

## Adding new tiles

![Tile Builder](https://i.imgur.com/JmJyeol.jpeg)

Go to the [Tile Builder page](https://freaker2k7.github.io/github-activity-graph-populator/) in your browser to start designing new tiles.

Or, if you prefer, you can open the `tile-builder/` folder and run it locally, optionally you can also improve the builder.
To run the Tile Builder locally:

1. In the `tile-builder` folder, run:

```bash
npm i
npm run dev
```

2. Use the builder interface to design your new tile.
3. Copy the generated code for your new tile under `src/github_activity_graph_populator/templates/<new-matrix-name>.py`.
Please look at other existing tiles in the `src/github_activity_graph_populator/templates/` directory for reference.

## Dry Run

Basically, when `--repo` is not specified, the tool will perform a dry run.

This is helpful sometime for debugging to leave the temporary folder:

```bash
gagp --mode busy --from-date 2013-01-01 --to-date 2013-04-01
```

## Running tests

The tests are located in the `tests` directory and cover various aspects of the GitHub Activity Graph Populator functionality.
When adding new things, make sure to write corresponding tests to ensure the functionality works as expected and the coverage must not drop below the required threshold.

You can run the tests using pytest:

```bash
python -m pytest --cov=github_activity_graph_populator --cov-report=term-missing --cov-fail-under=100
```

*NOTE: The coverage threshold is set to 100%, so the tests will fail if the coverage is below this value.*

## Linting & Formatting

To maintain code quality and consistency, the project uses linting and formatting tools which are checked during the CI.

You can run the linter using:

```bash
python -m ruff check src tests
```

You can run the formatter using:

```bash
python -m black src tests
```

## Commit Messages

Please use clear and descriptive commit messages that explain the purpose of the changes you are making.
Attach relevant issue numbers or related information in the commit message if applicable.
Screenshot are most welcome to illustrate the changes made.

And thank you again for contributing to the project!

## TODO (for now)

- Add more matrix styles for the `matrix` mode.
- Implement additional modes to enhance the GitHub activity graph patterns.

