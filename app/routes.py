from app import app
from app.models import Name
from flask import jsonify
@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route("/getall")
def get_all():
    try:
        names=Name.query.all()
        return  jsonify([e.serialize() for e in names])
    except Exception as e:
        return(str(e))

@app.route("/add")
def add_name():
    name=request.args.get('name')
    last_name=request.args.get('last_name')
    return Name.add_name(name,last_name)
