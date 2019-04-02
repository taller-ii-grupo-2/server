import os
from __init__ import app
if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=PORT)
