import time
from flask import Flask, request, jsonify
from init import app
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
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
