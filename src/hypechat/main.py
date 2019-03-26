"""
Module with main purpose to test basic setup functionality.
"""
from flask import Flask
# pylint: disable=invalid-name
app = Flask(__name__)
# pylint: enable=invalid-name


@app.route('/android')
def hello_android():
    """Returns msg for android endpoint."""
    return 'Hello, Android!'


@app.route('/web_admin')
def hello_admin():
    """ returns msg for web admin endpoint.  """
    return 'Hello, Admin!'


if __name__ == '__main__':
    app.run()
