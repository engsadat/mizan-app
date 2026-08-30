import os
from app import create_app, db

app = create_app()

if __name__ == '__main__':
    # Reloader left stale workers on :5001 that still served SQLite.
    app.run(host='0.0.0.0', port=5001, debug=False, use_reloader=False)
