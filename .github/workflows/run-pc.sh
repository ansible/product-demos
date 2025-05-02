#!/bin/bash -x

PYTHON_VARIANT="${USE_PYTHON:-python3.11}"

# intsall pre-commit
eval "${PYTHON_VARIANT} -m pip install pre-commit"

# view pip packages
eval "${PYTHON_VARIANT} -m pip freeze --local"

# fix permissions on directory
git config --global --add safe.directory $(pwd)

# run pre-commit
pre-commit run --show-diff-on-failure --color=always
