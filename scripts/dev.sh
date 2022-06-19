#!/bin/bash
if test -f "requirements-dev.txt"; then
  python3 -m pip install -r requirements-dev.txt
fi

