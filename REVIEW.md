# Mizan web app — external review

Reviewed: `mizan-phase1/hr_webapp` (this folder).
Live host: `southmizan.pythonanywhere.com`.
Also used PythonAnywhere error logs under `.worktrees/screenshoots/`.

**Do not implement yet.** Confirm or reject each finding with a file + line. If you disagree, say why from the code. Then give a fix order.

Reply as:
- `CONFIRMED` / `REJECTED` / `PARTIAL` per item
- then a short "what I would fix first" list

---

## Verdict (reviewer)

Solid first product: login, employee CRUD, status history, Excel import, three Arabic reports. Not yet safe as an internet-facing HR system.

---

## P0

### 1. Viewers can change employee status
`POST /employees/<id>/status` has `@login_required` but no role check. Add/edit already block `viewer`. The "تغيير الحالة" button is visible to all roles on the profile page.

### 2. No CSRF
Flask-WTF is not in `requirements.txt`. Login / add / edit / status / job-code POSTs have no CSRF token. `WTF_CSRF_ENABLED = False` exists only on `TestingConfig`.

---

## P1

### 3. Secrets committed
`.env.production` is in the repo with `SECRET_KEY=change-this-to-a-long-random-string`. `.gitignore` does not ignore `.env*`.

### 4. Production bootstrap
`create_app()` never calls `db.create_all()`. Tables are created only by `scripts/setup_admin.py` and `scripts/import_excel.py`. PythonAnywhere logs: `IndentationError` in `/var/www/southmizan_pythonanywhere_com_wsgi.py`, then login crash `no such table: users`.

### 5. Wrong production DB path
`ProductionConfig` defaults `DATABASE_URL` to `sqlite:////opt/mizan/instance/mizan.db` (droplet). The live app is PythonAnywhere SQLite.

### 6. Cookie / remember-me
`login_user(..., remember=True)` with no `SESSION_COOKIE_SECURE` / HttpOnly / SameSite settings.

---

## P2

### 7. `is_replacement` only set on import
Set in `scripts/import_excel.py` when status == `بديل`. Changing status later does not update the flag or the list badge.

### 8. KPI label mismatch
Dashboard label is `المستحق الشهري الكامل` but the number is `SUM(unit_price)`. Profile calls the same field `الراتب اليومي`.

### 9. UX holes
- Side panel always shows `تعديل` — viewers hit 403.
- Region chips drop the search query (`q`).
- No `base.html` — nav / fonts / Bootstrap are copy-pasted on every page.

---

## P3

### 10. Flask-Migrate unused
In `requirements.txt` but there is no `migrations/` folder and it is never initialized.

### 11. Test gaps
No viewer-403 test, no reports tests, no CSRF test. Import test walks several parents to find the Excel file.

---

## What already works (for context)

- Blueprints: auth, main, employees, settings, reports
- Roles: `admin` / `editor` / `viewer`. Settings are admin-only. Add/edit block viewers
- Passwords hashed. Employee list: search, region chips, status filter, HTMX side panel
- Excel import maps existing HR columns, dedupes names, writes status history
- Reports reuse NWC job-category rules; Chart.js data via `json.dumps`
- Tests cover login, list filters, add/edit, status history, job codes, export columns
