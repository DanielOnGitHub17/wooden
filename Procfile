web: python -m gunicorn wooden.asgi:application -k uvicorn.workers.UvicornWorker
# Uncomment this `release` process if you are using a database, so that Django's model
# migrations are run as part of app deployment, using Heroku's Release Phase feature:
# https://docs.djangoproject.com/en/5.1/topics/migrations/
# https://devcenter.heroku.com/articles/release-phase
release: python manage.py collectstatic --noinput && python manage.py makemigrations && python manage.py migrate
