# Mizan Phase 1 — Deployment Guide

**Version:** 1.0.0  
**Date:** 2026-08-30  
**Status:** ✅ Production Ready (Read-Only)  
**Data Source:** Excel files (not database)

---

## Quick Start

### Local Development
```bash
cd mizan-app
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
# App runs on http://localhost:5001
```

### Login Credentials (Development)
```
Username: admin
Password: testpass123
```

---

## Architecture

### Phase 1 Design (Current)
- **Read-only from Excel** — All employee/project data flows from Excel files
- **Database schema exists** — For Phase 2 write operations (currently unused)
- **Flask blueprints** — Organized by feature: auth / employees / reports / settings / main
- **Role-based access** — admin / editor / viewer with route-level guards
- **RTL Arabic** — Cairo font, NWC branding, proper text direction

### Data Flow
```
Excel Files (data/source/*.xlsx)
    ↓
EmployeeCache (utils/employee_cache.py)
    ↓
Flask Routes (app/blueprints/*/routes.py)
    ↓
Jinja2 Templates
    ↓
User Browser
```

---

## Deployment Configuration

### Environment Variables
Set these for production:

```bash
# Flask
export FLASK_ENV=production
export SECRET_KEY=<generate-a-random-key-here>

# Excel Sources (if different paths)
export EXCEL_EMPLOYEES=/path/to/employees.xlsx
export EXCEL_PROJECTS=/path/to/projects.xlsx

# Database (Phase 2 only)
export DATABASE_URL=sqlite:///instance/mizan.db
```

### Generate Secure SECRET_KEY
```python
import secrets
print(secrets.token_hex(32))
```

### Production Config Checklist
- [ ] Set `SECRET_KEY` (random, 64+ characters)
- [ ] Set `FLASK_ENV=production`
- [ ] Set `SESSION_COOKIE_SECURE=True` (HTTPS only)
- [ ] Set `SESSION_COOKIE_HTTPONLY=True` (default: on)
- [ ] Enable CSRF protection (default: on)
- [ ] Verify Excel file paths exist
- [ ] Use production WSGI server (Gunicorn, uWSGI, etc.)
- [ ] Enable HTTPS/SSL certificate

---

## Data Files

### Required Excel Files
All files must exist in `data/` directory (or override via environment variables):

| File | Path | Purpose |
|------|------|---------|
| Employees Master | `data/source/employees data source.xlsx` | 444 active employees |
| Projects Master | `data/source/project_2026_database_ver1_updated.xlsx` | 181 projects |
| Invoices | `data/Invoices/Jun_Inv.xlsx` | Invoice records |
| PO Master | `data/po_master.xlsx` | Purchase orders 1-5 |
| PO6 Detail | `data/po6_detail.xlsx` | Variation order jobs |
| Variations | `data/variations.xlsx` | Budget variations |
| Contacts | `data/source/contacts.xlsx` | Contact directory |
| Org Staffing | `data/Organize/Office-RE.xlsx` | RE staffing reference |

### Data as of
```
Timestamp: 2026-08-30 13:35:24 UTC
Employees: 444 active (status='على قوة العمل')
Projects: 181 total (132 ongoing)
```

**Note:** These files are loaded on-demand via `EmployeeCache` and `load_projects()`. Changes to Excel files are reflected on next app reload (no cache refresh needed).

---

## Routes & Access Control

### Public (No Auth Required)
- `GET /auth/login` — Login form
- `POST /auth/login` — Submit credentials

### Authenticated (All Roles)
- `GET /` — Dashboard
- `GET /employees/` — Employee list + search + export
- `GET /employees/<id>` — Employee profile
- `GET /employees/<id>/panel` — Side panel (AJAX)
- `GET /reports/` — Reports index
- `GET /reports/org-chart` — Org charts (4 regions)
- `GET /reports/project-map-smart` — Leaflet map
- `GET /reports/projects-dashboard` — KPI dashboard
- `GET /reports/finance` — Finance reports

### Admin Only
- `GET /settings/` — Settings home
- `GET /settings/job-codes` — Job codes (5 hardcoded codes)
- `GET /settings/users` — User management

### Phase 2 Routes (Currently Disabled)
These routes exist but are labeled **"PHASE 2"** and should remain read-only in Phase 1:
```
POST /employees/add
POST /employees/<id>/edit
POST /employees/<id>/status
POST /settings/job-codes/add
POST /settings/job-codes/<id>/edit
POST /settings/users/add
POST /settings/users/<id>/edit
POST /settings/users/<id>/delete
```

---

## Deployment to Azure / PythonAnywhere

### Option 1: PythonAnywhere (Free Tier)
1. Create account at pythonanywhere.com
2. Clone repo or upload files
3. Create virtual environment
4. Configure Web app:
   ```
   Source code: /home/username/mizan-app
   WSGI file: /home/username/mizan-app/run.py
   Virtual env: /home/username/mizan-app/venv
   ```
5. Set environment variables in Web tab → Environments
6. Reload web app

### Option 2: Azure App Service
1. Create App Service (Python 3.9+)
2. Connect git repo
3. Create `web.config` for IIS:
   ```xml
   <?xml version="1.0" encoding="utf-8"?>
   <configuration>
       <system.webServer>
           <handlers>
               <add name="PythonHandler" path="*" verb="*" modules="FastCgiModule" 
                    scriptProcessor="D:\home\python\VirtualEnvs\default\Scripts\python.exe|D:\home\python\VirtualEnvs\default\Lib\site-packages\wfastcgi.py" 
                    resourceType="Unspecified" requireAccess="Script" />
           </handlers>
       </system.webServer>
   </configuration>
   ```
4. Set Application settings (environment variables)
5. Deploy

### Option 3: Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt gunicorn
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

```bash
docker build -t mizan:1.0 .
docker run -p 5000:5000 -e SECRET_KEY=<key> mizan:1.0
```

---

## Monitoring & Maintenance

### Health Check
```bash
curl http://localhost:5001/
# Should return 302 redirect to /auth/login if not logged in
```

### Logs
- Flask development: Console output
- Production: Check WSGI server logs (Gunicorn, etc.)

### Performance
- Employee cache is loaded once on app startup
- Subsequent requests use in-memory cache (no Excel re-reads)
- For large datasets (1000+ employees), consider pagination (already implemented, 50 per page)

### Updating Data
1. Update Excel files locally
2. Replace files on server
3. Restart Flask app (cache reloads automatically)

No database migrations needed — Phase 1 is entirely Excel-backed.

---

## Troubleshooting

### "No such table: employee" Error
**Expected in Phase 1.** This error means:
- ✅ Database schema exists
- ⚠️ No data has been loaded (correct for Phase 1)
- Data is loaded from Excel, not database

**Fix:** Do nothing — this is expected behavior.

### Excel File Not Found
**Error:** `FileNotFoundError: [Errno 2] No such file or directory: 'data/source/employees data source.xlsx'`

**Fix:** 
1. Verify file exists in correct path
2. Or set environment variable:
   ```bash
   export EXCEL_EMPLOYEES=/correct/path/employees.xlsx
   ```
3. Restart app

### Login Not Working
**Check:**
1. Database initialized: `instance/mizan_dev.db` exists
2. Admin user exists: `python -c "from app import create_app, db; from app.models import User; app = create_app(); print(User.query.count())"`
3. If no users, run: `python scripts/setup_admin.py --username admin --password newpass`

### Permission Denied (403)
**Expected behavior:**
- Viewer cannot access `/settings/` (shows 403)
- Editor cannot add/edit employees in Phase 1
- Only admin can view settings

This is correct per Phase 1 audit.

---

## Testing Checklist

### Browser Testing (All Roles)
- [ ] **Viewer Role**
  - [ ] Can login
  - [ ] Can view employees list + search
  - [ ] Can view all reports
  - [ ] Cannot access `/settings/` (403)
  - [ ] Cannot click add/edit buttons

- [ ] **Editor Role**
  - [ ] Can login
  - [ ] Can view employees
  - [ ] Phase 2 routes are labeled (view source code)
  - [ ] Cannot access settings

- [ ] **Admin Role**
  - [ ] Can login
  - [ ] Can view settings
  - [ ] Can see 5 job codes
  - [ ] Can see user management (read-only in Phase 1)

### Data Verification
- [ ] Employees list shows correct regions: نجران, الباحة, جازان, عسير
- [ ] Project count: 132 ongoing (5.8B SAR)
- [ ] Footer shows: "البيانات من: 2026-08-30 13:35:24"
- [ ] Footer shows: "Phase 1: Read-only"

### Performance
- [ ] Employee search returns results in <500ms
- [ ] Reports load in <2s
- [ ] No N+1 queries in database logs

---

## Support & Next Steps

### Phase 2 (Future)
When ready to enable write operations:
1. Remove Phase 2 labels from routes
2. Implement `scripts/import_employees.py` (load Excel → Database)
3. Enable audit trails for changes
4. Add email notifications for status changes

### Contact
- **Project:** Mizan HR Web App (NWC Southern Region)
- **Date:** 2026-08-30
- **Version:** Phase 1.0
- **Status:** ✅ Production Ready
