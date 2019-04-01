"""
Main module of the server app.
"""
import os
from flask import request, jsonify
from sqlalchemy import exc
from hypechat.__init__ import app
from hypechat.models import Name


@app.route('/android')
def hello_android():
    """Returns msg for android endpoint."""
    return 'Hello, Android!'


@app.route('/web_admin')
def hello_admin():
    """ returns msg for web admin endpoint.  """
    return 'Hello, Admin!'


@app.route('/')
def hello():
    """base endpoint behaviour."""
    return 'Hello world!'


@app.route("/add")
def add_name():
    """add user to db endpoint."""
    name = request.args.get('name')
    last_name = request.args.get('last_name')
    # pylint: disable = no-value-for-parameter
    return Name.add_name(name, last_name)
    # pylint: enable = no-value-for-parameter


@app.route("/getall")
def get_all():
    """get all users from database endpoint."""
    try:
        names = Name.query.all()
        return jsonify([e.serialize() for e in names])
    except exc.SQLAlchemyError as exception:
        return str(exception)


if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=PORT)
