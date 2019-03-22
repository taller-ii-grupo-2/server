from flask import Flask
app = Flask(__name__)

@app.route('/android')
def hello_android():
    return 'Hello, Android!'

@app.route('/web_admin')
def hello_admin():
    return 'Hello, Admin!'
