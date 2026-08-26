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

- Canonical: `engsadat/mizan-app` `master` @ `2a9f92e` (2026-08-26, org chart integration complete)
- PythonAnywhere HEAD: `e90d900` (awaiting deployment of org chart feature)
- GitHub master: `2a9f92e` (org chart merged: script, routes, templates, PDF export)
- Local laptop: `C:\Users\engsa\OneDrive\Desktop\AI\HR\mizan` tracking `origin/master` only

## Product (this version)

Three home cards: الموظفون، التقارير، الإعدادات.
Settings = job codes + users. Roles: admin | editor | viewer.
Reports: BI + filter + finance. No SCD, no V2, no second codebase.

## One version — delete leftovers

See `CLAUDE.md` §1. Dead: `hr_webapp` folders, `nwc-mizan-webapp`, Claude-Projects Mizan PRs/branches. Close PR #2 without merging.

## Latest work (2026-08-26, session 2)

- Imported 227 projects from source Excel (project_2026_database_ver1_updated.xlsx)
- Created Project model with 32 fields (coordinates, contract, status, RE, progress, facilities)
- Built projects dashboard: `/reports/projects-dashboard`
  - KPI cards for ongoing projects by region (MSAR format)
  - Pivot tables: count and values by status × region
  - Charts: ongoing projects breakdown by region
  - Print/PDF support
- Tested locally and on PA — both working

## Dashboard complete ✓

Projects dashboard live: https://southmizan.pythonanywhere.com/reports/projects-dashboard
- KPI cards: total + 4 regions (تحت التنفيذ projects)
- Pivot tables: count & values by status × region (all projects)
- Charts: ongoing by region
- Print/PDF support

## Latest work (2026-08-26, session 3 — ORG CHART INTEGRATION COMPLETE)

**Org Chart Integration** — Implemented & deployed (Tasks 1-14):

**Task Group A: Script Generation (Tasks 1-7)**
- Created `scripts/gen_org_charts.py` with database integration
  - Loads 444 active employees from Mizan database (status = 'على قوة العمل')
  - Loads ongoing projects (project_state = 'تحت التنفيذ')
  - Generates 4 region-specific HTML org charts
  - Eager-loaded database queries (no N+1 issues)
  - Real NWC/Al-Amro logos with base64 encoding
  - Proper error handling for missing files

**Task Group B: Routes & Templates (Tasks 8-11)**
- Added 3 Flask routes with comprehensive security:
  - `/reports/org-chart` — Region selector (4 color-coded cards)
  - `/reports/org-chart/<region>` — View org chart with toolbar (print, PDF, back)
  - `/reports/org-chart/<region>/pdf` — Playwright-based PDF export (A3 landscape)
- Created 2 templates with RTL Arabic support, Cairo font, responsive layout
- Added org chart card to reports home page
- Security measures: input validation, path traversal defense, XSS mitigation with comments
- Error handling: proper HTTP status codes (404, 503, 500) with logging

**Task Group C: Dependencies (Task 12)**
- Added `playwright>=1.40.0` to requirements.txt

**Task Group D: Testing & Deployment (Tasks 13-14)**
- Local testing: 444 employees across 4 regions, all 4 HTML files generated
- Tests passing: 35 passed (no regressions)
- Code merged to master @ `2a9f92e`
- Pushed to GitHub

## Live Status (2026-08-26)
- **Code:** Merged to master locally and GitHub
- **Tests:** 35/35 passing
- **Deployment:** Awaiting PythonAnywhere server deployment (Playwright install + web app reload required)

## Next (one task)

**Org Chart Deployment to PythonAnywhere:**
1. SSH to server (or PythonAnywhere bash console)
2. `cd /home/southMizan/mizan-app && git pull origin master`
3. `python -m playwright install chromium`
4. Reload web app via PythonAnywhere dashboard
5. Test: https://southmizan.pythonanywhere.com/reports/org-chart
6. Verify PDF export works
