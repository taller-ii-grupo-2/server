import time
from flask import Flask, request
from init import app
import config
from models import Name

@app.route('/android')
def hello_android():
    return 'Hello, Android!'

@app.route('/web_admin')
def hello_admin():
    return 'Hello, Admin!'

@app.route('/')
def hello():
    return 'Hello world!'


@app.route("/add")
def add_name():
    name=request.args.get('name')
    last_name=request.args.get('last_name')
    return Name.add_name(name,last_name)

@app.route("/getall")
def get_all():
    try:
        names=Name.query.all()
        return  jsonify([e.serialize() for e in names])
    except Exception as e:
        return(str(e))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)