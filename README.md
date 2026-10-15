# GitHub Activity Graph Populator

[![GitHub Build](https://github.com/freaker2k7/github-activity-graph-populator/actions/workflows/ci.yml/badge.svg)](https://github.com/freaker2k7/github-activity-graph-populator/actions)

GAGP (GitHub Activity Graph Populator) is a tool to populate your GitHub activity graph the way you like — or make it look super busy!

Zero dependencies, making it more secure and lightweight 🚀

## Demo

You can see a live demo on my own GitHub profile [here](https://github.com/freaker2k7).

![Before](https://i.imgur.com/K5AkkUp.png)
<sub>Before it looked like this...</sub>

![After](https://i.imgur.com/DmmQgaI.png)
<sub>Now, it looked like this! This is the tree pattern and yeah, my design skills definitely need improvement 😅</sub>

*Note: I have a huge number of contributions on my GitHub profile, the images are from the years 2012 and 2013, back then my activity on GitHub was much lower.*

*Another Note: On the way, I discovered I can write history before I was a user which opened the 2012 tab and I cound see the year.*


## TL;DR

Originally, I wanted to represent my Bitbucket activity (where I have over 250 private repositories vs ~50 public ones on GitHub plus a few dozens private ones that apparenly isn't shown on the activity graph for the public) onto my GitHub activity graph, but I didn't want to mess with syncying jobs and dealing with API's when it's just git...
So I decided to just draw a nice pattern on my GitHub activity graph instead, using a nifty git hack I learned over the years; either way, the volume of my commits across GH, BB, AWS and a few other platforms is so high that it doesn't really matter 😜

But I thought it would be fun to create a tool that allows anyone to visually populate their GitHub activity graph with custom patterns 😇

## Installation

```bash
pip install github-activity-graph-populator
```

## Usage

**First** create a public repository on [GitHub](https://github.com/new).

**Then**, after you install the package, you can use the command line.
See the help message for available commands:

```bash
$ gagp --help

usage: main.py [-h] [--repo REPO] [--force-push] [--filename FILENAME] [--folder FOLDER] [--from-date FROM_DATE] [--to-date TO_DATE] [--mode {matrix,busy}] [--matrix {tree,checkmark,wave,smile,flower}]
               [--max-intensity MAX_INTENSITY] [--test]

Populate GitHub activity graph

options:
  -h, --help            show this help message and exit
  --repo REPO           Name of the repository to populate in the format of <github_username>/<repository_name>
  --force-push          Force push to the remote repository
  --filename FILENAME   Name of the file to create and commit
  --folder FOLDER       Folder to create temporary files in
  --from-date FROM_DATE
                        Start date for populating GitHub activity graph
  --to-date TO_DATE     End date for populating GitHub activity graph
  --mode {matrix,busy}  Mode for populating GitHub activity graph
  --matrix {tree,checkmark,wave,smile,flower}
                        Matrix style for populating GitHub activity graph
  --max-intensity MAX_INTENSITY
                        Average number of commits per day [only used for 'busy' mode]
  --test                Run in test mode
```

*Note: The date format for the `--from-date` and `--to-date` options is `YYYY-MM-DD`.*

*Another Note: As GitHub was released in 2008, the minimum `from-date` is 2008-01-01.*

### Examples

```bash
# Colorful tree pattern
gagp --matrix tree --from 2013-01-01 --to 2013-04-01 --repo your-github-username/your-repo-name

# Or make it look super busy
gagp --mode busy --from 2013-01-01 --to 2013-04-01 --repo your-github-username/your-repo-name
```

(Optionally) You can force push the changes if the repository is not clean:

```bash
gagp --mode busy --from 2013-01-01 --to 2013-04-01 --repo your-github-username/your-repo-name --force-push
```

*NOTE: Though I don't recommend it as the re-caching of the GitHub activity graph can take some time. I suggest using a new repo or deleting and recreating the existing one as this is kind of a "dummy" repository that we just need to update its history.*

## Contributing

If you want to contribute to the project, please refer to the [Contributing Guide](CONTRIBUTE.md) for detailed instructions on setting up the development environment, adding new modes or tiles, running tests and maintaining code quality.

## Security

Please see the [Security Policy](SECURITY.md) for information on reporting vulnerabilities and security-related concerns.


## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
