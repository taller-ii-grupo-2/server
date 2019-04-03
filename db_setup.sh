python /code/app/manage.py db init
chmod -R 777 migrations
python /code/app/manage.py db migrate
python /code/app/manage.py db upgrade
