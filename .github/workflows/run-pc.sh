#!/bin/bash -x

# should no longer need this
#dnf install git-lfs -y

PYTHON_VARIANT="${USE_PYTHON:-python3.11}"
PATH="$PATH:$HOME/.local/bin"

# intsall pip
eval "${PYTHON_VARIANT} -m pip install --user --upgrade pip"

# try to fix 2.4 incompatibility 
eval "${PYTHON_VARIANT} -m pip install --user --upgrade setuptools wheel twine check-wheel-contents"

# intsall pre-commit
eval "${PYTHON_VARIANT} -m pip install --user pre-commit"

# view pip packages
eval "${PYTHON_VARIANT} -m pip freeze --local"

# fix permissions on directory
git config --global --add safe.directory $(pwd)

# run pre-commit
pre-commit run --config $(pwd)/.pre-commit-gh.yml --show-diff-on-failure --color=always 
