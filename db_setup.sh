flask db init && 
chmod -R 777 migrations &&
flask db migrate && 
chmod -R 777 migrations &&
flask db upgrade ||
chmod -R 777 migrations &&
flask db migrate &&
chmod -R 777 migrations &&
flask db upgrade ||
chmod -R 777 migrations &&
flask db upgrade
