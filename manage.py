#!/usr/bin/env python
"""Flask-Migrate helper for Mizan — initialize and run database migrations."""
import os
from app import create_app, db
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

# Use: flask --app manage.py db init/migrate/upgrade
# Or set FLASK_APP=manage.py and run: flask db init/migrate/upgrade
