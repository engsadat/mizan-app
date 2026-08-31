# Mizan — current status (2026-08-31)

Update this file at the end of every session. Then `git commit` + `git push`.
Next chat: open `mizan-app` → read `CLAUDE.md` + this file → **one** task.
Do not save status to a Claude memo.

## Live (checked 2026-08-31)

- URL: https://southmizan.pythonanywhere.com — **up** (`/auth/login` shown)
- CSRF: not checked this session
- Login test this session: **not checked**
- Laptop SSH `southMizan@ssh.pythonanywhere.com`: **Permission denied** (publickey,password). Could not pull or reload from here.
- Live static Asir (`/static/org_charts/09_OrgChart_Asir.html`): Tel title `الهيكل التنظيمي — عسير (مع الاتصال)` — this is the Tel-only restore, not A+B.
- Live `/static/org_charts/09_OrgChart_Asir_Tel.html`: **404**. A+B (`de7db9a`) is not on the server yet.
- PythonAnywhere HEAD: **not read** (no SSH). Believed to be Tel-only (`70540f8` era), not `de7db9a`.

## Code (checked 2026-08-31)

- Canonical: `engsadat/mizan-app` `master`
- Laptop = GitHub: `de7db9a` (`Offer both print org charts: A default without phones, B Tel with phones.`)
- Print org charts on GitHub:
  - **A (default):** `/reports/org-chart` → `09–12_OrgChart_*.html`
  - **B (Tel):** `/reports/org-chart-tel` → `09–12_OrgChart_*_Tel.html`
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

This laptop cannot SSH. In the PythonAnywhere **Bash console** run:

```
cd /home/southMizan/mizan-app
git fetch origin
git pull origin master
git log -1 --oneline
git status -sb
```

That log must show `de7db9a`. Then Web tab → Reload `southmizan.pythonanywhere.com`.

Done when `/reports/` shows icons A 📋 and B 📞, Asir A title is `الهيكل التنظيمي — عسير`, and `/static/org_charts/09_OrgChart_Asir_Tel.html` is no longer 404.
