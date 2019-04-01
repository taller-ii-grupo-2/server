#if [ ! -d "migrations" ]; then
python /code/src/hypechat/manage.py db init
#fi

python /code/src/hypechat/manage.py db migrate
python /code/src/hypechat/manage.py db upgrade

python /code/src/hypechat/main.py