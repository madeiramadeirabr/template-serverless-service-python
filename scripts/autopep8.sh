#!/bin/bash
if [ -z "$1" ]; then
#  autopep8 --in-place --recursive --aggressive
  autopep8 --global-config .pep8 --in-place --recursive --verbose ./app.py ./boot.py ./flambda_app
else
  autopep8 --global-config .pep8 --in-place --aggressive --verbose $1
fi
