#!/bin/bash

source venv/bin/activate

python -m pytest  --cov=github_activity_graph_populator --cov-report=term-missing --cov-report=html --cov-fail-under=9