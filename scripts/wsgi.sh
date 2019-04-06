python /code/manage.py db init
chmod -R 777 migrations
python /code/manage.py db migrate
python /code/manage.py db upgrade

gunicorn app:app
