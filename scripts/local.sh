#python /code/manage.py db init
#chmod  -R 777 /code/migrations
#python /code/manage.py db migrate
#python /code/manage.py db upgrade
#python /code/manage.py db merge

gunicorn --worker-class eventlet --log-level debug --bind 0.0.0.0:5000 app:app
