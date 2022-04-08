#!/bin/bash
# **************************
# Tests Integration Coverage Script
# Version: 1.0.0
# **************************
if [ -z "$1" ]; then
  coverage run -m unittest discover -s ./tests/integration -t ./
else
  coverage run -m unittest discover -s ./tests/integration -t $1
fi
coverage report
coverage xml -o ./target/integration/report.xml
coverage html --omit="*/test*,venv/*,vendor/*" -d ./target/integration/coverage_html/
python3 -m coverage2clover -i ./target/integration/report.xml -o ./target/integration/clover.xml
echo 'results generated in ./target/integration/coverage_html/'
