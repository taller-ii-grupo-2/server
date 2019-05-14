import os
from app import socketio
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    socketio.run(host='0.0.0.0', port=port)
