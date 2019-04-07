python /code/manage.py db init
python /code/manage.py db migrate
python /code/manage.py db upgrade

gunicorn --bind 0.0.0.0:5000 app:app
