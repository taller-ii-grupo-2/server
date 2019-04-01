
alembic stamp 737c7b27b23c
python /code/src/hypechat/manage.py db init
chmod -R 777 migrations
python /code/src/hypechat/manage.py db migrate
python /code/src/hypechat/manage.py db upgrade


python /code/src/hypechat/main.py