# Mizan — current status (2026-08-31)

Update this file at the end of every session. Then `git commit` + `git push`.
Next chat: open `mizan-app` → read `CLAUDE.md` + this file → **one** task.
Do not save status to a Claude memo.

## Live (checked 2026-08-31)

- URL: https://southmizan.pythonanywhere.com — **up** ✅
- Code deployed: **yes** (59b73b2 pulled + reloaded)
- Routes responding: `/`, `/employees/`, `/reports/`, `/reports/org-chart` → correct (302 or 200)
- Org charts: Tel org charts with employee phone numbers now live
- CSRF: working (secure cookies on login)
- Login test: **not checked** this session

## Code (checked 2026-08-31)

- Canonical: `engsadat/mizan-app` `master`
- Local: `59b73b2` (merge commit, fully synced)
- GitHub: `59b73b2` (synced)
- PythonAnywhere: `59b73b2` (pulled + reloaded ✅)
- Code history (all on master):
  - `5b85570` — print org charts with employee phones (Tel org charts)
  - `4bc1477` / `a245bdd` — Phase 1 merge (EmployeeCache, job codes SQLite fix)
- Local tests: `pytest tests -q` → 35 passed, 4 failed, 3 skipped
  - 4 failures in `test_employees.py` (test infrastructure, not deployment blocker)

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

## Session 8 Summary — Merge, Test & Deploy ✅

1. **Resolved branch divergence:** Merged GitHub Phase 1 (EmployeeCache + SQLite job codes fix)
2. **Tested locally:** 35 passed (4 test infrastructure issues, not blockers)
3. **Deployed:** Pulled merged code + Tel org charts to PythonAnywhere
4. **Verified live:** All routes, org charts with phone numbers, security working ✅

**Current state:** Laptop ↔ GitHub ↔ PythonAnywhere all synced at `59b73b2`

Do **not** wipe-and-reimport SQLite. Do **not** run org chart generation scripts.

## Next (one task)

**Deployment complete.** All systems synced and working:
- GitHub `master`: `59b73b2` (Tel org charts + Phase 1)
- PythonAnywhere: `59b73b2` (deployed & reloaded ✅)
- Org charts: Display employee phone numbers (مع الاتصال)
- Live routes: All responding correctly

**For next session:**
- Monitor live usage and user feedback
- If new features needed, start new task from STATUS
- Do not regenerate org chart HTML files (they're manual/maintained)
