# Mizan — current status (2026-08-29)

Update this file at the end of every session. Then `git commit` + `git push`.
Next chat: open `mizan-app` → read `CLAUDE.md` + this file → **one** task.
Do not save status to a Claude memo.

## Live (checked 2026-08-29)

- URL: https://southmizan.pythonanywhere.com — **up** (`/auth/login` 200 OK)
- CSRF: session cookie includes `csrf_token`; flags Secure + HttpOnly + SameSite=Lax
- Login test this session: **not checked**
- Last successful login recorded: 2026-08-26 (admin user; do not treat as re-verified)

## Code (checked 2026-08-29)

- Canonical: `engsadat/mizan-app` `master`
- Local laptop = `origin/master` @ `a438eb5`
- PythonAnywhere HEAD: **not checked** this session (last recorded match was `c1285d8` / later reload; do not assume it equals `a438eb5`)
- Working tree on laptop: STATUS.md updated this session only

## Leftovers (checked 2026-08-29)

User deleted both folders. Verified gone earlier today:

- `C:\Users\engsa\OneDrive\Desktop\AI\hr_webapp` — gone
- `C:\Users\engsa\OneDrive\Desktop\AI\nwc-mizan-webapp` — gone

Canonical clone intact: `C:\Users\engsa\OneDrive\Desktop\AI\HR\mizan` → `engsadat/mizan-app`.

If PA stash `pa-before-pull-2026-08-29` still exists, restore Excel only (do not restore HTML/templates, do not commit). Do not `git add` untracked `routes.py.bak` or `app/org_charts/`.

## Product (this version)

Three home cards: الموظفون، التقارير، الإعدادات.
Settings = job codes + users. Roles: admin | editor | viewer.
Reports: BI + filter + finance + org charts + project map + projects dashboard.
No SCD, no V2, no second codebase.

## Latest work (2026-08-29) — Excel → DB design review

Reviewed how Excel files feed SQLite. **No code change.**

Verdict: intended pattern is ETL (Excel staging → DB system of record → reports). Actual pattern is a split brain.

Evidence from local `instance/mizan_dev.db`: all 227 `projects.name` values are numeric (column L `القيمة مع الضريبة2` imported as the name). `/reports/projects-dashboard` reads that table. `/reports/project-map-smart` and `/reports/org-chart-smart` still parse the Excel file with a different (correct) column map.

Finance models + `scripts/load_finance_data.py` exist, but `/reports/finance` reads four `.xlsx` files on every request. Alembic `001_initial.py` does not include `projects` / finance tables; local DB has no `alembic_version`.

## Next (one task)

Fix `scripts/import_projects.py` column map to the real `pro` sheet headers, then wipe-and-reimport `projects`:

- name = M / 12 (`إسم المشروع`)
- x = D / 3, y = E / 4
- region = R / 17
- project_state = X / 23
- value = AD / 29
- RE names = AE–AH / 30–33

Do not change the Excel files. After reimport, `/reports/projects-dashboard` should show Arabic names and MSAR values, not tax figures as names.
