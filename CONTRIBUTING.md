# Contributing to Wooden

## How to start
1. Create an issue describing the bug or feature you want to work on.
2. Or choose an existing issue and ask for permission to work on it.
3. Once you have the go-ahead, fork this repository and clone your fork locally.

```bash
# fork the repo on GitHub, then clone your fork
git clone https://github.com/<your-username>/wooden.git
cd wooden
```

4. Create a working branch for your fix.

```bash
git checkout -b fix/<issue-number>-short-description
```

## Local environment setup
### Python
Check your Python version first.

```bash
python3 --version
```

If this repository requires a newer Python version than installed, upgrade Python on your system before proceeding.

### Create a virtual environment
Create a hidden virtual environment named `env` or `venv` so it is ignored by `.gitignore`.

```bash
python3 -m venv env
source env/bin/activate
```

If you prefer `venv`:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies
Install the project requirements after activating the virtual environment.

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Run migrations
Initialize the database schema.

```bash
python manage.py migrate
```

### Confirm the database exists
A SQLite database file should be created locally.

```bash
ls -la db.sqlite3
```

You can also confirm migrations by running:

```bash
python manage.py showmigrations
```

## Environment variables
Create a `.env` file in the repository root.

```bash
touch .env
```

Add at least these values:

```env
DJANGO_SECRET_KEY=your-random-secret-key
REDISCLOUD_URL=redis://<your-redis-host>:<port>
```

If you want to work on reCAPTCHA features, add:

```env
RECAPTCHA_SECRET_KEY=<your-recaptcha-secret>
```

If you want a custom admin URL, add it as an optional setting. The path should not start with a slash and should end with a slash:

```env
DJANGO_ADMIN_URL=my-admin-path/
```

## Local email setup
For local testing, the project defaults to the Django console email backend when `POWER_AUTOMATE_URL` is not set.

That means email-related flows will print to the terminal instead of sending real email.

If you want to explicitly enable local console email backend, verify that `wooden/settings.py` falls back to:

```python
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
```

## Running the server
### Standard Django development server

```bash
python manage.py runserver
```

### Gunicorn (Linux)

```bash
python -m gunicorn --reload --log-level debug wooden.asgi:application -k uvicorn.workers.UvicornWorker
```

## Quick commands using `wood`
There is a helper script at the repository root called `wood`.

- Start the development server:
  ```bash
  ./wood -r
  ```
- Start a Redis container with Docker:
  ```bash
  ./wood -d
  ```
- Run Gunicorn with hot reload:
  ```bash
  ./wood -R
  ```

If you use GitHub Codespaces, Docker is already available there, so these commands should work well.

## Git hooks
Enable the repository's pre-push hook so local pushes run the same checks as the project expects.

```bash
git config core.hooksPath .githooks
chmod +x .githooks/pre-push
```

This hook verifies migrations, runs tests, and validates requirements before a push.

## Testing and verification
After the server is running, open the app in your browser and verify basic flows:
- Homepage
- Sign in / sign up
- Lounge page
- Game creation / join
- Chat and websocket behavior

If anything fails, create an issue describing the problem and the steps you took.

## FAQ
### Q: What should I do if setup fails?
A: Create an issue with the exact commands you ran, the error output, and the operating environment. I will update this document with the answer.

### Q: Which issue should I work on?
A: Either open a new issue or ask to work on an existing issue before making changes.

### Q: Do I need a separate app-specific README?
A: No. Keep the top-level `README.md` as the primary project overview and use code comments and docstrings for implementation details.

### Q: How do I get Redis working?
A: Start Redis locally via Docker and set `REDISCLOUD_URL` to the Redis server URL. The `wood` script can start a local Redis container with `./wood -d`.

## Notes
- Use `env` or `venv` for the local virtual environment so it is hidden by `.gitignore`.
- Keep secret keys private and do not commit `.env`.
- If you need reCAPTCHA support, set `RECAPTCHA_SECRET_KEY` after registering a key with Google Cloud.
- If you want a custom admin path, use `DJANGO_ADMIN_URL`.

