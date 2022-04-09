#!/bin/bash
# **************************
# Tests Component Tests Runner Script
# Version: 1.0.0
# **************************
if [ -z "$1" ]; then
  python3 -m unittest discover -s ./tests/component -t ./
else
  python3 -m unittest discover -s ./tests/component -t $1
fi