#!/bin/bash

# cleaning bash script

source .venv/bin/activate
black src/
isort src/
pip freeze >requirements.txt

# Append Python version requirement (if not already present)
# if ! grep -q "^python>=" requirements.txt; then
#     echo "python>=3.13.1" >>requirements.txt
# fi
