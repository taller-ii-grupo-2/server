python app/manage.py db init
chmod -R 777 migrations
python app/manage.py db migrate
python app/manage.py db upgrade
