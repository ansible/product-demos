#!/bin/bash -x

PYTHON_VARIANT="${USE_PYTHON:-python3.11}"

# intsall pip
eval "${PYTHON_VARIANT} -m pip install --upgrade pip"

# try to fix 2.4 incompatibility 
eval "${PYTHON_VARIANT} -m pip install --upgrade setuptools wheel twine check-wheel-contents"

# intsall pre-commit
eval "${PYTHON_VARIANT} -m pip install pre-commit"

# view pip packages
eval "${PYTHON_VARIANT} -m pip freeze --local"

# fix permissions on directory
git config --global --add safe.directory $(pwd)

# run pre-commit
pre-commit run --show-diff-on-failure --color=always
