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

- Canonical: `engsadat/mizan-app` `master` @ `e90d900` (2026-08-26, finance print fix + job codes script fix)
- PythonAnywhere HEAD: `be4b590` (not yet pulled latest)
- GitHub master: `e90d900` (finance report print layout + job code rates script fix)
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

## Latest work (2026-08-26, session 3)

**Org Chart Integration** — Implemented Tasks 1-7 of org chart generation:
- Created `scripts/gen_org_charts.py` script that:
  - Loads Flask app context and Mizan database models
  - Reads active employees (status = 'على قوة العمل') from database
  - Reads ongoing projects (project_state = 'تحت التنفيذ') from database
  - Loads optional supporting Excel files (emp_sort.xlsx, Office-RE.xlsx)
  - Generates 4 region-specific HTML org chart files
  - Writes to app/static/org_charts/ with filenames 09-12_OrgChart_*.html

HTML output features:
- NWC + Al-Amro header with branding
- KPI cards: employee count, project count per region
- Employee cards: name, job title, RE code, direct manager, nationality
- Project cards: name, contractor, RE code, dates, SAR value
- RTL Arabic layout with Cairo font, responsive grid design
- Print-friendly CSS media queries

Script tested end-to-end with sample data:
- 4 sample employees across 3 regions
- 3 sample projects across 3 regions
- All 4 org chart HTML files generated successfully

## Next (one task)

**Org Chart Integration Routes** — Build routes to serve org chart files via web interface and add to navigation.
Or: **Database Population** — Import actual employee and project data, then run org chart script.
