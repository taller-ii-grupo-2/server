python /code/src/hypechat/manage.py db init && 
chmod -R 777 migrations &&
python /code/src/hypechat/manage.py db migrate && 
chmod -R 777 migrations &&
python /code/src/hypechat/manage.py db upgrade ||
chmod -R 777 migrations &&
python /code/src/hypechat/manage.py db migrate &&
chmod -R 777 migrations &&
python /code/src/hypechat/manage.py db upgrade ||
chmod -R 777 migrations &&
python /code/src/hypechat/manage.py db upgrade

python /code/src/hypechat/main.py