"""File containing all endpoints in the app."""
from flask import request, jsonify
from app import app
from app.models import Name  # pylint: disable = syntax-error


@app.route('/')
@app.route('/index')
def index():
    """home endpoint"""
    return "Hello, World!"


@app.route("/getall")
def get_all():
    """get all data in database"""
    try:
        names = Name.query.all()
        return jsonify([e.serialize() for e in names])
    except Exception as exception:  # pylint: disable = broad-except
        return str(exception)


@app.route("/add")
def add_name():
    """ add a Name object to db."""
    name = request.args.get('name')
    last_name = request.args.get('last_name')
    return Name.add_name(name, last_name)
