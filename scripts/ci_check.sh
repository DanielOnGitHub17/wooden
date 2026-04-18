#!/bin/sh
set -e

# Create a temporary Python virtual environment for CI.
python3 -m venv .venv_ci
. .venv_ci/bin/activate

# Install dependencies.
pip install --upgrade pip
pip install -r requirements.txt

# Verify migrations are up to date.
python manage.py makemigrations --check

# Run the unit test suite.
python manage.py test

echo "CI script completed successfully."
