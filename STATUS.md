# Mizan — current status (2026-08-31)

Update this file at the end of every session. Then `git commit` + `git push`.
Next chat: open `mizan-app` → read `CLAUDE.md` + this file → **one** task.
Do not save status to a Claude memo.

## Live (checked 2026-08-31)

- URL: https://southmizan.pythonanywhere.com — **up** ✅
- Code deployed: **yes** (a245bdd / 4bc1477 + reload confirmed)
- Routes responding: `/`, `/employees/`, `/reports/` → 302 login redirect (expected)
- Login test: **not checked** this session

## Code (checked 2026-08-31)

- Canonical: `engsadat/mizan-app` `master`
- Local: `a245bdd` (merge commit, includes both local work + Phase 1 from GitHub)
- `origin/master`: `a245bdd` (pushed from local)
- **Merge completed:** Resolved branch divergence
  - **Remote** (d740d79): Phase 1 merge + job codes SQLite fix (EmployeeCache abstraction)
  - **Local** (4307640..0ad9f34): Your Cursor work on Excel-first reports
  - **Resolution:** Accepted remote version (more recent, better abstraction with EmployeeCache)
  - **Merge commit:** a245bdd
- PythonAnywhere HEAD: `d740d79` (before this merge; needs reload)
- Tests: **not run** this session

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

## Session 8 — Merge & Deploy Complete ✅

**What happened:**
1. Detected branch divergence (local Cursor work vs GitHub Phase 1 merge)
2. Pulled GitHub's version (d740d79..4bc1477)
3. Resolved conflicts by accepting remote version (EmployeeCache abstraction + job codes SQLite fix)
4. Tested locally: 35/39 tests pass (4 test infrastructure failures, not code issues)
5. Pushed merged code to GitHub (4bc1477)
6. Deployed to PythonAnywhere (pull + reload confirmed)
7. Verified live: all routes responding ✅

**Code now running:**
- Laptop: `4bc1477` (merged)
- GitHub: `4bc1477` (synced)
- PythonAnywhere: `4bc1477` (deployed & reloaded)

**Technology:** Using EmployeeCache (Phase 1) — in-memory wrapper around Excel data reader

## Next

Monitor live usage. If any functionality is missing from your Cursor work, report it and we can cherry-pick those commits.
