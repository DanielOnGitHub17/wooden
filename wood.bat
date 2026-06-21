@echo off
REM Wood - Django Management Command Wrapper for Windows

setlocal enabledelayedexpansion

set "command=%1"

if "!command!"=="" (
    echo No command specified. Available commands:
    echo   /a    Activate virtual environment
    echo   /c    Check Django configuration
    echo   /cd   Check Django configuration for deployment
    echo   /d    Run Redis in Docker
    echo   /m    Run migrations
    echo   /mm   Make migrations
    echo   /R    Run Gunicorn server with reload
    echo   /r    Run Django daphne development server
    echo   /s    Run Django shell
    echo   /st   Collect static files
    echo   /t    Run tests
    echo   /req  Install requirements
    exit /b 1
)

if "!command!"=="/a" (
    call ..\woodenv\Scripts\activate.bat
    exit /b 0
)

if "!command!"=="/c" (
    python manage.py check
    exit /b 0
)

if "!command!"=="/cd" (
    python manage.py check -/deploy
    exit /b 0
)

if "!command!"=="/d" (
    docker run --rm /p 6379:6379 redis:latest
    exit /b 0
)

if "!command!"=="/m" (
    python manage.py migrate
    exit /b 0
)

if "!command!"=="/mm" (
    python manage.py makemigrations
    exit /b 0
)

if "!command!"=="/R" (
    python -m gunicorn --reload --log-level debug wooden.asgi:application -k uvicorn.workers.UvicornWorker
    exit /b 0
)

if "!command!"=="/r" (
    python -m daphne -b 0.0.0.0 -p 5006 wooden.asgi:application
    exit /b 0
)

if "!command!"=="/s" (
    python manage.py shell
    exit /b 0
)

if "!command!"=="/st" (
    python manage.py collectstatic --noinput
    exit /b 0
)

if "!command!"=="/t" (
    python manage.py test
    exit /b 0
)

if "!command!"=="/req" (
    python -m pip install -r requirements.txt --require-virtualenv
    exit /b 0
)

echo Unknown command: !command!
exit /b 1
