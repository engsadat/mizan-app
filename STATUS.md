# Mizan — current status (2026-08-31)

Update this file at the end of every session. Then `git commit` + `git push`.
Next chat: open `mizan-app` → read `CLAUDE.md` + this file → **one** task.
Do not save status to a Claude memo.

## Live (checked 2026-08-31)

- URL: https://southmizan.pythonanywhere.com — **up** (`/auth/login` HTTP 200)
- CSRF: not checked this session
- Login test this session: **not checked**
- Code on the server: **behind GitHub**. Laptop SSH to `southMizan@ssh.pythonanywhere.com` → Permission denied. No API token on this laptop.
- Live Asir static chart still has the old title `المنطقة الجنوبية - NWC`. GitHub already has the current print files.

## Code (checked 2026-08-31)

- Canonical: `engsadat/mizan-app` `master`
- Laptop working tree: **clean**, tracking `origin/master`
- `origin/master` before this STATUS write: `714071b` (`Record origin SHA 5b85570 after pushing Tel org charts.`)
- App code already on GitHub (do **not** redo this work):
  - `5b85570` — print org charts with employee phones (مع الاتصال)
  - `4bc1477` / `a245bdd` — Phase 1 merge on GitHub
- PythonAnywhere HEAD: **not read** this session. Last recorded SHA on the server: `d740d79`
- Local tests this session: `pytest tests -q` → **36 passed, 4 failed, 3 skipped**
  - 4 failures in `tests/test_employees.py`: tests seed SQLite names; the app list/panel reads Excel. From the Phase 1 merge. Not a deploy blocker.
- Do **not** run `scripts/gen_org_charts_excel.py` or `scripts/test_org_charts.py` — they overwrite the print HTML already on GitHub.

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

## Latest work (2026-08-31) — GitHub is current; live is not

Cursor session: pulled GitHub, committed remaining local print-chart files, pushed `master`.

The org-chart rewrite is **done and on GitHub**. Do not treat it as the next task. Do not regenerate those HTML files this session.

Do **not** wipe-and-reimport SQLite. Do **not** treat `scripts/import_projects.py` as the live read path.

## Next (one task)

Deploy GitHub `master` to PythonAnywhere. This laptop cannot SSH. User (or you in a PA Bash console) run:

```
cd /home/southMizan/mizan-app
git fetch origin
git pull origin master
git log -1 --oneline
git status -sb
```

Then Web tab → Reload `southmizan.pythonanywhere.com`.

Done when `git log -1` on the server matches GitHub `master`, and a logged-in `/reports/org-chart` load is the GitHub print files (not the old `المنطقة الجنوبية - NWC` stub).
