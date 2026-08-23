# Flask-Migrate: Manage Schema Changes

## Why Migrations Matter
- **Safe updates:** Change the DB schema without losing employee data
- **Version control:** Track every schema change in git
- **Production ready:** Deploy changes to PythonAnywhere without data loss

## Common Tasks

### 1. Start Local Dev (First Time)
```bash
cd hr_webapp
export FLASK_APP=manage.py
flask db upgrade         # Creates all tables from migrations
python run.py           # Start app at http://localhost:5001
```

### 2. Add a New Column to `Employee`
```bash
# Edit app/models.py, add the column
vi app/models.py

# Generate migration (auto-detects your change)
flask db migrate -m "add phone2 to employees"

# Review the generated file in migrations/versions/
vi migrations/versions/00X_add_phone2_to_employees.py

# Apply it to your local DB
flask db upgrade
```

### 3. Deploy to Live (PythonAnywhere)
```bash
# On local: commit + push
git add -A
git commit -m "feat: add phone2 column to employees"
git push origin feature/mizan-phase1

# On PythonAnywhere console:
cd ~/Claude-Projects && git pull origin feature/mizan-phase1
export FLASK_APP=hr_webapp/manage.py
flask db upgrade        # Applies new migration — data stays intact

# Reload from Web tab
```

### 4. Rollback (Undo Last Migration)
```bash
flask db downgrade      # Goes back one step
```

## Files
- `migrations/versions/` — SQL migration files (auto-generated, check into git)
- `migrations/alembic.ini` — Alembic config (in git, don't edit)
- `manage.py` — Entry point for flask db commands

## Migration Naming
- `001_initial.py` — schema baseline
- `002_add_phone2_to_employees.py` — add a column
- `003_rename_salary_to_unit_price.py` — rename field

## Do's and Don'ts
✅ DO: Commit migration files to git  
✅ DO: Run `flask db upgrade` after pulling  
❌ DON'T: Edit migration files after they're applied to live  
❌ DON'T: Use `db.create_all()` — migrations are the source of truth

## Troubleshooting
**"table already exists"** → You already ran the migration. No action needed.  
**"migration context can't find table"** → Old `db.create_all()` conflict. Delete DB and re-run `flask db upgrade`.
