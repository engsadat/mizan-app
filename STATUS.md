# Mizan — current status (2026-08-31)

Update this file at the end of every session. Then `git commit` + `git push`.
Next chat: open `mizan-app` → read `CLAUDE.md` + this file → **one** task.
Do not save status to a Claude memo.

## Live (checked 2026-08-31)

- URL: https://southmizan.pythonanywhere.com — **up** (`/auth/login` HTTP 200)
- CSRF: not checked this session
- Login test this session: **not checked**
- Code deployed: **not reloaded from this laptop** (SSH `southMizan@ssh.pythonanywhere.com` → Permission denied)

## Code (checked 2026-08-31)

- Canonical: `engsadat/mizan-app` `master`
- Pulled `origin/master` first (fast-forward `d740d79` → `4bc1477`)
- This session adds Tel print org charts (مع الاتصال) on top of that
- PythonAnywhere HEAD: **not read** this session (no SSH). Last recorded by previous STATUS: `d740d79`
- Local tests this session: `pytest tests -q` → **36 passed, 4 failed, 3 skipped**
  - Reports / Tel print test passed (`test_org_chart_print_is_tel_version`)
  - 4 failures in `tests/test_employees.py` (SQLite-seeded names not on Excel-backed list/panel). Pre-existing after the Phase 1 merge; not introduced by Tel files
- Do **not** run `scripts/gen_org_charts_excel.py` or `scripts/test_org_charts.py` — they overwrite Tel HTML

## Leftovers (checked 2026-08-30)

- Do not run `scripts/test_org_charts.py` against live org HTML — it overwrote professional print charts with sample data (2 fake employees).
- Several Flask processes on `:5001` caused the UI to keep showing SQLite (4 employees) after Excel-first. `run.py` now starts with `debug=False, use_reloader=False`. One server only.
- Local SQLite `users` was empty until an admin was created with `scripts/setup_admin.py`. SQLite employees table still has a stale 4-row import; the app no longer reads it.
- `data/Organize/Office-RE.xlsx` may show a tiny local binary diff from Excel; not part of this commit.

## Product (this version)

Three home cards: الموظفون، التقارير، الإعدادات.
Settings = job codes + users. Roles: admin | editor | viewer.
**This phase: Excel is the system of record for business data.** SQLite = login / users only. Team still edits shareable `.xlsx` files. SQL conversion is later.

Employee add / edit / status in the app is **403**. Edit the Excel file, then refresh. Download: `/employees/export.xlsx`.

## Latest work (2026-08-31) — Tel print org charts ready to pull on PA

`/reports/org-chart/<region>` serves professional A3 Tel charts: name + phone for every team member.

- Generator: `python scripts/gen_org_chart_tel.py`
- Landing / reports index copy says مع الاتصال
- Stash `tel-org-charts-before-pull-2026-08-31` was used only to pull GitHub, then files were restored

Do **not** wipe-and-reimport SQLite. Do **not** treat `scripts/import_projects.py` as the live read path.

## Next (one task)

On PythonAnywhere Bash, pull this commit and reload the web app (this laptop cannot SSH):

```
cd /home/southMizan/mizan-app
git fetch origin
git pull origin master
git log -1 --oneline
git status -sb
```

Then Web tab → Reload `southmizan.pythonanywhere.com`. Confirm print org charts say مع الاتصال.
