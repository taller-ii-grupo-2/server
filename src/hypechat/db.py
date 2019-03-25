import os
from flask_sqlalchemy import SQLAlchemy

DATABASE_CONNECTION_URI = \
    'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user= os.environ['POSTGRES_USER'],
        passwd=os.environ['POSTGRES_PASSWORD'],
        host='db',
        port='5432',
        db=os.environ['POSTGRES_DB'])

db = SQLAlchemy()
