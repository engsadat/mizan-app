import os
from app import create_app

# PythonAnywhere imports this file. Unset FLASK_ENV would otherwise load
# DevelopmentConfig (DEBUG + mizan_dev.db). Set DATABASE_URL and SECRET_KEY
# in /var/www/southmizan_pythonanywhere_com_wsgi.py before this import.
os.environ.setdefault('FLASK_ENV', 'production')
application = create_app()

if __name__ == '__main__':
    application.run()
