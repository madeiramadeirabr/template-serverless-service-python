#!/bin/bash
# **************************
# Tests Unit Tests Runner Script
# Version: 1.0.0
# **************************
if [ -z "$1" ]; then
  python3 -m unittest discover -s ./tests/unit -t ./
else
  python3 -m unittest discover -s ./tests/unit -t $1
fi
