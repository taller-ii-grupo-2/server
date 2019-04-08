"""File containing all endpoints in the app."""
from flask import request, jsonify
from app import app
from app.models import User  # pylint: disable = syntax-error


@app.route('/')
@app.route('/index')
def index():
    """home endpoint"""
    return "Hello, World!"


@app.route('/android')
def android():
    """home endpoint"""
    return "Hello, android"


@app.route("/getall")
def get_all():
    """get all data in database"""
    try:
        users = User.query.all()
        return jsonify([e.serialize() for e in users])
    except Exception as exception:  # pylint: disable = broad-except
        return str(exception)


@app.route("/add")
def add_user():
    """add object to db"""
    name = request.args.get('name')
    last_name = request.args.get('last_name')
    age = request.args.get('age')
    mail = request.args.get('mail')
    pais = request.args.get('pais')
    token = request.args.get('token')
    height = request.args.get('height')
    return User.add_user(name, last_name, age, mail, pais, token, height)
