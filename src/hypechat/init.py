from flask import Flask
import flask_sqlalchemy
import config

DATABASE_CONNECTION_URI = \
    'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user= os.environ['POSTGRES_USER'],
        passwd=os.environ['POSTGRES_PASSWORD'],
        host='db',
        port='5432',
        db=os.environ['POSTGRES_DB'])


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
