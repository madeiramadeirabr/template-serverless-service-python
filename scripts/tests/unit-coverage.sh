#!/bin/bash
# **************************
# Tests Unit Coverage Script
# Version: 1.0.0
# **************************
if [ -z "$1" ]; then
  coverage run -m unittest discover -s ./tests/unit -t ./
else
  coverage run -m unittest discover -s ./tests/unit -t $1
fi
coverage report
coverage xml
coverage html
python3 -m coverage2clover -i ./target/unit/report.xml -o ./target/unit/clover.xml
echo 'results generated in ./target/unit/coverage_html/'
