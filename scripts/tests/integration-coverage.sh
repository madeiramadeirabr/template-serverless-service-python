#!/bin/bash
# **************************
# Tests Integration Coverage Script
# Version: 1.0.0
# **************************
if [ -z "$1" ]; then
  python3 -m coverage run -m unittest discover -s ./tests/integration -t ./
else
  python3 -m coverage run -m unittest discover -s ./tests/integration -t $1
fi
python3 -m coverage report
python3 -m coverage xml -o ./target/integration/report.xml
python3 -m coverage html --omit="*/test*,venv/*,vendor/*" -d ./target/integration/coverage_html/
python3 -m clover.coverage2clover -i ./target/integration/report.xml -o ./target/integration/clover.xml
echo 'results generated in ./target/integration/coverage_html/'
