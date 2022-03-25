#!/bin/bash
if [ -z "$1" ]; then
  pylint --rcfile .pylint --verbose ./app.py ./boot.py
  if test -d ./lambda_app; then
    pylint --rcfile .pylint --verbose ./lambda_app
  fi
  if test -d ./flambda_app; then
    pylint --rcfile .pylint --verbose ./flambda_app
  fi
  if test -d ./chalicelib; then
    pylint --rcfile .pylint --verbose ./chalicelib
  fi

else
  pylint --rcfile .pylint --verbose $1
fi
