pip install -r requirements.txt
python3.9 manage.py collectstatic
python3.9 manage.py makemigrations
python3.9 manage.py migrate
python3.9 -m daphne wooden.asgi:app # Imagine if this works :)
