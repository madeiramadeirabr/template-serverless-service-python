#!/bin/bash
# **************************
# Tests Component Coverage Script
# Version: 1.0.0
# **************************
if [ -z "$1" ]; then
  python3 -m coverage run -m unittest discover -s ./tests/component -t ./
else
  python3 -m coverage run -m unittest discover -s ./tests/component -t $1
fi
python3 -m coverage report
python3 -m coverage xml -o ./target/component/report.xml
python3 -m coverage html --omit="*/test*,venv/*,vendor/*" -d ./target/component/coverage_html/
python3 -m clover.coverage2clover -i ./target/component/report.xml -o ./target/component/clover.xml
echo 'results generated in ./target/component/coverage_html/'
