python /code/src/hypechat/manage.py db init
chmod -R 777 migrations
python /code/src/hypechat/manage.py db migrate
python /code/src/hypechat/manage.py db upgrade
