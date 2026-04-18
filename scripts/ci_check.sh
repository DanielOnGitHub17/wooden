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

# Ensure the settings file uses the expected production email backend.
python3 - <<'PY'
from pathlib import Path
import re

settings_file = Path('wooden/settings.py').read_text()
active_email_backend = None
for line in settings_file.splitlines():
    stripped = line.strip()
    if stripped.startswith('EMAIL_BACKEND') and not stripped.startswith('#'):
        active_email_backend = stripped
        break

if active_email_backend is None:
    raise SystemExit('ERROR: EMAIL_BACKEND is not configured in wooden/settings.py')

if 'register.email_backend.PowerAutomateEmailBackend' not in active_email_backend:
    raise SystemExit(
        'ERROR: EMAIL_BACKEND must be set to "register.email_backend.PowerAutomateEmailBackend" in wooden/settings.py'
    )

if 'console.EmailBackend' in active_email_backend:
    raise SystemExit(
        'ERROR: EMAIL_BACKEND is currently set to a console backend; it must use PowerAutomateEmailBackend for this workflow.'
    )

print('EMAIL_BACKEND is correctly configured.')
PY

echo "CI script completed successfully."
