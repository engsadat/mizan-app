# Mizan — current status (2026-08-30)

Update this file at the end of every session. Then `git commit` + `git push`.
Next chat: open `mizan-app` → read `CLAUDE.md` + this file → **one** task.
Do not save status to a Claude memo.

## Live (checked 2026-08-30)

- URL: https://southmizan.pythonanywhere.com — **not checked** this session (Excel-first code is local; **not deployed**)
- CSRF: not checked this session
- Login test this session: **not checked** on live
- Local Flask: `http://127.0.0.1:5001` (`run.py`, no reloader). Local login works (admin user in `instance/mizan_dev.db` — do not record passwords)

## Code (checked 2026-08-30)

- Canonical: `engsadat/mizan-app` `master`
- `origin/master` before merge: `2af06e4` (8 Phase-1 ticket commits landed on GitHub while this laptop was working)
- Merged those tickets with this session’s Excel-first + org-smart fixes (`excel_data.py` remains the live employee/project reader)
- PythonAnywhere HEAD: **not checked**
- Local tests this session: `pytest tests -q` → re-run after merge before treating as green

## Leftovers (checked 2026-08-30)

- Do not run `scripts/test_org_charts.py` against live org HTML — it overwrote professional print charts with sample data (2 fake employees). Print files were restored from git.
- Several Flask processes on `:5001` caused the UI to keep showing SQLite (4 employees) after Excel-first. `run.py` now starts with `debug=False, use_reloader=False`. One server only.
- Local SQLite `users` was empty until an admin was created with `scripts/setup_admin.py`. SQLite employees table still has a stale 4-row import; the app no longer reads it.
- `data/Organize/Office-RE.xlsx` may show a tiny local binary diff from Excel; not part of this commit.

## Product (this version)

Three home cards: الموظفون، التقارير، الإعدادات.
Settings = job codes + users. Roles: admin | editor | viewer.
**This phase: Excel is the system of record for business data.** SQLite = login / users only. Team still edits shareable `.xlsx` files. SQL conversion is later.

Employee add / edit / status in the app is **403**. Edit the Excel file, then refresh. Download: `/employees/export.xlsx`.

## Latest work (2026-08-30) — Excel-first + org charts

Business reads no longer use SQLite employees/projects.

- New `app/excel_data.py`: employees + projects + Office-RE (correct `pro` columns: name M/12, region R/17, state X/23, value AD/29)
- Home, employees, HR charts/KPI/filter, projects dashboard → Excel
- `/reports/` card for لوحة المشاريع
- Projects dashboard from real Excel: included **181 / 7579.5 MSAR**; تحت التنفيذ **132 / 5847.7 MSAR** (not 0.0)
- Home on-strength: **444**
- Print org charts restored from git (professional layout, not the sample stub)
- Smart org chart: office titles, job/project search, دعم فني cards, RE name matching (spaces / ي vs ى), contractor KPI, all projects with status
- `pytest.ini` `testpaths = tests`

Do **not** wipe-and-reimport SQLite. Do **not** treat `scripts/import_projects.py` as the live read path.

## Next (one task)

Wire print org charts to Excel for real: `scripts/gen_org_charts_excel.py` is now on master from the Phase 1 tickets — run it (or generate on request) so `/reports/org-chart/<region>` matches the live smart chart, then delete/ignore `scripts/test_org_charts.py`.

Do not deploy to PythonAnywhere until the user asks after reviewing locally.
