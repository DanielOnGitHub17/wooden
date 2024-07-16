pip install -r requirements.txt
python3.9 manage.py collectstatic
python3.9 manage.py makemigrations
python3.9 manage.py migrate
# docker run --rm -p 6379:6379 redis:7