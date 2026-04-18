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

# Ensure the Django settings module uses the expected production email backend.
python3 - <<'PY'
from wooden import settings

if not hasattr(settings, 'EMAIL_BACKEND'):
    raise SystemExit('ERROR: settings.EMAIL_BACKEND is not defined')

if settings.EMAIL_BACKEND != 'register.email_backend.PowerAutomateEmailBackend':
    raise SystemExit(
        'ERROR: settings.EMAIL_BACKEND must be set to "register.email_backend.PowerAutomateEmailBackend"'
    )

print('EMAIL_BACKEND is correctly configured.')
PY

echo "CI script completed successfully."
