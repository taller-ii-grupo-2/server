from app import app
from app.models import User
@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route("/add")
def add_name():
    username=request.args.get('username')
    email=request.args.get('email')
    return User.add_username(username,email)

@app.route("/getall")
def get_all():
    try:
        users=User.query.all()
        return  jsonify([e.serialize() for e in users])
    except Exception as e:
        return(str(e))
