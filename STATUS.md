# Mizan — current status (2026-08-31)

Update this file at the end of every session. Then `git commit` + `git push`.
Next chat: open `mizan-app` → read `CLAUDE.md` + this file → **one** task.
Do not save status to a Claude memo.

## Live (checked 2026-08-31)

- URL: https://southmizan.pythonanywhere.com — **up** (`/auth/login` shown earlier this calendar day)
- CSRF: not checked this session
- Login test this session: **not checked**
- PythonAnywhere HEAD: **not read** (no SSH). Live static Asir was still the Ticket 4 grid when fetched earlier today. It does **not** yet have A+B.

## Code (checked 2026-08-31)

- Canonical: `engsadat/mizan-app` `master`
- Laptop: A+B print org charts (this session)
- `origin/master` before this STATUS write: `70540f8` (Tel-only restore)
- Print org charts (do **not** regenerate with scripts):
  - **A (default):** `09–12_OrgChart_*.html` — professional A3, no employee-phone dump
  - **B (Tel):** `09–12_OrgChart_*_Tel.html` — same layout with phones (`مع الاتصال`)
- Routes: `/reports/org-chart` = A, `/reports/org-chart-tel` = B. Reports page shows both icons together.
- Local check this session: Flask test client (login disabled) → `/reports/`, `/reports/org-chart`, `/reports/org-chart-tel`, Asir A and Asir B all HTTP 200
- Do **not** run `scripts/gen_org_charts_excel.py` or `scripts/test_org_charts.py`

## Leftovers (checked 2026-08-30)

- Do not run `scripts/test_org_charts.py` against live org HTML — it overwrote professional print charts with sample data (2 fake employees).
- Several Flask processes on `:5001` caused the UI to keep showing SQLite (4 employees) after Excel-first. `run.py` now starts with `debug=False, use_reloader=False`. One server only.
- Local SQLite `users` was empty until an admin was created with `scripts/setup_admin.py`. SQLite employees table still has a stale 4-row import; the app no longer reads it.
- `data/Organize/Office-RE.xlsx` may show a tiny local binary diff from Excel; leave it uncommitted unless the user asks.

## Product (this version)

Three home cards: الموظفون، التقارير، الإعدادات.
Settings = job codes + users. Roles: admin | editor | viewer.
**This phase: Excel is the system of record for business data.** SQLite = login / users only. Team still edits shareable `.xlsx` files. SQL conversion is later.

Employee add / edit / status in the app is **403**. Edit the Excel file, then refresh. Download: `/employees/export.xlsx`.

## Next (one task)

Deploy GitHub `master` (A default + B Tel org charts) to PythonAnywhere. This laptop cannot SSH. User (or a PA Bash console) run:

```
cd /home/southMizan/mizan-app
git fetch origin
git pull origin master
git log -1 --oneline
git status -sb
```

Then Web tab → Reload `southmizan.pythonanywhere.com`.

Done when `/reports/` shows two org-chart icons (A 📋 and B 📞), and `/static/org_charts/09_OrgChart_Asir.html` title is `الهيكل التنظيمي — عسير` (not `المنطقة الجنوبية - NWC` and not Tel).
