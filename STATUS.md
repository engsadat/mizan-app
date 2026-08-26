# Mizan — current status (2026-08-26)

Update this file at the end of every session. Then `git commit` + `git push`.
Next chat: open `mizan-app` → read `CLAUDE.md` + this file → **one** task.
Do not save status to a Claude memo.

## Live (checked 2026-08-26)

- URL: https://southmizan.pythonanywhere.com — **up**
- Login page: Arabic ميزان / المنطقة الجنوبية, CSRF on, session cookie Secure + HttpOnly + SameSite=Lax
- `/` `/employees/` `/reports/` `/settings/` `/reports/finance` → redirect to `/auth/login` (routes exist)
- Login (admin user, password reset on PA): **succeeded** (2026-08-26)
- Job codes page: Populated with codes and salaries via script (2026-08-26)

## Code

- Canonical: `engsadat/mizan-app` `master` @ `aba2eb8` (2026-08-26, org chart integration complete)
- PythonAnywhere HEAD: `e90d900` (awaiting pull of latest commits)
- GitHub master: `aba2eb8` (org chart landing, routes, PDF export routes, 4 region HTML files generated)
- Local laptop: `C:\Users\engsa\OneDrive\Desktop\AI\HR\mizan` tracking `origin/master` only

## Product (this version)

Three home cards: الموظفون، التقارير، الإعدادات.
Settings = job codes + users. Roles: admin | editor | viewer.
Reports: BI + filter + finance. No SCD, no V2, no second codebase.

## One version — delete leftovers

See `CLAUDE.md` §1. Dead: `hr_webapp` folders, `nwc-mizan-webapp`, Claude-Projects Mizan PRs/branches. Close PR #2 without merging.

## Latest work (2026-08-26, session 3 — org chart integration)

- Added Playwright to requirements.txt for PDF export capability
- Created gen_org_charts.py script to generate 4 region org chart HTML files from database
  - Loads 444 active employees from Employee model
  - Filters by region (عسير, جازان, الباحة, نجران)
  - Generates static HTML with employee listings and KPIs
  - Output: app/static/org_charts/09_OrgChart_*.html (4 files)
- Implemented 3 Flask routes in reports blueprint:
  - `/reports/org-chart` — landing page with region cards
  - `/reports/org-chart/<region>` — region org chart with PDF export button
  - `/reports/org-chart/<region>/pdf` — PDF export via Playwright
- Created 2 templates with toolbar, security measures (safe HTML injection)
- Updated reports index with org chart card
- All code pushed to GitHub: aba2eb8

## Org Chart Feature Complete ✓

Organizational Chart Integration (Tasks 12-14):
- ✅ Task 12: Playwright added to requirements.txt and installed locally
- ✅ Task 13: Local testing — gen_org_charts.py generates 4 region HTML files successfully
- ⏳ Task 14: Deploy to PythonAnywhere (in progress)
  - Code pushed to GitHub: aba2eb8
  - Server pull requires manual intervention (SSH not configured on Windows laptop)
  - Playwright browsers must be installed on server: `python -m playwright install chromium`
  - Web app reload required after code pull

Live accessibility:
- Landing page: `/reports/org-chart` (will redirect to login if not authenticated)
- Region view: `/reports/org-chart/<region>` with PDF export button
- PDF export: `/reports/org-chart/<region>/pdf`

## Next (one task)

After server deployment verification:
1. SSH to server (or use PythonAnywhere bash console)
2. Navigate to `/home/southMizan/mizan-app` and run: `git pull origin master`
3. Install Playwright: `python -m playwright install chromium`
4. Reload web app via PythonAnywhere dashboard
5. Test: https://southmizan.pythonanywhere.com/reports/org-chart
6. Verify PDF export works

Once live verification complete, org chart feature is done.
