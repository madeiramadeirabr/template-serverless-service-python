#!/bin/bash
# **************************
# Tests Unit Coverage No Report HTML Script
# Version: 1.0.0
# **************************
if [ -z "$1" ]; then
  python3 -m coverage run -m unittest discover -s ./tests/unit -t ./
else
  python3 -m coverage run -m unittest discover -s ./tests/unit -t $1
fi
python3 -m coverage report
python3 -m coverage xml
python3 -m clover.coverage2clover -i ./target/unit/report.xml -o ./target/unit/clover.xml